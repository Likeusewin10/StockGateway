"""集成测试：/health/deep 深度健康端点（SDK 已在 conftest 桩替换）。"""


def test_health_deep_both_ok(app_client):
    r = app_client.get("/health/deep")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["ifind"]["status"] == "ok"
    assert body["em"]["status"] == "ok"
    assert "latency_ms" in body["ifind"]
    assert "latency_ms" in body["em"]
    assert "as_of" in body


def test_health_deep_ths_error_marks_down_not_500(app_client, monkeypatch):
    import stocksdk.routes_health as rh
    monkeypatch.setattr(rh, "THS_RealtimeQuotes",
                        lambda *a, **k: {"errorcode": 99, "errmsg": "boom"})
    r = app_client.get("/health/deep")
    assert r.status_code == 200          # 故障源不外抛 5xx
    body = r.json()
    assert body["status"] == "degraded"
    assert body["ifind"]["status"] == "down"
    assert "errorcode=99" in body["ifind"]["reason"]
    assert body["em"]["status"] == "ok"


def test_health_deep_em_exception_marks_down_not_500(app_client, monkeypatch):
    import stocksdk.routes_health as rh
    monkeypatch.setattr(rh.c, "css",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("sdk crash")))
    r = app_client.get("/health/deep")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "degraded"
    assert body["em"]["status"] == "down"
    assert "RuntimeError" in body["em"]["reason"]


def test_health_deep_reason_sanitized_truncated(app_client, monkeypatch):
    import stocksdk.routes_health as rh
    long_secret = "token=" + "A" * 500
    monkeypatch.setattr(rh.c, "css",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError(long_secret)))
    r = app_client.get("/health/deep")
    body = r.json()
    # 截断到上限 + 省略号，不整串回吐长字符串
    assert len(body["em"]["reason"]) <= rh._MAX_REASON_LEN + 1
    assert "A" * 500 not in body["em"]["reason"]


def test_health_deep_in_openapi(app_client):
    paths = set(app_client.get("/openapi.json").json()["paths"].keys())
    assert "/health/deep" in paths
