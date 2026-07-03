"""网关鉴权 + 限流中间件单测。

用一个最小 Starlette app 挂载中间件，避开 live 上游依赖。
"""
import importlib

import pytest
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient


def _build_client(monkeypatch, api_key: str, max_requests: int = 1000):
    """构造挂了鉴权中间件的测试 app。每次重置限流器避免跨用例污染。"""
    monkeypatch.setenv("API_KEY", api_key)

    import mcp_gateway.auth as auth_mod
    importlib.reload(auth_mod)  # 让 get_api_key 读到新 API_KEY，并重建 _limiter

    from stocksdk.ratelimit import RateLimiter
    auth_mod._limiter = RateLimiter(max_requests, 60)

    async def ok(request):
        return PlainTextResponse("ok")

    app = Starlette(
        routes=[Route("/mcp", ok, methods=["GET", "POST", "DELETE"])],
        middleware=[Middleware(auth_mod.ApiKeyAuthMiddleware)],
    )
    return TestClient(app)


class TestApiKeyAuth:
    def test_missing_key_returns_401(self, monkeypatch):
        client = _build_client(monkeypatch, "secret")
        resp = client.post("/mcp")
        assert resp.status_code == 401

    def test_wrong_key_returns_401(self, monkeypatch):
        client = _build_client(monkeypatch, "secret")
        resp = client.post("/mcp", headers={"X-API-Key": "nope"})
        assert resp.status_code == 401

    def test_correct_key_passes(self, monkeypatch):
        client = _build_client(monkeypatch, "secret")
        resp = client.post("/mcp", headers={"X-API-Key": "secret"})
        assert resp.status_code == 200
        assert resp.text == "ok"

    def test_bearer_authorization_accepted(self, monkeypatch):
        client = _build_client(monkeypatch, "secret")
        resp = client.post("/mcp", headers={"Authorization": "Bearer secret"})
        assert resp.status_code == 200

    def test_no_api_key_configured_passes_through(self, monkeypatch):
        client = _build_client(monkeypatch, "")  # 未配 key -> 放行
        resp = client.post("/mcp")
        assert resp.status_code == 200


class TestRateLimit:
    def test_exceeding_limit_returns_429(self, monkeypatch):
        client = _build_client(monkeypatch, "secret", max_requests=2)
        h = {"X-API-Key": "secret"}
        assert client.post("/mcp", headers=h).status_code == 200
        assert client.post("/mcp", headers=h).status_code == 200
        assert client.post("/mcp", headers=h).status_code == 429

    def test_get_and_delete_skip_rate_limit(self, monkeypatch):
        """SSE 长流(GET)与会话拆除(DELETE)属传输控制，不计入限流。

        MCP 客户端每 1000ms 重连 SSE，若计入会瞬间打满限流拖垮会话。
        """
        client = _build_client(monkeypatch, "secret", max_requests=1)
        h = {"X-API-Key": "secret"}
        # 用掉唯一的 POST 预算
        assert client.post("/mcp", headers=h).status_code == 200
        assert client.post("/mcp", headers=h).status_code == 429
        # GET / DELETE 仍应放行（鉴权仍需过）
        for _ in range(5):
            assert client.get("/mcp", headers=h).status_code == 200
            assert client.request("DELETE", "/mcp", headers=h).status_code == 200

    def test_rate_limit_isolated_per_session(self, monkeypatch):
        """按 mcp-session-id 计限：一个会话打满不影响另一个会话（经 ngrok IP 折叠场景）。"""
        client = _build_client(monkeypatch, "secret", max_requests=1)
        a = {"X-API-Key": "secret", "mcp-session-id": "sess-A"}
        b = {"X-API-Key": "secret", "mcp-session-id": "sess-B"}
        assert client.post("/mcp", headers=a).status_code == 200
        assert client.post("/mcp", headers=a).status_code == 429  # A 打满
        assert client.post("/mcp", headers=b).status_code == 200  # B 独立预算不受影响

    def test_get_delete_still_require_auth(self, monkeypatch):
        """不计限流不等于不鉴权：GET/DELETE 无 key 仍 401。"""
        client = _build_client(monkeypatch, "secret")
        assert client.get("/mcp").status_code == 401
        assert client.request("DELETE", "/mcp").status_code == 401
