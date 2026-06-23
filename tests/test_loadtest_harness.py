"""压测工具纯函数单测：统计/分类/CSV 不依赖服务、网络、时钟，必须可信。

这些函数是三类压测脚本结果判读的基础，若它们算错，整套测试结论都不可信，
故优先用单测锁死行为。
"""
import sys
from pathlib import Path

import pytest

# loadtest 不是包，按路径加入 sys.path 后直接 import 模块。
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from loadtest import _common as lc  # noqa: E402


# ---- percentile ----

def test_percentile_empty_returns_zero():
    assert lc.percentile([], 95) == 0.0


def test_percentile_single_value():
    assert lc.percentile([42.0], 50) == 42.0
    assert lc.percentile([42.0], 99) == 42.0


def test_percentile_p50_is_median_interpolated():
    # 升序 [10,20,30,40]，rank=1.5 → 20 与 30 中点 = 25
    assert lc.percentile([10.0, 20.0, 30.0, 40.0], 50) == 25.0


def test_percentile_p100_is_max_and_p0_is_min():
    vals = [1.0, 5.0, 9.0]
    assert lc.percentile(vals, 100) == 9.0
    assert lc.percentile(vals, 0) == 1.0


def test_percentile_p95_interpolates():
    vals = [float(i) for i in range(1, 101)]  # 1..100
    # rank = 0.95*99 = 94.05 → 介于 index94(=95.0) 与 index95(=96.0)
    result = lc.percentile(vals, 95)
    assert 95.0 <= result <= 96.0


# ---- classify_status ----

@pytest.mark.parametrize("status,expected", [
    (200, "ok"),
    (204, "ok"),
    (301, "ok"),       # <400 视为成功响应
    (429, "rate_limited"),
    (500, "server_error"),
    (503, "server_error"),
    (401, "failed"),   # 鉴权失败算 failed
    (404, "failed"),
    (None, "failed"),  # 连接级失败
])
def test_classify_status(status, expected):
    assert lc.classify_status(status) == expected


# ---- summarize ----

def test_summarize_counts_each_class():
    samples = [
        lc.Sample(10.0, 200),
        lc.Sample(20.0, 200),
        lc.Sample(0.0, 429),
        lc.Sample(0.0, 500),
        lc.Sample(0.0, None),
    ]
    rep = lc.summarize(samples, duration_s=2.0)
    assert rep.total == 5
    assert rep.ok == 2
    assert rep.rate_limited == 1
    assert rep.server_error == 1
    assert rep.failed == 1


def test_summarize_throughput():
    samples = [lc.Sample(1.0, 200) for _ in range(100)]
    rep = lc.summarize(samples, duration_s=5.0)
    assert rep.throughput_rps == pytest.approx(20.0)


def test_summarize_zero_duration_no_divzero():
    rep = lc.summarize([lc.Sample(1.0, 200)], duration_s=0.0)
    assert rep.throughput_rps == 0.0


def test_summarize_latency_only_counts_ok():
    # 失败/限流不计入延迟分布，避免污染分位数
    samples = [
        lc.Sample(10.0, 200),
        lc.Sample(99999.0, None),   # 超时——不应进 p99
        lc.Sample(20.0, 200),
    ]
    rep = lc.summarize(samples, duration_s=1.0)
    assert rep.max_ms == 20.0
    assert rep.p99_ms <= 20.0


def test_summarize_empty():
    rep = lc.summarize([], duration_s=1.0)
    assert rep.total == 0
    assert rep.p50_ms == 0.0
    assert rep.throughput_rps == 0.0


# ---- 限流主导判定 ----

def test_rate_limit_dominated_flag():
    # 100 个请求里 20 个 429 → 20% > 5% 阈值
    samples = [lc.Sample(1.0, 200) for _ in range(80)]
    samples += [lc.Sample(0.0, 429) for _ in range(20)]
    rep = lc.summarize(samples, duration_s=1.0)
    assert rep.is_rate_limit_dominated is True
    assert "限流" in lc.format_report(rep)


def test_not_rate_limit_dominated_when_below_threshold():
    samples = [lc.Sample(1.0, 200) for _ in range(99)]
    samples += [lc.Sample(0.0, 429)]
    rep = lc.summarize(samples, duration_s=1.0)
    assert rep.is_rate_limit_dominated is False


# ---- CSV 落盘 ----

def test_write_csv_roundtrip(tmp_path):
    reports = [
        lc.summarize([lc.Sample(5.0, 200)], duration_s=1.0,
                     meta={"concurrency": 4}),
        lc.summarize([lc.Sample(7.0, 200)], duration_s=1.0,
                     meta={"concurrency": 16}),
    ]
    out = tmp_path / "r.csv"
    lc.write_csv(out, reports)
    text = out.read_text(encoding="utf-8")
    assert "throughput_rps" in text
    assert "concurrency" in text
    # 两行数据 + 一行表头
    assert len(text.strip().splitlines()) == 3


# ---- URL / 鉴权头构造 ----

def test_ws_url_appends_key(monkeypatch):
    monkeypatch.setattr(lc, "get_api_key", lambda: "")
    url = lc.ws_url("/em/ws", key="secret")
    assert url.endswith("?key=secret")
    assert url.startswith("ws://")


def test_ws_url_no_key_when_empty(monkeypatch):
    url = lc.ws_url("/em/ws", key="")
    assert "key=" not in url


def test_auth_headers_present_and_absent():
    assert lc.auth_headers("abc") == {"X-API-Key": "abc"}
    assert lc.auth_headers("") == {}


def test_base_url_uses_config_port():
    assert lc.base_url(port=1234) == "http://127.0.0.1:1234"
    # 默认端口来自 config，不写死
    assert str(lc.DEFAULT_PORT) in lc.base_url()
