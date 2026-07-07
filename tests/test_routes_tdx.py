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
    expected = {"/tdx/bars", "/tdx/snapshot", "/tdx/more_info", "/tdx/stock_info", "/tdx/financial",
                "/tdx/sector", "/tdx/stock_list", "/tdx/trading_dates",
                "/tdx/health", "/tdx/asset", "/tdx/positions", "/tdx/orders",
                "/tdx/order", "/tdx/cancel", "/tdx/methods", "/tdx/call/{method}"}
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


def test_tdx_more_info_returns_more_and_gpjy(app_client):
    r = app_client.get("/tdx/more_info", params={"code": "600519.SH"})
    assert r.status_code == 200
    body = r.json()
    assert body["code"] == "600519.SH"
    assert body["EverZTCount"] == "2"
    assert body["FCAmo"] == "12345.67"
    assert body["GP14"] == 1.0
    assert body["GP15"] == 2.0
    assert body["GP24"] == 93000.0
    assert body["gpjy_raw"]["GP14"]["600519.SH"] == 1.0


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


# ---------- 交易查询（读，需账户句柄） ----------

def _enable_tdx_trading(monkeypatch):
    monkeypatch.setenv("TDX_TRADING_ENABLED", "true")


def test_tdx_health_connected(app_client):
    r = app_client.get("/tdx/health")
    assert r.status_code == 200
    assert r.json()["connected"] is True


def test_tdx_asset_ok(app_client):
    r = app_client.get("/tdx/asset")
    assert r.status_code == 200
    assert r.json()["Cash"] == "30234.070"


def test_tdx_positions_ok(app_client):
    r = app_client.get("/tdx/positions")
    assert r.status_code == 200
    assert r.json()[0]["Code"] == "000001.SZ"


def test_tdx_orders_ok(app_client):
    r = app_client.get("/tdx/orders")
    assert r.status_code == 200
    assert r.json()[0]["Wtbh"] == "58545"


# ---------- 交易总开关 ----------

def _disable_tdx_trading(monkeypatch):
    monkeypatch.delenv("TDX_TRADING_ENABLED", raising=False)


def test_tdx_order_blocked_when_trading_disabled(app_client, monkeypatch):
    _disable_tdx_trading(monkeypatch)
    r = app_client.post("/tdx/order", json={
        "side": "buy", "stock_code": "600519.SH", "volume": 100,
        "price_type": "limit", "price": 10.5})
    assert r.status_code == 503


def test_tdx_cancel_blocked_when_trading_disabled(app_client, monkeypatch):
    _disable_tdx_trading(monkeypatch)
    r = app_client.post("/tdx/cancel", json={"stock_code": "600519.SH", "order_id": 58545})
    assert r.status_code == 503


# ---------- 下单 dry-run / 真发 / 失败 ----------

def test_tdx_order_dry_run_default(app_client, monkeypatch):
    _enable_tdx_trading(monkeypatch)
    r = app_client.post("/tdx/order", json={
        "side": "buy", "stock_code": "600519.SH", "volume": 100,
        "price_type": "limit", "price": 10.5})
    assert r.status_code == 200
    body = r.json()
    assert body["dry_run"] is True
    assert body["would_send"]["price"] == 10.5


def test_tdx_order_confirm_sends(app_client, monkeypatch):
    _enable_tdx_trading(monkeypatch)
    r = app_client.post("/tdx/order", json={
        "side": "buy", "stock_code": "600519.SH", "volume": 100,
        "price_type": "limit", "price": 10.5, "confirm": True})
    assert r.status_code == 200
    body = r.json()
    assert body["dry_run"] is False
    assert body["order_id"] == "58545"
    assert body["value"] == 1


def test_tdx_order_failure_returns_502(app_client, monkeypatch):
    _enable_tdx_trading(monkeypatch)
    r = app_client.post("/tdx/order", json={
        "side": "buy", "stock_code": "FAIL.SH", "volume": 100,
        "price_type": "limit", "price": 10.5, "confirm": True})
    assert r.status_code == 502


def test_tdx_order_market_price_ok(app_client, monkeypatch):
    _enable_tdx_trading(monkeypatch)
    r = app_client.post("/tdx/order", json={
        "side": "sell", "stock_code": "600519.SH", "volume": 100,
        "price_type": "market", "confirm": True})
    assert r.status_code == 200
    assert r.json()["value"] == 1


# ---------- 护栏 ----------

def test_tdx_guard_max_notional(app_client, monkeypatch):
    _enable_tdx_trading(monkeypatch)
    monkeypatch.setenv("TDX_MAX_NOTIONAL", "1000")
    r = app_client.post("/tdx/order", json={
        "side": "buy", "stock_code": "600519.SH", "volume": 1000,
        "price_type": "limit", "price": 10.5, "confirm": True})   # 10500 > 1000
    assert r.status_code == 409
    assert "max_notional" in r.json()["detail"]


def test_tdx_guard_whitelist(app_client, monkeypatch):
    _enable_tdx_trading(monkeypatch)
    monkeypatch.setenv("TDX_CODE_WHITELIST", "000001.SZ")
    r = app_client.post("/tdx/order", json={
        "side": "buy", "stock_code": "600519.SH", "volume": 100,
        "price_type": "limit", "price": 10.5, "confirm": True})
    assert r.status_code == 409
    assert "whitelist" in r.json()["detail"]


def test_tdx_guard_daily_cap(app_client, monkeypatch):
    _enable_tdx_trading(monkeypatch)
    monkeypatch.setenv("TDX_DAILY_ORDER_CAP", "1")
    ok = app_client.post("/tdx/order", json={
        "side": "buy", "stock_code": "600519.SH", "volume": 100,
        "price_type": "limit", "price": 10.5, "confirm": True})
    assert ok.status_code == 200
    blocked = app_client.post("/tdx/order", json={
        "side": "buy", "stock_code": "600519.SH", "volume": 100,
        "price_type": "limit", "price": 10.5, "confirm": True})
    assert blocked.status_code == 409
    assert "daily_cap" in blocked.json()["detail"]


def test_tdx_order_bad_side_400(app_client, monkeypatch):
    _enable_tdx_trading(monkeypatch)
    r = app_client.post("/tdx/order", json={
        "side": "hold", "stock_code": "600519.SH", "volume": 100,
        "price_type": "limit", "price": 10.5, "confirm": True})
    assert r.status_code == 400


def test_tdx_limit_without_price_400(app_client, monkeypatch):
    _enable_tdx_trading(monkeypatch)
    r = app_client.post("/tdx/order", json={
        "side": "buy", "stock_code": "600519.SH", "volume": 100,
        "price_type": "limit", "confirm": True})
    assert r.status_code == 400


# ---------- 撤单 ----------

def test_tdx_cancel_ok(app_client, monkeypatch):
    _enable_tdx_trading(monkeypatch)
    r = app_client.post("/tdx/cancel", json={
        "stock_code": "688318.SH", "order_id": 58545, "confirm": True})
    assert r.status_code == 200
    assert r.json()["value"] == 1


def test_tdx_cancel_dry_run(app_client, monkeypatch):
    _enable_tdx_trading(monkeypatch)
    r = app_client.post("/tdx/cancel", json={"stock_code": "688318.SH", "order_id": 58545})
    assert r.status_code == 200
    assert r.json()["dry_run"] is True


def test_tdx_cancel_failure_409(app_client, monkeypatch):
    _enable_tdx_trading(monkeypatch)
    r = app_client.post("/tdx/cancel", json={
        "stock_code": "688318.SH", "order_id": -999, "confirm": True})
    assert r.status_code == 409


# ---------- 透传拦截（交易/账户类）----------

def test_tdx_call_account_query_blocked_403(app_client):
    r = app_client.post("/tdx/call/query_stock_asset", json={"args": []})
    assert r.status_code == 403


def test_tdx_methods_account_label(app_client):
    out = app_client.get("/tdx/methods").json()
    assert out["query_stock_asset"].startswith("blocked(需账户句柄")
    assert out["stock_account"].startswith("blocked(需账户句柄")


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


# ---------- tdx_order_result / tdx_cancel_result（单元） ----------

def test_tdx_order_result_success():
    out = serialize.tdx_order_result({"ErrorId": "0", "Msg": "待确认", "Value": 1, "Wtbh": "58545"})
    assert out == {"dry_run": False, "value": 1, "order_id": "58545", "msg": "待确认"}


def test_tdx_order_result_value_zero_raises_502():
    with pytest.raises(HTTPException) as ei:
        serialize.tdx_order_result({"ErrorId": "0", "Msg": "资金不足", "Value": 0})
    assert ei.value.status_code == 502


def test_tdx_order_result_error_id_raises_502():
    with pytest.raises(HTTPException) as ei:
        serialize.tdx_order_result({"ErrorId": "-1", "Msg": "未登录", "Value": 1})
    assert ei.value.status_code == 502


def test_tdx_cancel_result_success():
    out = serialize.tdx_cancel_result({"ErrorId": "0", "Msg": "已受理", "Value": 1})
    assert out == {"value": 1, "msg": "已受理"}


def test_tdx_cancel_result_value_zero_raises_409():
    with pytest.raises(HTTPException) as ei:
        serialize.tdx_cancel_result({"ErrorId": "0", "Msg": "委托已完成", "Value": 0})
    assert ei.value.status_code == 409


def test_tdx_cancel_result_error_id_raises_502():
    with pytest.raises(HTTPException) as ei:
        serialize.tdx_cancel_result({"ErrorId": "-1", "Msg": "未登录", "Value": 1})
    assert ei.value.status_code == 502


# ---------- 账户句柄管理（单元） ----------

def test_ensure_tdx_account_caches_handle(sessions, monkeypatch):
    monkeypatch.setattr(sessions.tdx, "initialize", lambda *a, **k: None)
    monkeypatch.setenv("TDX_ACCOUNT_ID", "acct-1")
    calls = {"n": 0}

    def _acct(account="", account_type="STOCK"):
        calls["n"] += 1
        return 7

    monkeypatch.setattr(sessions.tdx, "stock_account", _acct)
    sessions._tdx_ready = False
    sessions._tdx_account_id = None
    assert sessions.ensure_tdx_account() == 7
    assert sessions.ensure_tdx_account() == 7   # 复用缓存
    assert calls["n"] == 1


def test_ensure_tdx_account_handle_zero_ok(sessions, monkeypatch):
    monkeypatch.setattr(sessions.tdx, "initialize", lambda *a, **k: None)
    monkeypatch.setenv("TDX_ACCOUNT_ID", "acct-1")
    monkeypatch.setattr(sessions.tdx, "stock_account", lambda **k: 0)   # 合法句柄 0
    sessions._tdx_ready = False
    sessions._tdx_account_id = None
    assert sessions.ensure_tdx_account() == 0


def test_ensure_tdx_account_invalid_raises_502(sessions, monkeypatch):
    monkeypatch.setattr(sessions.tdx, "initialize", lambda *a, **k: None)
    monkeypatch.setenv("TDX_ACCOUNT_ID", "acct-1")
    monkeypatch.setattr(sessions.tdx, "stock_account", lambda **k: -1)   # 无效哨兵
    sessions._tdx_ready = False
    sessions._tdx_account_id = None
    with pytest.raises(HTTPException) as ei:
        sessions.ensure_tdx_account()
    assert ei.value.status_code == 502


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
