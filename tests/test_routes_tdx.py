"""集成 + 单元测试：通达信 TDX /tdx/* 路由、tdx_result 归一化、会话自愈。

SDK 已在 conftest 桩替换（FakeTdxClient），不触发真实终端连接。
"""
import importlib

import pandas as pd
import pytest
from fastapi import HTTPException

from stocksdk import serialize


# ---------- 路由（集成） ----------

def test_tdx_paths_in_openapi(app_client):
    paths = set(app_client.get("/openapi.json").json()["paths"].keys())
    expected = {"/tdx/bars", "/tdx/snapshot", "/tdx/stock_info", "/tdx/financial",
                "/tdx/sector", "/tdx/stock_list", "/tdx/trading_dates",
                "/tdx/methods", "/tdx/call/{method}"}
    assert expected.issubset(paths)


def test_tdx_bars_returns_records(app_client):
    r = app_client.get("/tdx/bars", params={
        "codes": "600519.SH", "period": "1d", "count": 3, "dividend": "none",
    })
    assert r.status_code == 200
    body = r.json()
    # dict{字段: records}
    assert "Close" in body and isinstance(body["Close"], list)
    assert "index" in body["Close"][0]


def test_tdx_snapshot_returns_dict(app_client):
    r = app_client.get("/tdx/snapshot", params={"code": "600519.SH"})
    assert r.status_code == 200
    body = r.json()
    assert body["Now"] == "35.06" and body["ErrorId"] == "0"


def test_tdx_stock_info_returns_dict(app_client):
    r = app_client.get("/tdx/stock_info", params={"code": "600519.SH", "fields": "Name"})
    assert r.status_code == 200
    assert r.json()["Name"] == "贵州茅台"


def test_tdx_sector_returns_list(app_client):
    r = app_client.get("/tdx/sector", params={"block": "钛金属", "block_type": 1, "list_type": 1})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_tdx_methods_labels(app_client):
    out = app_client.get("/tdx/methods").json()
    assert out["get_market_data"] == "ok"
    assert out["order_stock"].startswith("blocked(交易")
    assert out["send_message"].startswith("blocked(写")
    assert out["initialize"].startswith("blocked(会话")
    assert out["subscribe_hq"].startswith("ok(异步")


def test_tdx_call_passthrough_ok(app_client):
    r = app_client.post("/tdx/call/get_divid_factors", json={"args": ["688318.SH", "", ""]})
    assert r.status_code == 200


def test_tdx_call_trading_blocked_403(app_client):
    r = app_client.post("/tdx/call/order_stock", json={"args": []})
    assert r.status_code == 403


def test_tdx_call_write_blocked_403(app_client):
    r = app_client.post("/tdx/call/send_message", json={"args": ["hi"]})
    assert r.status_code == 403


def test_tdx_call_session_blocked_403(app_client):
    r = app_client.post("/tdx/call/close", json={"args": []})
    assert r.status_code == 403


def test_tdx_call_private_403(app_client):
    r = app_client.post("/tdx/call/__class__")
    assert r.status_code == 403


def test_tdx_call_unknown_404(app_client):
    r = app_client.post("/tdx/call/does_not_exist")
    assert r.status_code == 404


# ---------- tdx_result（单元） ----------

def test_tdx_result_market_data_df_to_records():
    df = pd.DataFrame({"2026-06-30": [1185.49]}, index=["600519.SH"])
    out = serialize.tdx_result({"Close": df})
    assert out["Close"] == [{"index": "600519.SH", "2026-06-30": 1185.49}]


def test_tdx_result_flat_dict_passes():
    out = serialize.tdx_result({"Now": "35.06", "ErrorId": "0"})
    assert out == {"Now": "35.06", "ErrorId": "0"}


def test_tdx_result_error_id_raises_502():
    with pytest.raises(HTTPException) as ei:
        serialize.tdx_result({"ErrorId": "-1", "Error": "未登录"})
    assert ei.value.status_code == 502


def test_tdx_result_list_passes():
    out = serialize.tdx_result([{"Code": "600000.SH"}])
    assert out == [{"Code": "600000.SH"}]


# ---------- 会话自愈（单元） ----------

@pytest.fixture
def sessions(monkeypatch):
    import stocksdk.sessions as s
    importlib.reload(s)
    return s


def test_ensure_tdx_success(sessions, monkeypatch):
    monkeypatch.setattr(sessions.tdx, "initialize", lambda *a, **k: None)
    sessions._tdx_ready = False
    sessions.ensure_tdx()   # 不抛即通过


def test_ensure_tdx_failure_raises_502(sessions, monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("终端未开")
    monkeypatch.setattr(sessions.tdx, "initialize", boom)
    sessions._tdx_ready = False
    with pytest.raises(HTTPException) as ei:
        sessions.ensure_tdx()
    assert ei.value.status_code == 502


def test_tdx_exec_retries_on_exception(sessions, monkeypatch):
    calls = {"init": 0, "fn": 0}
    monkeypatch.setattr(sessions.tdx, "initialize",
                        lambda *a, **k: calls.__setitem__("init", calls["init"] + 1))
    sessions._tdx_ready = False

    def fn():
        calls["fn"] += 1
        if calls["fn"] == 1:
            raise RuntimeError("断连")
        return {"ErrorId": "0", "ok": 1}

    r = sessions.tdx_exec(fn)
    assert calls["fn"] == 2 and calls["init"] >= 2
    assert r["ok"] == 1


def test_tdx_exec_retries_on_session_dead(sessions, monkeypatch):
    calls = {"init": 0, "fn": 0}
    monkeypatch.setattr(sessions.tdx, "initialize",
                        lambda *a, **k: calls.__setitem__("init", calls["init"] + 1))
    sessions._tdx_ready = False

    def fn():
        calls["fn"] += 1
        return {"ErrorId": "-1", "Error": "未登录"} if calls["fn"] == 1 else {"ErrorId": "0"}

    sessions.tdx_exec(fn)
    assert calls["fn"] == 2 and calls["init"] >= 2


def test_tdx_session_dead_detection(sessions):
    assert sessions._tdx_session_dead(None) is True
    assert sessions._tdx_session_dead({"ErrorId": "-1", "Error": "未登录"}) is True
    assert sessions._tdx_session_dead({"ErrorId": "0"}) is False
    # ErrorId 非0但消息无会话关键词 → 不判失效（普通业务错误）
    assert sessions._tdx_session_dead({"ErrorId": "-5", "Error": "字段无效"}) is False
