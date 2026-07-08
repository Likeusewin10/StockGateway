"""peer_service.py 端到端单测：线程内起真服务，用 urllib 打各原语。

不桩 subprocess —— exec 用跨平台无害命令（python -c）实测状态机；文件原语用 tmp_path。
"""
import base64
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import peer_service as ps  # noqa: E402


@pytest.fixture
def server(monkeypatch, tmp_path):
    """起服务在随机端口，返回 (base_url, api_key)。每例独立 key/work_dir。"""
    monkeypatch.setenv("PEER_API_KEY", "test-key-123")
    monkeypatch.setenv("PEER_WORK_DIR", str(tmp_path))
    # 重置任务表，避免跨例污染
    ps.REGISTRY.__init__()
    srv = ThreadingHTTPServer(("127.0.0.1", 0), ps._Handler)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{port}", "test-key-123"
    srv.shutdown()


def _req(url, method="GET", key=None, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if key:
        req.add_header("X-API-Key", key)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


def _wait_terminal(base, key, task_id, timeout=15):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        _, st = _req(f"{base}/task?id={task_id}", key=key)
        if st.get("status") in ("done", "failed", "timeout", "unknown"):
            return st
        time.sleep(0.1)
    return {"status": "poll_timeout"}


class TestAuth:
    def test_missing_key_rejected(self, server):
        base, _ = server
        code, payload = _req(f"{base}/health")
        assert code == 401 and payload["ok"] is False

    def test_wrong_key_rejected(self, server):
        base, _ = server
        code, _p = _req(f"{base}/health", key="wrong")
        assert code == 401

    def test_valid_key_ok(self, server):
        base, key = server
        code, payload = _req(f"{base}/health", key=key)
        assert code == 200 and payload["service"] == "peer_service"
        assert "claude" in payload["engines"]


class TestExec:
    def test_exec_success(self, server):
        base, key = server
        argv = [sys.executable, "-c", "print('hello-peer')"]
        code, sub = _req(f"{base}/exec", method="POST", key=key, body={"argv": argv})
        assert code == 200 and sub["status"] == "running"
        result = _wait_terminal(base, key, sub["task_id"])
        assert result["status"] == "done"
        _, full = _req(f"{base}/task?id={sub['task_id']}&full=1", key=key)
        assert "hello-peer" in full["output"] and full["returncode"] == 0

    def test_exec_nonzero_is_failed(self, server):
        base, key = server
        argv = [sys.executable, "-c", "import sys; sys.exit(3)"]
        _, sub = _req(f"{base}/exec", method="POST", key=key, body={"argv": argv})
        result = _wait_terminal(base, key, sub["task_id"])
        assert result["status"] == "failed"

    def test_exec_unknown_command(self, server):
        base, key = server
        code, sub = _req(f"{base}/exec", method="POST", key=key,
                         body={"argv": ["no_such_cmd_xyz_123"]})
        assert sub["ok"] is False and "PATH" in sub["error"]

    def test_exec_empty_argv_rejected(self, server):
        base, key = server
        _, sub = _req(f"{base}/exec", method="POST", key=key, body={"argv": []})
        assert sub["ok"] is False

    def test_exec_allowlist_blocks(self, server, monkeypatch):
        base, key = server
        monkeypatch.setenv("PEER_EXEC_ALLOW", "claude,codex")
        _, sub = _req(f"{base}/exec", method="POST", key=key,
                      body={"argv": [sys.executable, "-c", "print(1)"]})
        assert sub["ok"] is False and "白名单" in sub["error"]

    def test_timeout_kills(self, server, monkeypatch):
        base, key = server
        argv = [sys.executable, "-c", "import time; time.sleep(30)"]
        _, sub = _req(f"{base}/exec", method="POST", key=key,
                      body={"argv": argv, "timeout": 1})
        result = _wait_terminal(base, key, sub["task_id"])
        assert result["status"] == "timeout"

    def test_cwd_locked_to_work_dir(self, server, tmp_path):
        base, key = server
        argv = [sys.executable, "-c", "import os; print(os.getcwd())"]
        _, sub = _req(f"{base}/exec", method="POST", key=key, body={"argv": argv})
        _wait_terminal(base, key, sub["task_id"])
        _, full = _req(f"{base}/task?id={sub['task_id']}&full=1", key=key)
        assert str(tmp_path.resolve()) in os.path.realpath(full["output"].strip())


class TestFile:
    def test_put_get_roundtrip(self, server, tmp_path):
        base, key = server
        target = str(tmp_path / "sub" / "data.bin")
        payload = bytes(range(256)) * 4
        b64 = base64.b64encode(payload).decode()
        _, put = _req(f"{base}/file", method="POST", key=key,
                      body={"action": "put", "path": target, "data_b64": b64})
        assert put["ok"] and put["bytes_written"] == len(payload)
        _, get = _req(f"{base}/file", method="POST", key=key,
                      body={"action": "get", "path": target})
        assert base64.b64decode(get["data_b64"]) == payload and get["eof"]

    def test_append_chunks_and_stat(self, server, tmp_path):
        base, key = server
        target = str(tmp_path / "big.bin")
        c1, c2 = b"A" * 100, b"B" * 50
        _req(f"{base}/file", method="POST", key=key,
             body={"action": "put", "path": target,
                   "data_b64": base64.b64encode(c1).decode(), "mode": "write"})
        _, ap = _req(f"{base}/file", method="POST", key=key,
                     body={"action": "put", "path": target,
                           "data_b64": base64.b64encode(c2).decode(),
                           "mode": "append", "expected_size": 100})
        assert ap["ok"] and ap["size"] == 150
        _, stat = _req(f"{base}/file", method="POST", key=key,
                       body={"action": "stat", "path": target})
        import hashlib
        assert stat["sha256"] == hashlib.sha256(c1 + c2).hexdigest()

    def test_append_expected_size_mismatch_rejected(self, server, tmp_path):
        base, key = server
        target = str(tmp_path / "x.bin")
        _req(f"{base}/file", method="POST", key=key,
             body={"action": "put", "path": target,
                   "data_b64": base64.b64encode(b"AAA").decode()})
        _, ap = _req(f"{base}/file", method="POST", key=key,
                     body={"action": "put", "path": target,
                           "data_b64": base64.b64encode(b"B").decode(),
                           "mode": "append", "expected_size": 999})
        assert ap["ok"] is False

    def test_relative_path_rejected(self, server):
        base, key = server
        _, put = _req(f"{base}/file", method="POST", key=key,
                      body={"action": "put", "path": "relative/x.bin",
                            "data_b64": base64.b64encode(b"x").decode()})
        assert put["ok"] is False

    def test_bad_action(self, server, tmp_path):
        base, key = server
        _, r = _req(f"{base}/file", method="POST", key=key,
                    body={"action": "nope", "path": str(tmp_path / "a")})
        assert r["ok"] is False


class TestSelfUpdate:
    def test_bad_syntax_rejected_no_swap(self, server, tmp_path, monkeypatch):
        # 指向一份可写副本作为 __file__，避免动到真实文件
        fake = tmp_path / "svc.py"
        fake.write_text("# original\n")
        monkeypatch.setattr(ps, "__file__", str(fake))
        bad = base64.b64encode(b"def broken(:\n").decode()
        # 直接调函数（不经 HTTP，__file__ 已 monkeypatch 到副本）
        res = ps.self_update(bad)
        assert res["ok"] is False and fake.read_text() == "# original\n"

    def test_valid_source_swaps(self, server, tmp_path, monkeypatch):
        fake = tmp_path / "svc.py"
        fake.write_text("# original\n")
        monkeypatch.setattr(ps, "__file__", str(fake))
        monkeypatch.setattr(ps, "schedule_restart", lambda delay=8: {"ok": True, "pid": 0})
        good = base64.b64encode(b"x = 1  # new version\n").decode()
        res = ps.self_update(good)
        assert res["ok"] and "new version" in fake.read_text()


class TestRouting:
    def test_unknown_path_404(self, server):
        base, key = server
        code, _p = _req(f"{base}/nope", key=key)
        assert code == 404

    def test_task_missing_id_400(self, server):
        base, key = server
        code, _p = _req(f"{base}/task", key=key)
        assert code == 400

    def test_unknown_task_id(self, server):
        base, key = server
        _, st = _req(f"{base}/task?id=deadbeef", key=key)
        assert st["status"] == "unknown"
