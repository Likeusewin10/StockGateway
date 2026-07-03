"""服务器端 Agent 异步任务核心单测（mcp_gateway/agent_runner.py）。

全程桩 subprocess，不起真 claude/codex 进程：
- monkeypatch subprocess.Popen 为可控假进程（stdout/returncode/挂起超时）。
- monkeypatch shutil.which 控制 CLI 是否「已装」。
覆盖：正常 done、非零退出 failed、超时 kill、engine 不在白名单、prompt 空、
codex CLI 缺失优雅降级、cwd 锁定目录、reason 脱敏截断、任务数上限清理。
"""
import time

import pytest

import mcp_gateway.agent_runner as ar
from mcp_gateway.agent_runner import AgentRunner, STATUS_DONE, STATUS_FAILED, STATUS_TIMEOUT


class FakeProc:
    """可控假子进程，模拟 communicate / kill / returncode。"""

    def __init__(self, stdout="", stderr="", returncode=0, hang=False):
        self._stdout = stdout
        self._stderr = stderr
        self.returncode = None
        self._final_rc = returncode
        self._hang = hang        # True 时首次 communicate 抛 TimeoutExpired
        self.killed = False
        self._hung_once = False

    def communicate(self, timeout=None):
        if self._hang and not self._hung_once:
            self._hung_once = True
            import subprocess
            raise subprocess.TimeoutExpired(cmd="fake", timeout=timeout)
        self.returncode = self._final_rc
        return self._stdout, self._stderr

    def kill(self):
        self.killed = True


def _wait_terminal(runner: AgentRunner, task_id: str, timeout=3.0):
    """轮询直到任务进入终态或超时（后台线程异步写状态）。"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        st = runner.status(task_id)["status"]
        if st in (STATUS_DONE, STATUS_FAILED, STATUS_TIMEOUT):
            return st
        time.sleep(0.02)
    return runner.status(task_id)["status"]


@pytest.fixture
def patch_which_ok(monkeypatch):
    """让所有引擎都「已装」。"""
    monkeypatch.setattr(ar.shutil, "which", lambda name: "/usr/bin/" + name)


def test_submit_done(monkeypatch, patch_which_ok):
    monkeypatch.setattr(ar, "AGENT_STREAM_JSON", False)  # 本用例测非流式 communicate 路径(FakeProc 模型)
    captured = {}

    def fake_popen(cmd, cwd=None, **kw):
        captured["cmd"] = cmd
        captured["cwd"] = cwd
        return FakeProc(stdout="hello world", returncode=0)

    monkeypatch.setattr(ar.subprocess, "Popen", fake_popen)
    runner = AgentRunner()
    r = runner.submit("claude", "列出当前目录")
    assert r["status"] == "running"
    tid = r["task_id"]
    assert _wait_terminal(runner, tid) == STATUS_DONE
    res = runner.result(tid)
    assert res["output"] == "hello world"
    assert res["returncode"] == 0


def test_submit_nonzero_exit_failed(monkeypatch, patch_which_ok):
    monkeypatch.setattr(ar, "AGENT_STREAM_JSON", False)  # 本用例测非流式 communicate 路径(FakeProc 模型)
    monkeypatch.setattr(
        ar.subprocess, "Popen",
        lambda cmd, cwd=None, **kw: FakeProc(stderr="boom", returncode=1),
    )
    runner = AgentRunner()
    tid = runner.submit("claude", "do x")["task_id"]
    assert _wait_terminal(runner, tid) == STATUS_FAILED
    assert "boom" in runner.result(tid)["error"]


def test_submit_timeout_kills(monkeypatch, patch_which_ok):
    monkeypatch.setattr(ar, "AGENT_STREAM_JSON", False)  # 本用例测非流式 communicate 路径(FakeProc 模型)
    proc = FakeProc(hang=True)
    monkeypatch.setattr(ar.subprocess, "Popen", lambda cmd, cwd=None, **kw: proc)
    runner = AgentRunner(timeout_seconds=1)
    tid = runner.submit("claude", "sleep forever")["task_id"]
    assert _wait_terminal(runner, tid) == STATUS_TIMEOUT
    assert proc.killed is True
    assert "超时" in runner.result(tid)["error"]


def test_engine_not_in_whitelist(monkeypatch, patch_which_ok):
    runner = AgentRunner()
    r = runner.submit("rogue", "x")
    assert r["status"] == STATUS_FAILED
    assert "不支持" in r["error"]


def test_empty_prompt_failed(monkeypatch, patch_which_ok):
    runner = AgentRunner()
    r = runner.submit("claude", "   ")
    assert r["status"] == STATUS_FAILED
    assert "prompt" in r["error"]


def test_codex_cli_missing_graceful(monkeypatch):
    # claude 已装、codex 未装：codex 优雅降级，不崩。
    monkeypatch.setattr(ar.shutil, "which", lambda name: "/usr/bin/claude" if name == "claude" else None)
    runner = AgentRunner()
    r = runner.submit("codex", "x")
    assert r["status"] == STATUS_FAILED
    assert "unavailable" in r["error"]


def test_cwd_locked_to_project_dir(monkeypatch, patch_which_ok):
    captured = {}
    monkeypatch.setattr(
        ar.subprocess, "Popen",
        lambda cmd, cwd=None, **kw: captured.update(cwd=cwd) or FakeProc(returncode=0),
    )
    runner = AgentRunner()
    runner.submit("claude", "x")
    assert captured["cwd"] == ar.get_agent_project_dir()


def test_command_template_substitutes_prompt(monkeypatch, patch_which_ok):
    captured = {}
    monkeypatch.setattr(
        ar.subprocess, "Popen",
        lambda cmd, cwd=None, **kw: captured.update(cmd=cmd) or FakeProc(returncode=0),
    )
    runner = AgentRunner()
    runner.submit("claude", "MYPROMPT")
    assert "MYPROMPT" in captured["cmd"]
    assert "--dangerously-skip-permissions" in captured["cmd"]


def test_dash_dash_sentinel_before_prompt(monkeypatch, patch_which_ok):
    # `--` 结束选项解析,防以 `-` 开头的 prompt 被当 flag(argument injection)。
    captured = {}
    monkeypatch.setattr(
        ar.subprocess, "Popen",
        lambda cmd, cwd=None, **kw: captured.update(cmd=cmd) or FakeProc(returncode=0),
    )
    runner = AgentRunner()
    runner.submit("claude", "--version")
    cmd = captured["cmd"]
    assert "--" in cmd
    # prompt 必须排在 `--` 之后,才不会被解析成 flag
    assert cmd.index("--") < cmd.index("--version")


def test_reason_sanitized_truncation():
    long = "x" * 5000
    assert len(ar._sanitize(long)) <= ar._MAX_REASON_LEN + 1  # +1 为省略号


def test_unknown_task_id():
    runner = AgentRunner()
    assert runner.status("nope")["status"] == "unknown"
    assert runner.result("nope")["status"] == "unknown"


def test_max_tasks_eviction(monkeypatch, patch_which_ok):
    monkeypatch.setattr(
        ar.subprocess, "Popen",
        lambda cmd, cwd=None, **kw: FakeProc(returncode=0),
    )
    runner = AgentRunner(max_tasks=3)
    ids = [runner.submit("claude", "x")["task_id"] for _ in range(5)]
    # 最旧两个被清理
    assert runner.status(ids[0])["status"] == "unknown"
    assert runner.status(ids[1])["status"] == "unknown"
    # 最近三个仍在
    for tid in ids[2:]:
        assert runner.status(tid)["status"] != "unknown"


def test_popen_raises_recorded_failed(monkeypatch, patch_which_ok):
    def boom(cmd, cwd=None, **kw):
        raise OSError("cannot exec")

    monkeypatch.setattr(ar.subprocess, "Popen", boom)
    runner = AgentRunner()
    r = runner.submit("claude", "x")
    assert r["status"] == STATUS_FAILED
    assert "cannot exec" in r["error"]


def test_project_dir_default(monkeypatch):
    from mcp_gateway.config import AGENT_PROJECT_DIR_DEFAULT, get_agent_project_dir
    monkeypatch.delenv("AGENT_PROJECT_DIR", raising=False)
    assert get_agent_project_dir() == AGENT_PROJECT_DIR_DEFAULT


def test_project_dir_override_outside_root_falls_back(monkeypatch):
    from mcp_gateway.config import AGENT_PROJECT_DIR_DEFAULT, get_agent_project_dir
    # 指向项目根之外(系统临时目录),应被拒绝并回退默认根
    monkeypatch.setenv("AGENT_PROJECT_DIR", "C:\\Windows" if __import__("os").name == "nt" else "/tmp")
    assert get_agent_project_dir() == AGENT_PROJECT_DIR_DEFAULT


# ---- 上下文接力（session_id 回传/续传）---------------------------------------

def _is_uuid(value: str) -> bool:
    import uuid
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, TypeError, AttributeError):
        return False


def test_claude_fresh_returns_server_generated_session_id(monkeypatch, patch_which_ok):
    # claude 首轮：服务器预生成 UUID，submit 返回里即带 session_id，命令行含 --session-id <该id>。
    monkeypatch.setattr(ar, "AGENT_STREAM_JSON", False)  # 终态断言走非流式 communicate 路径(FakeProc 模型)
    captured = {}
    monkeypatch.setattr(
        ar.subprocess, "Popen",
        lambda cmd, cwd=None, **kw: captured.update(cmd=cmd) or FakeProc(returncode=0),
    )
    runner = AgentRunner()
    r = runner.submit("claude", "记住数字 42")
    sid = r["session_id"]
    assert _is_uuid(sid)
    cmd = captured["cmd"]
    assert "--session-id" in cmd
    assert cmd[cmd.index("--session-id") + 1] == sid
    # 终态结果里仍带同一 session_id
    tid = r["task_id"]
    assert _wait_terminal(runner, tid) == STATUS_DONE
    assert runner.result(tid)["session_id"] == sid


def test_claude_resume_uses_passed_id(monkeypatch, patch_which_ok):
    # claude 续轮：传入合法 session_id，命令行改用 --resume <id>，回传同一 id。
    captured = {}
    monkeypatch.setattr(
        ar.subprocess, "Popen",
        lambda cmd, cwd=None, **kw: captured.update(cmd=cmd) or FakeProc(returncode=0),
    )
    sid = "4b167ebd-0b3d-4488-bf3f-a160b9bb8dc3"
    runner = AgentRunner()
    r = runner.submit("claude", "继续", session_id=sid)
    assert r["session_id"] == sid
    cmd = captured["cmd"]
    assert "--resume" in cmd
    assert cmd[cmd.index("--resume") + 1] == sid
    assert "--session-id" not in cmd     # 续轮不再带 --session-id


def test_codex_fresh_parses_session_id_from_jsonl(monkeypatch, patch_which_ok):
    # codex 首轮：id 由 codex 生成，从 --json(JSONL) 输出解析后回填。
    sid = "019edfbc-1784-7902-b0ca-39c61d53f0bf"
    jsonl = (
        '{"type":"session_meta","payload":{"id":"%s","cwd":"X"}}\n'
        '{"type":"event_msg","payload":{"type":"task_started"}}\n' % sid
    )
    monkeypatch.setattr(
        ar.subprocess, "Popen",
        lambda cmd, cwd=None, **kw: FakeProc(stdout=jsonl, returncode=0),
    )
    runner = AgentRunner()
    r = runner.submit("codex", "你好")
    # codex 首轮 id 在终态解析回填（submit 立即返回时可能已填或未填，取决于子进程快慢，
    # 故此处只对终态结果断言，不对 submit 即时返回断言）。
    tid = r["task_id"]
    assert _wait_terminal(runner, tid) == STATUS_DONE
    assert runner.result(tid)["session_id"] == sid


def test_codex_resume_uses_resume_subcommand(monkeypatch, patch_which_ok):
    # codex 续轮：命令行走 `codex exec resume <id>`。
    captured = {}
    monkeypatch.setattr(
        ar.subprocess, "Popen",
        lambda cmd, cwd=None, **kw: captured.update(cmd=cmd) or FakeProc(returncode=0),
    )
    sid = "019edfbc-1784-7902-b0ca-39c61d53f0bf"
    runner = AgentRunner()
    runner.submit("codex", "继续", session_id=sid)
    cmd = captured["cmd"]
    assert "resume" in cmd
    assert sid in cmd


def test_resume_rejects_invalid_session_id(monkeypatch, patch_which_ok):
    # 非法 session_id（非 UUID）→ 直接 failed，不起进程。
    started = {"n": 0}
    monkeypatch.setattr(
        ar.subprocess, "Popen",
        lambda cmd, cwd=None, **kw: started.update(n=started["n"] + 1) or FakeProc(returncode=0),
    )
    runner = AgentRunner()
    r = runner.submit("claude", "x", session_id="not-a-uuid")
    assert r["status"] == STATUS_FAILED
    assert "session_id" in r["error"]
    assert started["n"] == 0     # 未起任何子进程


def test_no_session_id_backward_compatible(monkeypatch, patch_which_ok):
    # codex 不传 session_id：维持原一次性行为（命令不含 resume 子命令）。
    captured = {}
    monkeypatch.setattr(
        ar.subprocess, "Popen",
        lambda cmd, cwd=None, **kw: captured.update(cmd=cmd) or FakeProc(returncode=0),
    )
    runner = AgentRunner()
    runner.submit("codex", "x")
    assert "resume" not in captured["cmd"]


def test_codex_missing_session_id_still_returns_result(monkeypatch, patch_which_ok):
    # codex 输出里解析不到 session_id：不报错，结果照常返回，session_id 留空。
    monkeypatch.setattr(
        ar.subprocess, "Popen",
        lambda cmd, cwd=None, **kw: FakeProc(stdout="no json here", returncode=0),
    )
    runner = AgentRunner()
    tid = runner.submit("codex", "x")["task_id"]
    assert _wait_terminal(runner, tid) == STATUS_DONE
    res = runner.result(tid)
    assert res["session_id"] is None
    assert res["output"] == "no json here"
