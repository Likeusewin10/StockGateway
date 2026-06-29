"""/qmt/* 交易路由测试：用 conftest 的 XtQuantTrader 桩，不连真终端。

覆盖：查询(asset/positions/orders/trades)、下单 dry-run/真发/失败、撤单、
交易总开关 503、护栏(金额/白名单/当日笔数)、透传拦截、methods 标注。
"""
import importlib


def _enable_trading(monkeypatch):
    monkeypatch.setenv("QMT_TRADING_ENABLED", "true")


# ----------------------------- 读类 -----------------------------

def test_asset_ok(app_client):
    r = app_client.get("/qmt/asset")
    assert r.status_code == 200
    body = r.json()
    assert body["total_asset"] == 150000.0
    assert body["cash"] == 100000.0


def test_positions_ok(app_client):
    r = app_client.get("/qmt/positions")
    assert r.status_code == 200
    assert r.json()[0]["stock_code"] == "600000.SH"


def test_orders_and_trades_ok(app_client):
    assert app_client.get("/qmt/orders").json()[0]["order_id"] == 12345
    assert app_client.get("/qmt/trades").json()[0]["traded_volume"] == 1000


def test_health_connected(app_client):
    r = app_client.get("/qmt/health")
    assert r.status_code == 200
    assert r.json()["connected"] is True


# ----------------------------- 交易总开关 -----------------------------

def test_order_blocked_when_trading_disabled(app_client):
    # 默认未开交易开关 → 503
    r = app_client.post("/qmt/order", json={
        "side": "buy", "stock_code": "600000.SH", "volume": 100,
        "price_type": "limit", "price": 10.5})
    assert r.status_code == 503


def test_cancel_blocked_when_trading_disabled(app_client):
    r = app_client.post("/qmt/cancel", json={"order_id": 12345})
    assert r.status_code == 503


# ----------------------------- 下单 dry-run / 真发 / 失败 -----------------------------

def test_order_dry_run_default(app_client, monkeypatch):
    _enable_trading(monkeypatch)
    r = app_client.post("/qmt/order", json={
        "side": "buy", "stock_code": "600000.SH", "volume": 100,
        "price_type": "limit", "price": 10.5})
    assert r.status_code == 200
    body = r.json()
    assert body["dry_run"] is True
    assert body["would_send"]["price"] == 10.5


def test_order_confirm_sends(app_client, monkeypatch):
    _enable_trading(monkeypatch)
    r = app_client.post("/qmt/order", json={
        "side": "buy", "stock_code": "600000.SH", "volume": 100,
        "price_type": "limit", "price": 10.5, "confirm": True})
    assert r.status_code == 200
    body = r.json()
    assert body["dry_run"] is False
    assert body["order_id"] == 12345


def test_order_failure_returns_502(app_client, monkeypatch):
    _enable_trading(monkeypatch)
    r = app_client.post("/qmt/order", json={
        "side": "buy", "stock_code": "FAIL.SH", "volume": 100,
        "price_type": "limit", "price": 10.5, "confirm": True})
    assert r.status_code == 502


def test_order_latest_price_ok(app_client, monkeypatch):
    _enable_trading(monkeypatch)
    r = app_client.post("/qmt/order", json={
        "side": "sell", "stock_code": "600000.SH", "volume": 100,
        "price_type": "latest", "confirm": True})
    assert r.status_code == 200
    assert r.json()["order_id"] == 12345


# ----------------------------- 护栏 -----------------------------

def test_guard_max_notional(app_client, monkeypatch):
    _enable_trading(monkeypatch)
    monkeypatch.setenv("QMT_MAX_NOTIONAL", "1000")   # 上限 1000 元
    r = app_client.post("/qmt/order", json={
        "side": "buy", "stock_code": "600000.SH", "volume": 1000,
        "price_type": "limit", "price": 10.5, "confirm": True})   # 10500 > 1000
    assert r.status_code == 409
    assert "max_notional" in r.json()["detail"]


def test_guard_whitelist(app_client, monkeypatch):
    _enable_trading(monkeypatch)
    monkeypatch.setenv("QMT_CODE_WHITELIST", "000001.SZ")
    r = app_client.post("/qmt/order", json={
        "side": "buy", "stock_code": "600000.SH", "volume": 100,
        "price_type": "limit", "price": 10.5, "confirm": True})
    assert r.status_code == 409
    assert "whitelist" in r.json()["detail"]


def test_guard_daily_cap(app_client, monkeypatch):
    _enable_trading(monkeypatch)
    monkeypatch.setenv("QMT_DAILY_ORDER_CAP", "1")
    ok = app_client.post("/qmt/order", json={
        "side": "buy", "stock_code": "600000.SH", "volume": 100,
        "price_type": "limit", "price": 10.5, "confirm": True})
    assert ok.status_code == 200
    blocked = app_client.post("/qmt/order", json={
        "side": "buy", "stock_code": "600000.SH", "volume": 100,
        "price_type": "limit", "price": 10.5, "confirm": True})
    assert blocked.status_code == 409
    assert "daily_cap" in blocked.json()["detail"]


def test_order_bad_side_400(app_client, monkeypatch):
    _enable_trading(monkeypatch)
    r = app_client.post("/qmt/order", json={
        "side": "hold", "stock_code": "600000.SH", "volume": 100,
        "price_type": "limit", "price": 10.5, "confirm": True})
    assert r.status_code == 400


def test_limit_without_price_400(app_client, monkeypatch):
    _enable_trading(monkeypatch)
    r = app_client.post("/qmt/order", json={
        "side": "buy", "stock_code": "600000.SH", "volume": 100,
        "price_type": "limit", "confirm": True})
    assert r.status_code == 400


# ----------------------------- 撤单 -----------------------------

def test_cancel_ok(app_client, monkeypatch):
    _enable_trading(monkeypatch)
    r = app_client.post("/qmt/cancel", json={"order_id": 12345, "confirm": True})
    assert r.status_code == 200
    assert r.json()["cancel_result"] == 0


def test_cancel_not_logged_in_409(app_client, monkeypatch):
    _enable_trading(monkeypatch)
    r = app_client.post("/qmt/cancel", json={"order_id": -999, "confirm": True})
    assert r.status_code == 409


# ----------------------------- 透传 / methods -----------------------------

def test_call_blocks_trading_method(app_client):
    r = app_client.post("/qmt/call/order_stock", json={"args": []})
    assert r.status_code == 403


def test_call_blocks_session_method(app_client):
    r = app_client.post("/qmt/call/connect", json={"args": []})
    assert r.status_code == 403


def test_call_query_passthrough(app_client):
    r = app_client.post("/qmt/call/query_stock_asset", json={"args": [None]})
    # query_stock_asset(account) 桩忽略入参，返回资产对象
    assert r.status_code == 200


def test_methods_annotates(app_client):
    body = app_client.get("/qmt/methods").json()
    assert "blocked" in body.get("order_stock", "")
    assert body.get("query_stock_asset", "").startswith("ok")


# ----------------------------- 行情数据 xtdata（/qmt/data/*）-----------------------------

def test_data_kline(app_client):
    r = app_client.get("/qmt/data/kline?codes=600000.SH&fields=close&period=1d")
    assert r.status_code == 200
    body = r.json()
    assert "close" in body
    assert body["close"]["data"][0][0] == 10.5   # to_json orient=split


def test_data_tick(app_client):
    r = app_client.get("/qmt/data/tick?codes=600000.SH")
    assert r.status_code == 200
    assert r.json()["600000.SH"]["lastPrice"] == 10.5


def test_data_sector(app_client):
    r = app_client.get("/qmt/data/sector?name=沪深A股")
    assert r.status_code == 200
    assert "600000.SH" in r.json()


def test_data_trading_dates(app_client):
    r = app_client.get("/qmt/data/trading_dates?market=SH")
    assert r.status_code == 200
    assert r.json() == [1704412800000]


def test_data_instrument(app_client):
    r = app_client.get("/qmt/data/instrument?code=600000.SH")
    assert r.status_code == 200
    assert r.json()["InstrumentID"] == "600000.SH"


def test_data_download(app_client):
    r = app_client.post("/qmt/data/download", json={"code": "600000.SH", "period": "1d"})
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_data_methods(app_client):
    body = app_client.get("/qmt/data/methods").json()
    assert body.get("get_market_data_ex") == "ok"
    assert "blocked" in body.get("subscribe_quote", "")


def test_data_call_blocks_subscribe(app_client):
    r = app_client.post("/qmt/data/call/subscribe_quote", json={"args": []})
    assert r.status_code == 403


def test_data_call_passthrough(app_client):
    r = app_client.post("/qmt/data/call/get_full_tick", json={"args": [["600000.SH"]]})
    assert r.status_code == 200
    assert r.json()["600000.SH"]["lastPrice"] == 10.5


def test_data_does_not_need_trading_enabled(app_client):
    # 行情不受交易总开关影响（默认 QMT_TRADING_ENABLED 未开仍可取）
    assert app_client.get("/qmt/data/tick?codes=600000.SH").status_code == 200
