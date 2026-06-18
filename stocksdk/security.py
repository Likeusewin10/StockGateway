"""安全控制：API Key 鉴权（常量时间比较）、进程内限流、WS 鉴权。

服务经 ngrok 公网暴露，鉴权与限流为必需项。
限流为进程内令牌桶，按客户端 IP；单 worker 部署下足够，重启即重置。
"""
import secrets
import threading
import time

from fastapi import HTTPException, Request, Security, WebSocket
from fastapi.security import APIKeyHeader

from stocksdk.config import (
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
    get_api_key,
)

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def _keys_match(provided: str, expected: str) -> bool:
    """常量时间比较，避免按字符提前返回导致的时序侧信道。"""
    if not provided:
        return False
    return secrets.compare_digest(provided, expected)


def require_key(key: str = Security(_api_key_header)):
    """依赖项：未配置 API_KEY 时不鉴权；否则请求头 X-API-Key 必须匹配。"""
    expected = get_api_key()
    if not expected:          # 未配置 key：不鉴权（仅本机/内网场景）
        return
    if not _keys_match(key or "", expected):
        raise HTTPException(401, "缺少或错误的 X-API-Key")


def ws_authed(ws: WebSocket) -> bool:
    """WebSocket 鉴权：WS 不便带请求头，改走 query 参数 ?key=。"""
    expected = get_api_key()
    if not expected:
        return True
    return _keys_match(ws.query_params.get("key") or "", expected)


class RateLimiter:
    """按 IP 的滑动窗口计数限流。线程安全（取数端点持锁串行，仍加锁防 WS 并发）。"""

    def __init__(self, max_requests: int, window_seconds: int):
        self._max = max_requests
        self._window = window_seconds
        self._hits: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def check(self, client_id: str) -> bool:
        """记录一次访问并返回是否允许。超限返回 False。"""
        now = time.monotonic()
        cutoff = now - self._window
        with self._lock:
            hits = [t for t in self._hits.get(client_id, []) if t > cutoff]
            if len(hits) >= self._max:
                self._hits[client_id] = hits
                return False
            hits.append(now)
            self._hits[client_id] = hits
            return True


_limiter = RateLimiter(RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW_SECONDS)


def rate_limit(request: Request):
    """依赖项：按客户端 IP 限流，超限抛 429。"""
    client_ip = request.client.host if request.client else "unknown"
    if not _limiter.check(client_ip):
        raise HTTPException(
            429,
            "请求过于频繁：{}s 内最多 {} 次".format(RATE_LIMIT_WINDOW_SECONDS, RATE_LIMIT_REQUESTS),
        )
