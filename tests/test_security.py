"""单元测试：security（鉴权、限流）。"""
import pytest
from fastapi import HTTPException

from stocksdk import security
from stocksdk.security import RateLimiter


def test_keys_match_constant_time():
    assert security._keys_match("abc", "abc") is True
    assert security._keys_match("abc", "abd") is False
    assert security._keys_match("", "abc") is False


def test_require_key_no_config_skips(monkeypatch):
    monkeypatch.setenv("API_KEY", "")
    # 不配置 key 时任意输入都放行（返回 None 不抛异常）
    assert security.require_key(None) is None


def test_require_key_correct(monkeypatch):
    monkeypatch.setenv("API_KEY", "secret")
    assert security.require_key("secret") is None


def test_require_key_wrong_raises_401(monkeypatch):
    monkeypatch.setenv("API_KEY", "secret")
    with pytest.raises(HTTPException) as exc:
        security.require_key("wrong")
    assert exc.value.status_code == 401


def test_require_key_missing_raises_401(monkeypatch):
    monkeypatch.setenv("API_KEY", "secret")
    with pytest.raises(HTTPException) as exc:
        security.require_key(None)
    assert exc.value.status_code == 401


def test_rate_limiter_allows_under_limit():
    rl = RateLimiter(max_requests=3, window_seconds=60)
    assert all(rl.check("ip1") for _ in range(3))


def test_rate_limiter_blocks_over_limit():
    rl = RateLimiter(max_requests=2, window_seconds=60)
    assert rl.check("ip1") is True
    assert rl.check("ip1") is True
    assert rl.check("ip1") is False


def test_rate_limiter_isolates_by_ip():
    rl = RateLimiter(max_requests=1, window_seconds=60)
    assert rl.check("ip1") is True
    assert rl.check("ip2") is True   # 不同 IP 独立计数
    assert rl.check("ip1") is False


def test_rate_limiter_window_expiry(monkeypatch):
    rl = RateLimiter(max_requests=1, window_seconds=10)
    times = iter([100.0, 100.0, 115.0])  # 第三次已过窗口
    monkeypatch.setattr(security.time, "monotonic", lambda: next(times))
    assert rl.check("ip1") is True
    assert rl.check("ip1") is False
    assert rl.check("ip1") is True


class _FakeWS:
    def __init__(self, key=None):
        self.query_params = {"key": key} if key is not None else {}


def test_ws_authed_no_config(monkeypatch):
    monkeypatch.setenv("API_KEY", "")
    assert security.ws_authed(_FakeWS()) is True


def test_ws_authed_correct_key(monkeypatch):
    monkeypatch.setenv("API_KEY", "k")
    assert security.ws_authed(_FakeWS("k")) is True


def test_ws_authed_wrong_key(monkeypatch):
    monkeypatch.setenv("API_KEY", "k")
    assert security.ws_authed(_FakeWS("nope")) is False
    assert security.ws_authed(_FakeWS()) is False
