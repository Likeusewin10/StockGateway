"""网关对外鉴权 + 限流中间件（Starlette ASGI）。

复用 stocksdk.security 的常量时间比较与按 IP 限流，不重写。
鉴权失败在进入 MCP 处理前返回 401/429，不进 MCP 层。
未配置 API_KEY 则放行（仅本机/内网场景）。
"""
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from stocksdk.config import RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW_SECONDS
from stocksdk.ratelimit import RateLimiter, keys_match
from mcp_gateway.config import get_api_key

logger = logging.getLogger("mcp_gateway.auth")

_limiter = RateLimiter(RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW_SECONDS)


def _extract_key(request: Request) -> str:
    """优先 X-API-Key；兼容 MCP 客户端常用的 Authorization: Bearer <key>。"""
    key = request.headers.get("x-api-key")
    if key:
        return key
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:]
    return ""


class ApiKeyAuthMiddleware(BaseHTTPMiddleware):
    """按 API Key 鉴权 + 按客户端 IP 限流。"""

    async def dispatch(self, request: Request, call_next):
        expected = get_api_key()
        if expected:  # 未配 key 时整体放行（内网）
            provided = _extract_key(request)
            if not keys_match(provided, expected):
                return JSONResponse({"error": "缺少或错误的 API Key"}, status_code=401)

        client_ip = request.client.host if request.client else "unknown"
        if not _limiter.check(client_ip):
            return JSONResponse(
                {
                    "error": "请求过于频繁：{}s 内最多 {} 次".format(
                        RATE_LIMIT_WINDOW_SECONDS, RATE_LIMIT_REQUESTS
                    )
                },
                status_code=429,
            )
        return await call_next(request)
