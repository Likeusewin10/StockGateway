"""集成测试：鉴权开启 + 限流的端到端行为。"""
import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def authed_client(monkeypatch):
    monkeypatch.setenv("API_KEY", "topsecret")
    monkeypatch.setenv("CORS_ORIGINS", "https://app.example.com")
    import stocksdk.sessions as sessions
    importlib.reload(sessions)
    import app as app_module
    importlib.reload(app_module)
    return TestClient(app_module.app)


def test_missing_key_rejected(authed_client):
    r = authed_client.get("/em/csd", params={
        "codes": "x", "indicators": "CLOSE",
        "startdate": "2024-01-01", "enddate": "2024-01-05",
    })
    assert r.status_code == 401


def test_correct_key_accepted(authed_client):
    r = authed_client.get("/em/csd", headers={"X-API-Key": "topsecret"}, params={
        "codes": "x", "indicators": "CLOSE",
        "startdate": "2024-01-01", "enddate": "2024-01-05",
    })
    assert r.status_code == 200


def test_wrong_key_rejected(authed_client):
    r = authed_client.get("/ths/funcs", headers={"X-API-Key": "nope"})
    assert r.status_code == 401


def test_rate_limit_returns_429(monkeypatch):
    # 把限流阈值压到很低，验证 429 触发
    monkeypatch.setenv("API_KEY", "")
    import stocksdk.security as security
    from stocksdk.security import RateLimiter
    monkeypatch.setattr(security, "_limiter", RateLimiter(max_requests=2, window_seconds=60))
    import stocksdk.sessions as sessions
    importlib.reload(sessions)
    import app as app_module
    importlib.reload(app_module)
    client = TestClient(app_module.app)

    params = {"codes": "x", "indicators": "CLOSE",
              "startdate": "2024-01-01", "enddate": "2024-01-05"}
    assert client.get("/em/csd", params=params).status_code == 200
    assert client.get("/em/csd", params=params).status_code == 200
    assert client.get("/em/csd", params=params).status_code == 429
