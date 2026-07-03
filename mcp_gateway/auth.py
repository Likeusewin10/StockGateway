"""网关对外鉴权 + 限流中间件（Starlette ASGI）。

复用 stocksdk.security 的常量时间比较与按 IP 限流，不重写。
鉴权失败在进入 MCP 处理前返回 401/429，不进 MCP 层。
未配置 API_KEY 则放行（仅本机/内网场景）。
"""
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from stocksdk.ratelimit import RateLimiter, keys_match
from mcp_gateway.config import (
    GATEWAY_RATE_LIMIT_REQUESTS,
    GATEWAY_RATE_LIMIT_WINDOW_SECONDS,
    get_api_key,
)

logger = logging.getLogger("mcp_gateway.auth")

_limiter = RateLimiter(GATEWAY_RATE_LIMIT_REQUESTS, GATEWAY_RATE_LIMIT_WINDOW_SECONDS)


def _extract_key(request: Request) -> str:
    """优先 X-API-Key；兼容 MCP 客户端常用的 Authorization: Bearer <key>。"""
    key = request.headers.get("x-api-key")
    if key:
        return key
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:]
    return ""


def _rate_key(request: Request) -> str:
    """限流键：优先按 MCP 会话（mcp-session-id），回退到客户端 IP。

    经 ngrok 后所有客户端的 request.client.host 折叠成同一隧道 IP，按 IP 限流会
    让多个客户端共享一个预算、互相挤爆。按 session 计则每个 MCP 会话独立预算。
    握手期首个 POST（尚无 session-id）回退到 IP，阈值已放宽到不影响正常握手。
    """
    sid = request.headers.get("mcp-session-id")
    if sid:
        return "sid:" + sid
    client_ip = request.client.host if request.client else "unknown"
    return "ip:" + client_ip


class ApiKeyAuthMiddleware(BaseHTTPMiddleware):
    """按 API Key 鉴权 + 按 MCP 会话限流。"""

    async def dispatch(self, request: Request, call_next):
        expected = get_api_key()
        if expected:  # 未配 key 时整体放行（内网）
            provided = _extract_key(request)
            if not keys_match(provided, expected):
                return JSONResponse({"error": "缺少或错误的 API Key"}, status_code=401)

        # SSE 长流（GET）与会话拆除（DELETE）属传输控制，非取数调用，不计入限流。
        # MCP 客户端会每 1000ms 重连 SSE，若计入会瞬间打满限流并拖垮整条会话。
        if request.method in ("GET", "DELETE"):
            return await call_next(request)

        if not _limiter.check(_rate_key(request)):
            return JSONResponse(
                {
                    "error": "请求过于频繁：{}s 内最多 {} 次".format(
                        GATEWAY_RATE_LIMIT_WINDOW_SECONDS, GATEWAY_RATE_LIMIT_REQUESTS
                    )
                },
                status_code=429,
            )
        return await call_next(request)
