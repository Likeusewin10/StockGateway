"""会话自愈测试：会话失效时 em_exec/ths_exec 应强制重登并重试一次。

复用 conftest 注入的桩 SDK；这里直接测 sessions 层的恢复逻辑。
"""
import importlib

import pytest
from fastapi import HTTPException


@pytest.fixture
def sessions(monkeypatch):
    """重载 sessions，确保 _em_ready/_ths_ready 从干净状态开始。"""
    monkeypatch.setenv("THS_USER", "test_user")
    monkeypatch.setenv("THS_PWD", "test_pwd")
    import stocksdk.sessions as s
    importlib.reload(s)
    return s


class _EmResult:
    def __init__(self, code, msg=""):
        self.ErrorCode = code
        self.ErrorMsg = msg
        self.Data = {}


# ---------- EM ----------

def test_em_exec_retries_on_session_dead(sessions, monkeypatch):
    """首次返回 10001009（登录数超限）→ 重登后重试 → 成功。"""
    calls = {"start": 0, "fn": 0}

    def fake_start(*a, **k):
        calls["start"] += 1
        return _EmResult(0)

    monkeypatch.setattr(sessions.c, "start", fake_start)

    def fn():
        calls["fn"] += 1
        return _EmResult(10001009) if calls["fn"] == 1 else _EmResult(0, "success")

    r = sessions.em_exec(fn)

    assert calls["fn"] == 2          # 重试了一次
    assert calls["start"] >= 2       # 惰性登录 + force 重登
    assert r.ErrorCode == 0          # 最终成功


def test_em_exec_no_retry_on_normal_result(sessions, monkeypatch):
    """正常结果不触发重登重试。"""
    calls = {"start": 0, "fn": 0}
    monkeypatch.setattr(sessions.c, "start",
                        lambda *a, **k: (calls.__setitem__("start", calls["start"] + 1) or _EmResult(0)))

    def fn():
        calls["fn"] += 1
        return _EmResult(0)

    sessions.em_exec(fn)
    assert calls["fn"] == 1
    assert calls["start"] == 1       # 仅惰性登录一次


def test_em_exec_raises_502_when_relogin_fails(sessions, monkeypatch):
    """会话失效且重登失败 → 抛 502。"""
    monkeypatch.setattr(sessions.c, "start", lambda *a, **k: _EmResult(10001002, "账密错误"))
    with pytest.raises(HTTPException) as ei:
        sessions.em_exec(lambda: _EmResult(10001009))
    assert ei.value.status_code == 502


# ---------- iFinD ----------

def test_ths_exec_retries_on_logged_out(sessions, monkeypatch):
    """首次返回 -1010（已登出）→ 重登后重试 → 成功。"""
    calls = {"login": 0, "logout": 0, "fn": 0}
    monkeypatch.setattr(sessions, "THS_iFinDLogin",
                        lambda u, p: (calls.__setitem__("login", calls["login"] + 1) or 0))
    monkeypatch.setattr(sessions, "THS_iFinDLogout",
                        lambda *a, **k: (calls.__setitem__("logout", calls["logout"] + 1) or 0))

    def fn():
        calls["fn"] += 1
        return {"errorcode": -1010, "errmsg": "Your account has been logged out"} if calls["fn"] == 1 \
            else {"errorcode": 0, "tables": []}

    r = sessions.ths_exec(fn)

    assert calls["fn"] == 2
    assert calls["login"] >= 2       # 惰性登录 + force 重登
    assert calls["logout"] == 1      # force 重登前先登出一次
    assert r["errorcode"] == 0


def test_ths_exec_no_retry_on_normal(sessions, monkeypatch):
    calls = {"login": 0, "fn": 0}
    monkeypatch.setattr(sessions, "THS_iFinDLogin",
                        lambda u, p: (calls.__setitem__("login", calls["login"] + 1) or 0))

    def fn():
        calls["fn"] += 1
        return {"errorcode": 0}

    sessions.ths_exec(fn)
    assert calls["fn"] == 1
    assert calls["login"] == 1


def test_ths_session_dead_keyword_fallback(sessions):
    """码集没覆盖但 errmsg 含关键词时也判失效。"""
    assert sessions._ths_session_dead({"errorcode": -9999, "errmsg": "not login"}) is True
    assert sessions._ths_session_dead({"errorcode": 0, "tables": []}) is False
