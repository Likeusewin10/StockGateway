"""hub → 对等机小服务（peer_service.py）的 HTTP 客户端。

对等机不再跑 MCP 网关，改跑纯 HTTP 的哑执行服务（/exec、/task、/file、/admin/*）。
本模块把那些原语封成同步方法，供 peers.py 生成的 hub 原生工具调用。

- 鉴权：每次请求带 X-API-Key（该 peer 独立 key，绝不入日志）。
- 🔴 connect 超时必须短（对等机随时可能关机）：否则一台宕机拖慢 hub 整体。
- 失败一律返回 {ok: False, error}，不抛异常 —— 让上层工具把错误如实回给调用方。
"""
import logging
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger("mcp_gateway.peer_client")

# 连接超时短、读超时覆盖单次原语（/exec 立即返 task_id，不等子进程；/file 传块最大 ~11MB）。
CONNECT_TIMEOUT_SECONDS = 5.0
READ_TIMEOUT_SECONDS = 120.0


class PeerClient:
    """一台对等机的 HTTP 客户端；base_url 为其公网入口（去掉可能的 /mcp 尾巴）。"""

    def __init__(self, name: str, base_url: str, api_key: str):
        self.name = name
        self.base_url = base_url.rstrip("/")
        # 兼容旧 .env：peer URL 曾指向 MCP 端点 .../mcp，小服务的原语在根路径下。
        if self.base_url.endswith("/mcp"):
            self.base_url = self.base_url[: -len("/mcp")]
        self._headers = {"X-API-Key": api_key} if api_key else {}
        self._timeout = httpx.Timeout(READ_TIMEOUT_SECONDS, connect=CONNECT_TIMEOUT_SECONDS)

    def _post(self, path: str, body: Dict[str, Any]) -> Dict[str, Any]:
        try:
            with httpx.Client(timeout=self._timeout) as client:
                resp = client.post(self.base_url + path, json=body, headers=self._headers)
            return self._parse(resp)
        except httpx.HTTPError as exc:
            return {"ok": False, "error": f"peer {self.name} 请求失败：{type(exc).__name__}: {exc}"}

    def _get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            with httpx.Client(timeout=self._timeout) as client:
                resp = client.get(self.base_url + path, params=params, headers=self._headers)
            return self._parse(resp)
        except httpx.HTTPError as exc:
            return {"ok": False, "error": f"peer {self.name} 请求失败：{type(exc).__name__}: {exc}"}

    @staticmethod
    def _parse(resp: httpx.Response) -> Dict[str, Any]:
        try:
            data = resp.json()
        except ValueError:
            return {"ok": False, "error": f"peer 返回非 JSON（HTTP {resp.status_code}）：{resp.text[:200]}"}
        if resp.status_code == 401:
            return {"ok": False, "error": "peer 鉴权失败（401）：检查 PEER_<NAME>_API_KEY"}
        return data

    # ---- 原语 ----
    def exec(self, argv: List[str], timeout: int = 0) -> Dict[str, Any]:
        return self._post("/exec", {"argv": argv, "timeout": timeout})

    def task_status(self, task_id: str) -> Dict[str, Any]:
        return self._get("/task", {"id": task_id})

    def task_result(self, task_id: str) -> Dict[str, Any]:
        return self._get("/task", {"id": task_id, "full": "1"})

    def health(self) -> Dict[str, Any]:
        return self._get("/health", {})

    def file_put(self, path: str, data_b64: str, mode: str = "write",
                 mkdirs: bool = True, expected_size: int = -1) -> Dict[str, Any]:
        return self._post("/file", {"action": "put", "path": path, "data_b64": data_b64,
                                    "mode": mode, "mkdirs": mkdirs, "expected_size": expected_size})

    def file_get(self, path: str, offset: int = 0, max_bytes: int = 0) -> Dict[str, Any]:
        return self._post("/file", {"action": "get", "path": path,
                                    "offset": offset, "max_bytes": max_bytes})

    def file_stat(self, path: str) -> Dict[str, Any]:
        return self._post("/file", {"action": "stat", "path": path})

    def admin_update(self, source_b64: str, restart_delay: int = 8) -> Dict[str, Any]:
        return self._post("/admin/update", {"source_b64": source_b64, "restart_delay": restart_delay})

    def admin_restart(self, delay: int = 8) -> Dict[str, Any]:
        return self._post("/admin/restart", {"delay": delay})
