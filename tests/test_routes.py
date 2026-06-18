"""集成测试：HTTP 端点（SDK 已在 conftest 桩替换）。"""


def test_health(app_client):
    r = app_client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_openapi_paths_preserved(app_client):
    paths = set(app_client.get("/openapi.json").json()["paths"].keys())
    expected = {
        "/health",
        "/em/csd", "/em/css", "/em/methods", "/em/call/{method}",
        "/ths/history", "/ths/basic", "/ths/realtime", "/ths/funcs", "/ths/call/{func}",
    }
    assert expected.issubset(paths)


def test_em_csd_returns_data(app_client):
    r = app_client.get("/em/csd", params={
        "codes": "300059.SZ", "indicators": "CLOSE",
        "startdate": "2024-01-01", "enddate": "2024-01-05",
    })
    assert r.status_code == 200


def test_em_methods_all_ok_with_labels(app_client):
    out = app_client.get("/em/methods").json()
    # 全部可调用：状态一律以 "ok" 开头，仅类别标注不同
    assert all(v.startswith("ok") for v in out.values())
    assert out["start"].startswith("ok(会话管理")     # 会话管理标注
    assert out["csq"].startswith("ok(异步")            # 异步推送标注
    assert out["porder"].startswith("ok(交易")         # 交易/组合标注
    assert out["csd"] == "ok"


def test_em_call_session_method_callable(app_client):
    # 会话管理类不再 403：start 在桩里可调用并返回成功
    r = app_client.post("/em/call/start")
    assert r.status_code == 200


def test_em_call_private_method_403(app_client):
    r = app_client.post("/em/call/__class__")
    assert r.status_code == 403


def test_em_call_unknown_method_404(app_client):
    r = app_client.post("/em/call/does_not_exist")
    assert r.status_code == 404


def test_em_call_passthrough_ok(app_client):
    r = app_client.post("/em/call/edb", json={"args": ["EMM00087117", "Ispandas=1"]})
    assert r.status_code == 200


def test_em_call_porder_passthrough(app_client):
    orderdict = {"code": ["300059.SZ"], "volume": [1000], "price": [13.11],
                 "date": ["2024-01-05"], "optype": [1]}
    r = app_client.post("/em/call/porder",
                        json={"args": ["quant001.PF", orderdict, "test"], "options_pandas": False})
    assert r.status_code == 200


def test_em_call_pquery_passthrough(app_client):
    r = app_client.post("/em/call/pquery", json={"args": [""], "options_pandas": False})
    assert r.status_code == 200


def test_em_csd_sdk_error_502(app_client, fake_em):
    from tests.conftest import FakeEmResult
    fake_em._csd_result = FakeEmResult(error_code=10001, error_msg="bad")
    r = app_client.get("/em/csd", params={
        "codes": "x", "indicators": "CLOSE",
        "startdate": "2024-01-01", "enddate": "2024-01-05",
    })
    assert r.status_code == 502
    fake_em._csd_result = FakeEmResult(data={"x": 1})  # 复位，避免影响其它用例


def test_em_call_type_error_400(app_client, monkeypatch):
    import stocksdk.routes_em as rem
    monkeypatch.setattr(rem.c, "edb", lambda *a, **k: (_ for _ in ()).throw(TypeError("wrong args")))
    r = app_client.post("/em/call/edb", json={"args": []})
    assert r.status_code == 400


def test_ths_history_ok(app_client):
    r = app_client.get("/ths/history", params={
        "codes": "300033.SZ", "indicators": "close",
        "begin": "2024-01-01", "end": "2024-01-05",
    })
    assert r.status_code == 200


def test_ths_basic_ok(app_client):
    r = app_client.get("/ths/basic", params={
        "codes": "300033.SZ", "indicators": "ths_stock_short_name_stock",
    })
    assert r.status_code == 200


def test_ths_realtime_ok(app_client):
    r = app_client.get("/ths/realtime", params={
        "codes": "300033.SZ", "indicators": "latest",
    })
    assert r.status_code == 200


def test_ths_call_passthrough_ok(app_client):
    r = app_client.post("/ths/call/EDB", json={
        "args": ["指标", "", "2024-01-01", "2024-06-01"],
    })
    assert r.status_code == 200


def test_ths_history_sdk_error_502(app_client, monkeypatch):
    import stocksdk.routes_ths as rths
    monkeypatch.setattr(rths, "THS_HistoryQuotes",
                        lambda *a, **k: {"errorcode": 99, "errmsg": "boom"})
    r = app_client.get("/ths/history", params={
        "codes": "x", "indicators": "close",
        "begin": "2024-01-01", "end": "2024-01-05",
    })
    assert r.status_code == 502


def test_ths_funcs_all_ok_with_labels(app_client):
    out = app_client.get("/ths/funcs").json()
    assert all(v.startswith("ok") for v in out.values())
    assert out.get("THS_iFinDLogin", "").startswith("ok(会话管理")


def test_ths_call_session_func_callable(app_client):
    # 会话管理类不再 403：iFinDLogin 在桩里可调用
    r = app_client.post("/ths/call/iFinDLogin", json={"args": ["u", "p"]})
    assert r.status_code == 200


def test_ths_call_unknown_404(app_client):
    r = app_client.post("/ths/call/Nope")
    assert r.status_code == 404
