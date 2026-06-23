"""安全控制：API Key 鉴权（常量时间比较）、进程内限流、WS 鉴权。

服务经 ngrok 公网暴露，鉴权与限流为必需项。
限流为进程内令牌桶，按客户端 IP；单 worker 部署下足够，重启即重置。
"""
import secrets

from fastapi import HTTPException, Request, Security, WebSocket
from fastapi.security import APIKeyHeader

from stocksdk.config import (
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
    get_api_key,
)
from stocksdk.ratelimit import RateLimiter, keys_match

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# 框架无关原语在 ratelimit.py，security.py 仅做 FastAPI 适配。
_keys_match = keys_match  # 兼容旧调用名


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


_limiter = RateLimiter(RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW_SECONDS)


def rate_limit(request: Request):
    """依赖项：按客户端 IP 限流，超限抛 429。"""
    client_ip = request.client.host if request.client else "unknown"
    if not _limiter.check(client_ip):
        raise HTTPException(
            429,
            "请求过于频繁：{}s 内最多 {} 次".format(RATE_LIMIT_WINDOW_SECONDS, RATE_LIMIT_REQUESTS),
        )
