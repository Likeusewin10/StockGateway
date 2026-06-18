"""集成测试：WebSocket 推送端点（SDK 已桩替换）。

用 TestClient 的 websocket_connect 驱动订阅/退订/错误分支。
SDK 回调在桩里不会真正触发后台线程，这里只验证协议层。
"""
import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def ws_client_noauth(monkeypatch):
    monkeypatch.setenv("API_KEY", "")
    monkeypatch.setenv("CORS_ORIGINS", "")
    import stocksdk.sessions as sessions
    importlib.reload(sessions)
    import app as app_module
    importlib.reload(app_module)
    return TestClient(app_module.app)


@pytest.fixture
def ws_client_authed(monkeypatch):
    monkeypatch.setenv("API_KEY", "wskey")
    import stocksdk.sessions as sessions
    importlib.reload(sessions)
    import app as app_module
    importlib.reload(app_module)
    return TestClient(app_module.app)


def test_em_ws_subscribe_unsubscribe(ws_client_noauth):
    with ws_client_noauth.websocket_connect("/em/ws") as ws:
        ws.send_json({"action": "subscribe", "codes": "300059.SZ", "indicators": "now"})
        msg = ws.receive_json()
        assert msg["event"] == "subscribed"
        assert msg["serial"] == 42
        ws.send_json({"action": "unsubscribe", "serial": 42})
        msg = ws.receive_json()
        assert msg["event"] == "unsubscribed"


def test_em_ws_unknown_action(ws_client_noauth):
    with ws_client_noauth.websocket_connect("/em/ws") as ws:
        ws.send_json({"action": "frobnicate"})
        msg = ws.receive_json()
        assert msg["event"] == "error"


def test_em_ws_bad_json(ws_client_noauth):
    with ws_client_noauth.websocket_connect("/em/ws") as ws:
        ws.send_text("not json")
        msg = ws.receive_json()
        assert msg["event"] == "error"
        assert "JSON" in msg["msg"]


def test_em_ws_auth_rejected(ws_client_authed):
    with ws_client_authed.websocket_connect("/em/ws") as ws:
        msg = ws.receive_json()
        assert msg["event"] == "error"


def test_em_ws_auth_ok_with_key(ws_client_authed):
    with ws_client_authed.websocket_connect("/em/ws?key=wskey") as ws:
        ws.send_json({"action": "subscribe", "codes": "x", "indicators": "now"})
        msg = ws.receive_json()
        assert msg["event"] == "subscribed"


def test_ths_ws_subscribe(ws_client_noauth):
    with ws_client_noauth.websocket_connect("/ths/ws") as ws:
        ws.send_json({"action": "subscribe", "codes": "300033.SZ", "indicators": "latest"})
        msg = ws.receive_json()
        assert msg["event"] == "subscribed"
        assert msg["codes"] == "300033.SZ"


def test_ths_ws_unsubscribe(ws_client_noauth):
    with ws_client_noauth.websocket_connect("/ths/ws") as ws:
        ws.send_json({"action": "unsubscribe", "codes": "300033.SZ", "indicators": "latest"})
        msg = ws.receive_json()
        assert msg["event"] == "unsubscribed"


def test_ths_ws_unknown_action(ws_client_noauth):
    with ws_client_noauth.websocket_connect("/ths/ws") as ws:
        ws.send_json({"action": "nope"})
        msg = ws.receive_json()
        assert msg["event"] == "error"


def test_ths_ws_bad_json(ws_client_noauth):
    with ws_client_noauth.websocket_connect("/ths/ws") as ws:
        ws.send_text("{{bad")
        msg = ws.receive_json()
        assert msg["event"] == "error"


def test_ths_ws_auth_rejected(ws_client_authed):
    with ws_client_authed.websocket_connect("/ths/ws") as ws:
        msg = ws.receive_json()
        assert msg["event"] == "error"
