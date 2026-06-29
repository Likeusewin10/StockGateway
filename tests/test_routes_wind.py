"""集成 + 单元测试:Wind /wind/* 路由、wind_result 归一化、会话自愈。

SDK 已在 conftest 桩替换(FakeWindClient),不触发真实登录/网络。
"""
import importlib

import pandas as pd
import pytest
from fastapi import HTTPException

from stocksdk import serialize


# ---------- 路由(集成) ----------

def test_wind_paths_in_openapi(app_client):
    paths = set(app_client.get("/openapi.json").json()["paths"].keys())
    expected = {"/wind/wsd", "/wind/wss", "/wind/methods", "/wind/call/{method}"}
    assert expected.issubset(paths)


def test_wind_wsd_returns_records(app_client):
    r = app_client.get("/wind/wsd", params={
        "codes": "600030.SH", "fields": "close",
        "startdate": "2024-01-01", "enddate": "2024-01-05",
    })
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list) and body and "close" in body[0]


def test_wind_wss_returns_records(app_client):
    r = app_client.get("/wind/wss", params={
        "codes": "600030.SH", "fields": "sec_name", "options": "tradeDate=20240105",
    })
    assert r.status_code == 200


def test_wind_methods_labels(app_client):
    out = app_client.get("/wind/methods").json()
    assert out["wsd"] == "ok"
    assert out["start"].startswith("ok(会话管理")
    assert out["wsq"].startswith("ok(异步")
    assert out["torder"].startswith("blocked(交易")   # 交易类标注为已拦截


def test_wind_call_passthrough_ok(app_client):
    r = app_client.post("/wind/call/edb", json={"args": ["M0017126", "2024-01-01", "2024-06-01"]})
    assert r.status_code == 200


def test_wind_call_trading_blocked_403(app_client):
    r = app_client.post("/wind/call/torder", json={"args": []})
    assert r.status_code == 403


def test_wind_call_private_403(app_client):
    r = app_client.post("/wind/call/__class__")
    assert r.status_code == 403


def test_wind_call_unknown_404(app_client):
    r = app_client.post("/wind/call/does_not_exist")
    assert r.status_code == 404


def test_wind_call_typeerror_retry_without_usedf(app_client):
    # tdays 桩不接受 usedf 关键字 → 路由应退回不带 usedf 重试,仍 200
    r = app_client.post("/wind/call/tdays", json={"args": ["2024-01-01", "2024-01-05"]})
    assert r.status_code == 200


# ---------- wind_result(单元) ----------

def _wd(error_code=0, codes=None, fields=None, times=None, data=None):
    class _WD:
        ErrorCode = error_code
        Codes = codes if codes is not None else []
        Fields = fields if fields is not None else []
        Times = times if times is not None else []
        Data = data if data is not None else []
    return _WD()


def test_wind_result_usedf_tuple_to_records():
    df = pd.DataFrame({"close": [1.0]}, index=["2024-01-05"])
    out = serialize.wind_result((0, df))
    assert out == [{"index": "2024-01-05", "close": 1.0}]


def test_wind_result_usedf_error_raises_502():
    with pytest.raises(HTTPException) as ei:
        serialize.wind_result((-40520004, None))
    assert ei.value.status_code == 502


def test_wind_result_winddata_structured():
    out = serialize.wind_result(_wd(codes=["600030.SH"], fields=["close"],
                                    times=["2024-01-05"], data=[[1.0]]))
    assert out == {"Codes": ["600030.SH"], "Fields": ["close"],
                   "Times": ["2024-01-05"], "Data": [[1.0]]}


def test_wind_result_winddata_error_raises_502():
    with pytest.raises(HTTPException) as ei:
        serialize.wind_result(_wd(error_code=-2))
    assert ei.value.status_code == 502


def test_wind_result_bad_code_zero_errorcode_passes():
    # 坏证券码:ErrorCode=0 + Data=[[None]] → 仍按正常数据返回,不报错
    out = serialize.wind_result(_wd(data=[[None]]))
    assert out["Data"] == [[None]]


# ---------- 会话自愈(单元) ----------

@pytest.fixture
def sessions(monkeypatch):
    import stocksdk.sessions as s
    importlib.reload(s)
    return s


class _R:
    def __init__(self, code, data=""):
        self.ErrorCode = code
        self.Data = data


def test_ensure_wind_success(sessions, monkeypatch):
    monkeypatch.setattr(sessions.w, "start", lambda *a, **k: _R(0, ["OK!"]))
    monkeypatch.setattr(sessions.w, "isconnected", lambda: True)
    sessions.ensure_wind()   # 不抛即通过


def test_ensure_wind_failure_raises_502(sessions, monkeypatch):
    monkeypatch.setattr(sessions.w, "start", lambda *a, **k: _R(-40520004))
    monkeypatch.setattr(sessions.w, "isconnected", lambda: False)
    with pytest.raises(HTTPException) as ei:
        sessions.ensure_wind()
    assert ei.value.status_code == 502


def test_wind_exec_retries_on_session_dead(sessions, monkeypatch):
    calls = {"start": 0, "fn": 0}
    monkeypatch.setattr(sessions.w, "isconnected", lambda: True)

    def fake_start(*a, **k):
        calls["start"] += 1
        return _R(0)

    monkeypatch.setattr(sessions.w, "start", fake_start)
    monkeypatch.setattr(sessions.w, "stop", lambda *a, **k: None)

    def fn():
        calls["fn"] += 1
        return _R(-103) if calls["fn"] == 1 else _R(0, "ok")

    r = sessions.wind_exec(fn)
    assert calls["fn"] == 2          # 重试了一次
    assert calls["start"] >= 2       # 惰性登录 + force 重登
    assert r.ErrorCode == 0


def test_wind_exec_no_retry_on_normal(sessions, monkeypatch):
    calls = {"start": 0, "fn": 0}
    monkeypatch.setattr(sessions.w, "isconnected", lambda: True)
    monkeypatch.setattr(sessions.w, "start",
                        lambda *a, **k: (calls.__setitem__("start", calls["start"] + 1) or _R(0)))

    def fn():
        calls["fn"] += 1
        return _R(0)

    sessions.wind_exec(fn)
    assert calls["fn"] == 1
    assert calls["start"] == 1


def test_wind_exec_retries_on_session_dead_tuple(sessions, monkeypatch):
    """usedf=True 路径返回 (-103, None) 元组时也应判失效并重试一次(wsd/wss 走此路)。"""
    calls = {"start": 0, "fn": 0}
    monkeypatch.setattr(sessions.w, "isconnected", lambda: True)
    monkeypatch.setattr(sessions.w, "start",
                        lambda *a, **k: (calls.__setitem__("start", calls["start"] + 1) or _R(0)))
    monkeypatch.setattr(sessions.w, "stop", lambda *a, **k: None)

    def fn():
        calls["fn"] += 1
        return (-103, None) if calls["fn"] == 1 else (0, "df")

    r = sessions.wind_exec(fn)
    assert calls["fn"] == 2
    assert calls["start"] >= 2
    assert r == (0, "df")


def test_wind_session_dead_detection(sessions):
    assert sessions._wind_session_dead(_R(-2)) is True
    assert sessions._wind_session_dead(_R(-40520004)) is True
    assert sessions._wind_session_dead(_R(0)) is False
    # 坏证券码 ErrorCode=0 不判失效
    assert sessions._wind_session_dead(_R(0, [[None]])) is False
    # usedf=True 元组路径
    assert sessions._wind_session_dead((-103, None)) is True
    assert sessions._wind_session_dead((0, "df")) is False
