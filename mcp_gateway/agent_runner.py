"""服务器端 Agent 异步任务核心。

把 `claude -p` / `codex exec` 包成「立即返 task_id + 后台跑 + 轮询取结果」的异步任务，
避开 MCP 同步调用超时。每个任务起一个 `subprocess.Popen`，cwd 锁死项目目录，
后台 `threading.Thread` 等待+捕获 stdout/stderr+超时 kill，状态机
`running → done | failed | timeout`。

安全约束（与 plan 一致）：
- engine 限白名单（AGENT_ENGINES）；不在白名单 / CLI 未装 → 直接返回 failed，不起进程。
- cwd 锁死 AGENT_PROJECT_DIR，防任意路径读写。
- submit 探活与错误 reason 脱敏截断（不外泄长 URL/堆栈/token）；result 输出按需保留完整。
- 保留最近 N 个任务，超出清理最旧，防内存涨。

模式借鉴：routes_ws.py（后台线程+生命周期清理）、routes_health.py（脱敏不外抛）。
"""
import json
import logging
import shutil
import subprocess
import threading
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List, Optional

from mcp_gateway.config import (
    AGENT_ENGINES,
    AGENT_MAX_TASKS,
    AGENT_TASK_TIMEOUT_SECONDS,
    CODEX_SESSION_ID_KEYS,
    get_agent_project_dir,
)

logger = logging.getLogger("mcp_gateway.agent_runner")

# 脱敏：错误/原因消息最多回这么多字符，避免泄漏长 URL/堆栈/凭据。
_MAX_REASON_LEN = 500

# 状态机取值。
STATUS_RUNNING = "running"
STATUS_DONE = "done"
STATUS_FAILED = "failed"
STATUS_TIMEOUT = "timeout"


def _sanitize(text: str) -> str:
    """截断过长文本，避免泄漏长 URL/堆栈/凭据。"""
    if text is None:
        return ""
    text = str(text)
    if len(text) > _MAX_REASON_LEN:
        return text[:_MAX_REASON_LEN] + "…"
    return text


def _is_valid_uuid(value: str) -> bool:
    """会话 id 续轮前的格式校验：必须是合法 UUID（防命令行注入）。"""
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, AttributeError, TypeError):
        return False


@dataclass
class AgentTask:
    """一个 Agent 子进程任务的全部状态。"""

    task_id: str
    engine: str
    prompt: str
    status: str = STATUS_RUNNING
    output: str = ""          # 子进程 stdout（成功时的主要结果；claude 为 JSON 信封，原样透传）
    error: str = ""           # 错误原因 / stderr（脱敏截断）
    returncode: Optional[int] = None
    session_id: Optional[str] = None   # 会话 id：claude 首轮预生成/续轮回填；codex 终态解析回填
    _proc: Optional[subprocess.Popen] = field(default=None, repr=False)

    def snapshot_status(self) -> Dict[str, str]:
        """对外的轻量状态视图（不含完整 output，省带宽）。"""
        out = {"task_id": self.task_id, "status": self.status, "engine": self.engine}
        if self.session_id:
            out["session_id"] = self.session_id
        if self.error and self.status in (STATUS_FAILED, STATUS_TIMEOUT):
            out["error"] = self.error
        return out

    def snapshot_result(self) -> Dict[str, object]:
        """对外的完整结果视图（含 output / error / returncode / session_id）。"""
        return {
            "task_id": self.task_id,
            "status": self.status,
            "engine": self.engine,
            "session_id": self.session_id,
            "output": self.output,
            "error": self.error,
            "returncode": self.returncode,
        }


def _build_command(engine: str, prompt: str, executable: str,
                   session_id: Optional[str], is_resume: bool) -> List[str]:
    """按引擎模板拼命令行（区分首轮 fresh / 续轮 resume）。

    argv[0] 用 shutil.which 解析出的**完整路径**(executable),而非裸引擎名:
    Windows 上 claude/codex 多为 npm 生成的 .CMD shim,裸名经 CreateProcess
    不会自动补 .CMD 扩展名 → WinError 2。用完整路径可同时兼容 .exe/.cmd 且无需 shell=True。
    {prompt}/{session_id} 处分别替换为用户 prompt / 会话 id。
    """
    template = AGENT_ENGINES[engine]["resume" if is_resume else "fresh"]
    sid = session_id or ""
    cmd = [part.replace("{prompt}", prompt).replace("{session_id}", sid) for part in template]
    cmd[0] = executable    # 替换裸引擎名为解析后的完整可执行路径
    return cmd


def _extract_codex_session_id(stdout: str) -> Optional[str]:
    """从 codex --json(JSONL) 首轮输出里捞 session id。

    逐行 json.loads，按 CODEX_SESSION_ID_KEYS 在每行及其 payload 子对象里探测首个命中。
    解析失败/无命中返回 None（调用方留空 + warning，不影响结果返回）。
    """
    for line in (stdout or "").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, TypeError):
            continue
        # 顶层与 payload 子对象都查一遍（codex 把 meta 放在 payload 里）
        for scope in (obj, obj.get("payload") if isinstance(obj, dict) else None):
            if not isinstance(scope, dict):
                continue
            for key in CODEX_SESSION_ID_KEYS:
                val = scope.get(key)
                if isinstance(val, str) and val.strip():
                    return val.strip()
    return None


class AgentRunner:
    """异步 Agent 任务管理器：submit 起进程、status/result 查询、超时 kill、任务上限。"""

    def __init__(self, timeout_seconds: int = AGENT_TASK_TIMEOUT_SECONDS,
                 max_tasks: int = AGENT_MAX_TASKS):
        self._tasks: Dict[str, AgentTask] = {}
        self._order: Deque[str] = deque()    # 按创建顺序记录 task_id，便于清理最旧（O(1) popleft）
        self._lock = threading.Lock()        # 仅保护任务表，不与 SDK 全局锁相关
        self._timeout = timeout_seconds
        self._max_tasks = max_tasks

    # ---- 对外 API ----------------------------------------------------------

    def submit(self, engine: str, prompt: str,
               session_id: Optional[str] = None) -> Dict[str, str]:
        """起一个 Agent 子进程任务。立即返回 {task_id, status[, session_id]}。

        engine 不在白名单 / CLI 未装 / 起进程失败 → status=failed（不抛异常，附脱敏 reason）。

        session_id 语义（上下文接力）：
        - 不传：首轮全新会话。claude 服务器预生成 UUID 并回传；codex 终态从输出解析后回传。
        - 传入：续接该会话全部历史。先做 UUID 格式校验，非法直接 failed（防命令行注入）。
        """
        engine = (engine or "").strip().lower()
        if engine not in AGENT_ENGINES:
            return self._record_failed(
                engine, prompt,
                "engine 不支持：{}（仅 {}）".format(engine, "/".join(AGENT_ENGINES)),
            )
        if not (prompt or "").strip():
            return self._record_failed(engine, prompt, "prompt 不能为空")

        session_id = (session_id or "").strip() or None
        is_resume = session_id is not None
        if is_resume and not _is_valid_uuid(session_id):
            return self._record_failed(engine, prompt, "session_id 非法（须为 UUID）")

        executable = shutil.which(engine)
        if executable is None:
            return self._record_failed(
                engine, prompt, "引擎 CLI 未安装或不在 PATH：{}（unavailable）".format(engine),
            )

        # claude 首轮：服务器预生成 session id，id 在此刻即确定（不依赖解析子进程输出）。
        task_session_id = session_id
        if not is_resume and engine == "claude":
            task_session_id = str(uuid.uuid4())

        task = AgentTask(
            task_id=uuid.uuid4().hex, engine=engine, prompt=prompt,
            session_id=task_session_id,
        )
        try:
            proc = subprocess.Popen(
                _build_command(engine, prompt, executable, task_session_id, is_resume),
                cwd=get_agent_project_dir(),     # 🔴 cwd 锁死项目目录
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",                # claude/codex 输出为 UTF-8；
                errors="replace",                # 不指定则 Windows 用 GBK 解码非 ASCII 字节会抛错丢输出
            )
        except Exception as e:   # 起进程本身失败（命令不可执行等）
            return self._record_failed(engine, prompt, _sanitize("{}: {}".format(type(e).__name__, e)))

        task._proc = proc
        self._store(task)
        threading.Thread(target=self._wait, args=(task,), daemon=True).start()
        logger.info("Agent 任务已起 %s engine=%s resume=%s", task.task_id, engine, is_resume)
        # 固定返回 running：任务在 submit 这一刻定义为「已受理」，活态交给 status() 轮询；
        # 不读 task.status 实时值，避免极快子进程在本函数返回前已翻 done 造成歧义。
        out = {"task_id": task.task_id, "status": STATUS_RUNNING, "engine": engine}
        if task.session_id:
            out["session_id"] = task.session_id
        return out

    def status(self, task_id: str) -> Dict[str, str]:
        """查询任务状态（轻量）。未知 task_id → status=unknown。"""
        task = self._get(task_id)
        if task is None:
            return {"task_id": task_id, "status": "unknown"}
        return task.snapshot_status()

    def result(self, task_id: str) -> Dict[str, object]:
        """查询任务完整结果。未知 task_id → status=unknown。"""
        task = self._get(task_id)
        if task is None:
            return {"task_id": task_id, "status": "unknown"}
        return task.snapshot_result()

    # ---- 内部 --------------------------------------------------------------

    def _wait(self, task: AgentTask) -> None:
        """后台线程：等子进程结束，超时 kill，写回状态机。"""
        proc = task._proc
        try:
            stdout, stderr = proc.communicate(timeout=self._timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            try:
                stdout, stderr = proc.communicate(timeout=10)
            except Exception:
                stdout, stderr = "", ""
                try:
                    proc.wait(timeout=5)   # 末路兜底回收，防僵尸/句柄泄漏
                except Exception:
                    pass
            with self._lock:
                task.status = STATUS_TIMEOUT
                task.output = stdout or ""
                task.error = _sanitize("超时 {}s 已被 kill。{}".format(self._timeout, stderr or ""))
                task.returncode = proc.returncode
            logger.warning("Agent 任务超时 kill %s", task.task_id)
            return
        except Exception as e:
            with self._lock:
                task.status = STATUS_FAILED
                task.error = _sanitize("{}: {}".format(type(e).__name__, e))
            return

        with self._lock:
            task.returncode = proc.returncode
            task.output = stdout or ""
            if proc.returncode == 0:
                task.status = STATUS_DONE
                # codex 首轮：id 由 codex 生成，须从 --json 输出解析后回填。
                if task.engine == "codex" and not task.session_id:
                    sid = _extract_codex_session_id(task.output)
                    if sid:
                        task.session_id = sid
                    else:
                        logger.warning("Agent 任务 %s codex 输出未解析到 session_id", task.task_id)
            else:
                task.status = STATUS_FAILED
                task.error = _sanitize(stderr or "退出码 {}".format(proc.returncode))
        logger.info("Agent 任务结束 %s status=%s rc=%s", task.task_id, task.status, proc.returncode)

    def _record_failed(self, engine: str, prompt: str, reason: str) -> Dict[str, str]:
        """登记一个直接失败的任务（未起进程）并返回其状态。"""
        task = AgentTask(
            task_id=uuid.uuid4().hex, engine=engine, prompt=prompt,
            status=STATUS_FAILED, error=_sanitize(reason),
        )
        self._store(task)
        return task.snapshot_status()

    def _store(self, task: AgentTask) -> None:
        """入表并按上限清理最旧任务。被清理的任务若仍在跑，先 kill 防孤儿进程占资源。"""
        with self._lock:
            self._tasks[task.task_id] = task
            self._order.append(task.task_id)
            while len(self._order) > self._max_tasks:
                oldest = self._order.popleft()
                evicted = self._tasks.pop(oldest, None)
                if evicted and evicted.status == STATUS_RUNNING and evicted._proc:
                    try:
                        evicted._proc.kill()   # 没人会再读它的结果，别让它白占 CPU
                    except Exception:
                        pass

    def _get(self, task_id: str) -> Optional[AgentTask]:
        with self._lock:
            return self._tasks.get(task_id)


# 进程内单例：网关内所有 agent 工具共用一份任务表。
runner = AgentRunner()
