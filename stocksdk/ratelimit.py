"""框架无关的鉴权/限流原语（仅标准库）。

从 security.py 抽出，使无 FastAPI 的进程（如 mcp_gateway）也能复用同一份逻辑，
避免两套限流/比较实现漂移。security.py 仍从此处导入，行为不变。
"""
import secrets
import threading
import time


def keys_match(provided: str, expected: str) -> bool:
    """常量时间比较，避免按字符提前返回导致的时序侧信道。"""
    if not provided:
        return False
    return secrets.compare_digest(provided, expected)


class RateLimiter:
    """按 IP 的滑动窗口计数限流。线程安全。"""

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
