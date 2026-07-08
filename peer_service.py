#!/usr/bin/env python3
"""对等机「哑执行」小服务 —— 多机 Agent 协同的对等机侧唯一落盘代码。

设计目标（用户拍板的架构）：**所有会演进的业务逻辑都留在 hub**，对等机只跑这一个
永不需要维护的极小服务。它不含任何业务语义，只提供几组「十年不用改」的原语：

  GET  /health              存活 + 服务版本 + 平台 + 引擎可用性（供 hub 审计全 fleet）
  POST /exec   {argv,...}    异步执行一条命令（立即返 task_id，后台线程跑，状态机同 agent_runner）
  GET  /task?id=&full=      查任务状态/结果
  POST /file   {action,...}  put/get/stat 主机文件（二进制安全，含分块 offset/append）
  POST /admin/update {...}   用推来的新版本覆盖自己（py_compile 自检 + 原子替换 + 延迟重启）
  POST /admin/restart {...}  延迟脱离式自杀，交给看门狗/launchd 拉起（使新代码生效）

关键切分：hub 负责拼 `claude -p ... -- <prompt>` 这类完整命令行（argv[0] 用裸引擎名
`claude`），本服务负责 **argv[0] 的 shutil.which 解析**（Windows 上 claude/codex 多为
.CMD shim，裸名 CreateProcess 会 WinError 2）与 **Popen encoding=utf-8**（不指定 Windows
用 GBK 解码非 ASCII 会丢输出）—— 这两个坑与对等机的 OS 强绑定，故留在这里而非 hub。

安全：X-API-Key 常量时间比较（与网关同信任模型：拿到 key 即可执行任意命令，与旧
agent_run 同级风险）。cwd 锁死 PEER_WORK_DIR，防任意路径。纯标准库 —— 对等机连
venv/fastmcp 都不需要，依赖漂移问题整个消失。

配置全走环境变量（读 .env 亦可，见 main）：
  PEER_API_KEY / API_KEY   对外鉴权 key（前者优先；留空=不鉴权，仅本机/内网）
  PEER_SERVICE_PORT        监听端口（默认 8765，顶替旧网关位置，frp/域名零改动复用）
  PEER_WORK_DIR            exec 子进程 cwd（默认本文件所在目录）
  PEER_EXEC_ALLOW          可选：argv[0] basename 白名单（逗号分隔），留空=允许任意
  FS_PUT_MAX_BYTES / FS_GET_MAX_BYTES   单次文件传输字节上限（默认 8MB）
  PEER_TASK_TIMEOUT_SECONDS / PEER_MAX_TASKS   任务超时 / 内存保留任务数
"""
import base64
import binascii
import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import threading
import time
import uuid
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PureWindowsPath
from typing import Any, Dict, List, Optional, Tuple

SERVICE_VERSION = "1.0.0"

# 任务状态机（与 mcp_gateway.agent_runner 同口径）。
STATUS_RUNNING = "running"
STATUS_DONE = "done"
STATUS_FAILED = "failed"
STATUS_TIMEOUT = "timeout"

# 单任务 stdout/stderr 保留字节上限（防长任务撑爆内存）。
_OUTPUT_CAP = 4 * 1024 * 1024
# 请求体上限（自更新推来的整份源码也走这条，留足余量）。
_REQUEST_CAP = 32 * 1024 * 1024
# 流式哈希块大小。
_CHUNK = 1024 * 1024
# MSYS/Git-Bash 盘符路径：/c/Users/... → C:/Users/...（仅 Windows 语义）。
_MSYS_DRIVE_RE = re.compile(r"^/([A-Za-z])(/|$)")


# ---- 配置（全部 live 读环境变量，便于测试 monkeypatch）----

def _api_key() -> str:
    return (os.environ.get("PEER_API_KEY") or os.environ.get("API_KEY") or "").strip()


def _port() -> int:
    raw = os.environ.get("PEER_SERVICE_PORT", "").strip()
    return int(raw) if raw else 8765


def _work_dir() -> str:
    raw = os.environ.get("PEER_WORK_DIR", "").strip()
    return raw if raw else str(Path(__file__).resolve().parent)


def _exec_allow() -> List[str]:
    raw = os.environ.get("PEER_EXEC_ALLOW", "").strip()
    return [x.strip().lower() for x in raw.split(",") if x.strip()]


def _int_env(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    return int(raw) if raw else default


def _fs_put_max() -> int:
    return _int_env("FS_PUT_MAX_BYTES", 8 * 1024 * 1024)


def _fs_get_max() -> int:
    return _int_env("FS_GET_MAX_BYTES", 8 * 1024 * 1024)


def _task_timeout() -> int:
    return _int_env("PEER_TASK_TIMEOUT_SECONDS", 600)


def _max_tasks() -> int:
    return _int_env("PEER_MAX_TASKS", 100)


# ---- 任务表 -----------------------------------------------------------------

class _Task:
    """一个 exec 子进程任务的全部状态（精简自 agent_runner.AgentTask）。"""

    def __init__(self, task_id: str, argv: List[str]):
        self.task_id = task_id
        self.argv = argv
        self.status = STATUS_RUNNING
        self.output = ""
        self.error = ""
        self.returncode: Optional[int] = None
        self.proc: Optional[subprocess.Popen] = None

    def status_view(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"task_id": self.task_id, "status": self.status}
        if self.error and self.status in (STATUS_FAILED, STATUS_TIMEOUT):
            out["error"] = self.error
        return out

    def result_view(self) -> Dict[str, Any]:
        return {"task_id": self.task_id, "status": self.status,
                "output": self.output, "error": self.error,
                "returncode": self.returncode}


class _Registry:
    """进程内任务表：submit 起进程、查询、超时 kill、按上限清理最旧。"""

    def __init__(self):
        self._tasks: Dict[str, _Task] = {}
        self._order: deque = deque()
        self._lock = threading.Lock()

    def submit(self, argv: List[str], timeout: int) -> Dict[str, Any]:
        """起一个子进程任务；argv[0] 在本机解析为完整路径。立即返回 {task_id,status}。"""
        if not isinstance(argv, list) or not argv or not all(isinstance(a, str) for a in argv):
            return {"ok": False, "error": "argv 必须为非空字符串数组"}
        allow = _exec_allow()
        if allow and Path(argv[0]).name.lower() not in allow:
            return {"ok": False, "error": f"argv[0] {argv[0]!r} 不在 PEER_EXEC_ALLOW 白名单"}
        exe = shutil.which(argv[0])
        if exe is None:
            return {"ok": False, "error": f"命令未安装或不在 PATH：{argv[0]!r}"}

        task = _Task(uuid.uuid4().hex, argv)
        resolved = [exe, *argv[1:]]
        try:
            proc = subprocess.Popen(
                resolved,
                cwd=_work_dir(),                 # 🔴 cwd 锁死工作目录
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",                # 🔴 不指定 Windows 用 GBK 解码非 ASCII 会丢输出
                errors="replace",
            )
        except Exception as exc:  # noqa: BLE001  起进程失败不抛，登记 failed
            task.status = STATUS_FAILED
            task.error = f"{type(exc).__name__}: {exc}"[:_OUTPUT_CAP]
            self._store(task)
            return task.status_view()

        task.proc = proc
        self._store(task)
        threading.Thread(target=self._wait, args=(task, timeout), daemon=True).start()
        return {"task_id": task.task_id, "status": STATUS_RUNNING}

    def _wait(self, task: _Task, timeout: int) -> None:
        proc = task.proc
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            try:
                stdout, stderr = proc.communicate(timeout=10)
            except Exception:  # noqa: BLE001
                stdout, stderr = "", ""
            with self._lock:
                task.status = STATUS_TIMEOUT
                task.output = (stdout or "")[:_OUTPUT_CAP]
                task.error = f"超时 {timeout}s 已被 kill。{(stderr or '')[:2000]}"
                task.returncode = proc.returncode
            return
        except Exception as exc:  # noqa: BLE001
            with self._lock:
                task.status = STATUS_FAILED
                task.error = f"{type(exc).__name__}: {exc}"[:_OUTPUT_CAP]
            return
        with self._lock:
            task.returncode = proc.returncode
            task.output = (stdout or "")[:_OUTPUT_CAP]
            if proc.returncode == 0:
                task.status = STATUS_DONE
            else:
                task.status = STATUS_FAILED
                task.error = (stderr or f"退出码 {proc.returncode}")[:_OUTPUT_CAP]

    def status(self, task_id: str) -> Dict[str, Any]:
        task = self._get(task_id)
        return task.status_view() if task else {"task_id": task_id, "status": "unknown"}

    def result(self, task_id: str) -> Dict[str, Any]:
        task = self._get(task_id)
        return task.result_view() if task else {"task_id": task_id, "status": "unknown"}

    def _store(self, task: _Task) -> None:
        with self._lock:
            self._tasks[task.task_id] = task
            self._order.append(task.task_id)
            while len(self._order) > _max_tasks():
                oldest = self._order.popleft()
                evicted = self._tasks.pop(oldest, None)
                if evicted and evicted.status == STATUS_RUNNING and evicted.proc:
                    try:
                        evicted.proc.kill()
                    except Exception:  # noqa: BLE001
                        pass

    def _get(self, task_id: str) -> Optional[_Task]:
        with self._lock:
            return self._tasks.get(task_id)


REGISTRY = _Registry()


# ---- 文件传输（内联精简自 mcp_gateway.fs_tools，保持纯标准库自足）----

def _normalize_path(raw: str) -> Optional[Path]:
    """归一路径；非绝对路径返回 None。Windows 下 /c/Users → C:\\Users。"""
    s = (raw or "").strip()
    if not s:
        return None
    if os.name == "nt":
        m = _MSYS_DRIVE_RE.match(s)
        if m:
            s = f"{m.group(1).upper()}:/{s[m.end():]}"
        if not PureWindowsPath(s).drive:
            return None
    p = Path(s)
    if not p.is_absolute():
        return None
    return p.resolve()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(_CHUNK):
            h.update(chunk)
    return h.hexdigest()


def fs_put(path: str, data_b64: str, mode: str = "write",
           mkdirs: bool = True, expected_size: int = -1) -> Dict[str, Any]:
    p = _normalize_path(path)
    if p is None:
        return {"ok": False, "error": f"path 非法（须为绝对路径）：{path!r}"}
    if mode not in ("write", "append"):
        return {"ok": False, "error": f"mode 非法（须为 write/append）：{mode!r}"}
    try:
        data = base64.b64decode(data_b64, validate=True)
    except (binascii.Error, ValueError) as exc:
        return {"ok": False, "error": f"data_b64 非法 base64：{exc}"}
    if len(data) > _fs_put_max():
        return {"ok": False,
                "error": f"单次写入 {len(data)} 字节超上限 {_fs_put_max()}，请用 mode='append' 分块"}
    try:
        if mkdirs:
            p.parent.mkdir(parents=True, exist_ok=True)
        if mode == "append" and expected_size >= 0:
            current = p.stat().st_size if p.exists() else 0
            if current != expected_size:
                return {"ok": False, "size": current,
                        "error": f"expected_size 不匹配：当前 {current} 字节，期望 {expected_size}"}
        with open(p, "wb" if mode == "write" else "ab") as f:
            f.write(data)
        size = p.stat().st_size
    except OSError as exc:
        return {"ok": False, "error": f"写入失败：{exc}"}
    result: Dict[str, Any] = {"ok": True, "path": str(p), "bytes_written": len(data),
                              "size": size, "sha256": None}
    if mode == "write":
        try:
            result["sha256"] = _sha256_file(p)
        except OSError as exc:
            result["warning"] = f"写入成功但哈希失败：{exc}"
    return result


def fs_get(path: str, offset: int = 0, max_bytes: int = 0) -> Dict[str, Any]:
    p = _normalize_path(path)
    if p is None:
        return {"ok": False, "error": f"path 非法（须为绝对路径）：{path!r}"}
    if offset < 0 or max_bytes < 0:
        return {"ok": False, "error": "offset/max_bytes 须 >= 0"}
    limit = max_bytes if 0 < max_bytes <= _fs_get_max() else _fs_get_max()
    try:
        size = p.stat().st_size
        with open(p, "rb") as f:
            f.seek(offset)
            data = f.read(limit)
    except OSError as exc:
        return {"ok": False, "error": f"读取失败：{exc}"}
    return {"ok": True, "path": str(p), "size": size, "offset": offset,
            "bytes_read": len(data), "eof": offset + len(data) >= size,
            "sha256": hashlib.sha256(data).hexdigest(),
            "data_b64": base64.b64encode(data).decode("ascii")}


def fs_stat(path: str) -> Dict[str, Any]:
    p = _normalize_path(path)
    if p is None:
        return {"ok": False, "error": f"path 非法（须为绝对路径）：{path!r}"}
    try:
        size = p.stat().st_size
        sha256 = _sha256_file(p)
    except OSError as exc:
        return {"ok": False, "error": f"读取失败：{exc}"}
    return {"ok": True, "path": str(p), "size": size, "sha256": sha256}


def _dispatch_file(body: Dict[str, Any]) -> Dict[str, Any]:
    action = str(body.get("action", "")).strip().lower()
    path = body.get("path", "")
    if action == "put":
        return fs_put(path, body.get("data_b64", ""),
                      mode=body.get("mode", "write"),
                      mkdirs=bool(body.get("mkdirs", True)),
                      expected_size=int(body.get("expected_size", -1)))
    if action == "get":
        return fs_get(path, offset=int(body.get("offset", 0)),
                      max_bytes=int(body.get("max_bytes", 0)))
    if action == "stat":
        return fs_stat(path)
    return {"ok": False, "error": f"action 非法（须 put/get/stat）：{action!r}"}


# ---- 自更新 / 重启 ----------------------------------------------------------

def schedule_restart(delay: int = 8) -> Dict[str, Any]:
    """延迟 + 脱离式杀掉本进程（自己是被看门狗/launchd 拉起的，退出后会被重新拉起）。

    自己无法同步杀自己（会中断响应），故起一个分离子进程延迟后 kill 本 PID。
    """
    pid = os.getpid()
    try:
        if os.name == "nt":
            flags = getattr(subprocess, "DETACHED_PROCESS", 0) | \
                    getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            subprocess.Popen(
                ["cmd", "/c", f"timeout /t {delay} >nul & taskkill /F /PID {pid}"],
                creationflags=flags, close_fds=True)
        else:
            subprocess.Popen(["sh", "-c", f"sleep {delay}; kill -9 {pid}"],
                             start_new_session=True, close_fds=True)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    return {"ok": True, "pid": pid, "delay": delay}


def self_update(source_b64: str, restart_delay: int = 8) -> Dict[str, Any]:
    """用推来的新源码覆盖本文件：py_compile 自检通过才原子替换，再安排延迟重启。

    自检失败绝不替换（避免把服务写坏后拉不起来）。替换成功后看门狗重启即加载新版本。
    """
    try:
        source = base64.b64decode(source_b64, validate=True)
    except (binascii.Error, ValueError) as exc:
        return {"ok": False, "error": f"source_b64 非法 base64：{exc}"}
    target = Path(__file__).resolve()
    tmp = target.with_suffix(".py.new")
    try:
        tmp.write_bytes(source)
    except OSError as exc:
        return {"ok": False, "error": f"写临时文件失败：{exc}"}
    import py_compile
    try:
        py_compile.compile(str(tmp), doraise=True)
    except py_compile.PyCompileError as exc:
        try:
            tmp.unlink()
        except OSError:
            pass
        return {"ok": False, "error": f"新版本语法自检失败，未替换：{exc}"}
    try:
        os.replace(tmp, target)
    except OSError as exc:
        return {"ok": False, "error": f"原子替换失败：{exc}"}
    restart = schedule_restart(restart_delay)
    return {"ok": True, "bytes": len(source), "restart": restart}


def _health() -> Dict[str, Any]:
    return {
        "ok": True,
        "service": "peer_service",
        "version": SERVICE_VERSION,
        "platform": sys.platform,
        "python": sys.version.split()[0],
        "work_dir": _work_dir(),
        "engines": {
            "claude": shutil.which("claude") is not None,
            "codex": shutil.which("codex") is not None,
        },
    }


# ---- HTTP 层 ----------------------------------------------------------------

class _Handler(BaseHTTPRequestHandler):
    """极小路由；所有端点先过 X-API-Key 鉴权。失败一律 JSON，不抛裸异常。"""

    server_version = f"peer_service/{SERVICE_VERSION}"

    def log_message(self, fmt, *args):  # noqa: A003  静默默认 stderr 噪声
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    # -- 工具 --
    def _authed(self) -> bool:
        expected = _api_key()
        if not expected:
            return True  # 未配 key = 不鉴权（仅本机/内网）
        got = self.headers.get("X-API-Key", "") or self.headers.get("x-api-key", "")
        return secrets.compare_digest(got, expected)

    def _send(self, code: int, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _read_json(self) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length <= 0:
            return {}, None
        if length > _REQUEST_CAP:
            return None, f"请求体 {length} 超上限 {_REQUEST_CAP}"
        raw = self.rfile.read(length)
        try:
            obj = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            return None, f"请求体非法 JSON：{exc}"
        if not isinstance(obj, dict):
            return None, "请求体须为 JSON 对象"
        return obj, None

    def _query(self) -> Dict[str, str]:
        from urllib.parse import parse_qs, urlparse
        qs = parse_qs(urlparse(self.path).query)
        return {k: v[0] for k, v in qs.items()}

    def _path(self) -> str:
        from urllib.parse import urlparse
        return urlparse(self.path).path.rstrip("/") or "/"

    # -- 分发 --
    def do_GET(self):  # noqa: N802
        if not self._authed():
            return self._send(401, {"ok": False, "error": "unauthorized"})
        path = self._path()
        if path == "/health":
            return self._send(200, _health())
        if path == "/task":
            q = self._query()
            task_id = q.get("id", "")
            if not task_id:
                return self._send(400, {"ok": False, "error": "缺 id 参数"})
            full = q.get("full", "0") in ("1", "true", "yes")
            return self._send(200, REGISTRY.result(task_id) if full else REGISTRY.status(task_id))
        return self._send(404, {"ok": False, "error": f"未知路径：{path}"})

    def do_HEAD(self):  # noqa: N802
        if not self._authed():
            return self._send(401, {"ok": False, "error": "unauthorized"})
        return self._send(200, {"ok": True})

    def do_POST(self):  # noqa: N802
        if not self._authed():
            return self._send(401, {"ok": False, "error": "unauthorized"})
        path = self._path()
        body, err = self._read_json()
        if err:
            return self._send(400, {"ok": False, "error": err})
        try:
            if path == "/exec":
                argv = body.get("argv")
                timeout = int(body.get("timeout", 0)) or _task_timeout()
                return self._send(200, REGISTRY.submit(argv, timeout))
            if path == "/file":
                return self._send(200, _dispatch_file(body))
            if path == "/admin/update":
                res = self_update(body.get("source_b64", ""),
                                  int(body.get("restart_delay", 8)))
                return self._send(200 if res.get("ok") else 400, res)
            if path == "/admin/restart":
                return self._send(200, schedule_restart(int(body.get("delay", 8))))
        except Exception as exc:  # noqa: BLE001  任何处理异常都回 JSON,不断连
            return self._send(500, {"ok": False, "error": f"{type(exc).__name__}: {exc}"})
        return self._send(404, {"ok": False, "error": f"未知路径：{path}"})


def _load_dotenv() -> None:
    """极简 .env 加载（真实环境变量优先，与 stocksdk.config.load_dotenv 同 setdefault 语义）。

    不 import stocksdk —— 本服务须自足于对等机（可能没有该包）。仅解析 KEY=VALUE。
    """
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip('"').strip("'")
            if key:
                os.environ.setdefault(key, val)
    except OSError:
        pass


def main() -> None:
    _load_dotenv()
    host = os.environ.get("PEER_SERVICE_HOST", "0.0.0.0").strip() or "0.0.0.0"
    port = _port()
    if not _api_key():
        sys.stderr.write("[peer_service] 警告：未配置 PEER_API_KEY/API_KEY，当前不鉴权，勿暴露公网\n")
    server = ThreadingHTTPServer((host, port), _Handler)
    sys.stderr.write(f"[peer_service] v{SERVICE_VERSION} 监听 {host}:{port} work_dir={_work_dir()}\n")
    server.serve_forever()


if __name__ == "__main__":
    main()
