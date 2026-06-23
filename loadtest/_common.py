"""压测工具共享原语：配置读取、延迟统计、错误分类、CSV 落盘。

设计原则：
- 统计/解析全部为**纯函数**，可在无服务、无网络下单测（见 tests/test_loadtest_harness.py）。
- 端口/限流阈值一律从 stocksdk.config 读，绝不在压测脚本里写死，避免与生产配置漂移。
- 仅依赖标准库；HTTP 客户端由各脚本自带（httpx2），本模块不碰网络。
"""
from __future__ import annotations

import csv
import math
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

# 让 loadtest/ 下的脚本能 import stocksdk.*（项目根在本文件父目录的父目录）。
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from stocksdk.config import (  # noqa: E402
    DEFAULT_PORT,
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
    WS_QUEUE_MAXSIZE,
    get_api_key,
    load_dotenv,
)

# 压测脚本启动时也走同一份 .env 加载，拿到 API_KEY / 限流常量。
load_dotenv()


def _force_utf8_stdio() -> None:
    """Windows 控制台默认 GBK，输出 ✓/✗/ℹ 等符号会 UnicodeEncodeError。

    所有压测脚本都 import 本模块，故在此统一把 stdout/stderr 切到 UTF-8，
    一处修复全部脚本。Python 3.7+ 的 reconfigure 可用；失败则静默退回。
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_force_utf8_stdio()

# 429 占比超过此阈值 → 判定「测到的是限流而非承载」，脚本应告警。
RATE_LIMITED_WARN_RATIO = 0.05


def base_url(host: str = "127.0.0.1", port: int | None = None) -> str:
    """REST 服务基址。端口默认取 config.DEFAULT_PORT，不写死。"""
    return "http://{}:{}".format(host, port or DEFAULT_PORT)


def ws_url(path: str, host: str = "127.0.0.1", port: int | None = None,
           key: str | None = None) -> str:
    """WebSocket 地址；若服务配了 API_KEY，自动补 ?key=（WS 走 query 鉴权）。"""
    url = "ws://{}:{}{}".format(host, port or DEFAULT_PORT, path)
    api_key = key if key is not None else get_api_key()
    if api_key:
        sep = "&" if "?" in url else "?"
        url = "{}{}key={}".format(url, sep, api_key)
    return url


def auth_headers(key: str | None = None) -> dict[str, str]:
    """REST 鉴权头；未配置 key 时返回空 dict。"""
    api_key = key if key is not None else get_api_key()
    return {"X-API-Key": api_key} if api_key else {}


def percentile(sorted_values: list[float], pct: float) -> float:
    """有序列表的百分位（线性插值）。pct 取 0..100。空列表返回 0.0。

    纯函数，便于单测。输入必须已升序排序。
    """
    if not sorted_values:
        return 0.0
    if pct <= 0:
        return sorted_values[0]
    if pct >= 100:
        return sorted_values[-1]
    rank = (pct / 100.0) * (len(sorted_values) - 1)
    low = math.floor(rank)
    high = math.ceil(rank)
    if low == high:
        return sorted_values[int(rank)]
    frac = rank - low
    return sorted_values[low] * (1 - frac) + sorted_values[high] * frac


def classify_status(status: int | None) -> str:
    """把一次请求结果归到四类之一：ok / rate_limited / server_error / failed。

    status=None 表示连接级失败（超时/拒绝/异常）。
    """
    if status is None:
        return "failed"
    if status == 429:
        return "rate_limited"
    if status >= 500:
        return "server_error"
    if 200 <= status < 400:
        return "ok"
    return "failed"   # 4xx（非 429）也算失败：鉴权错/参数错等


@dataclass
class Sample:
    """单次请求采样：耗时（毫秒）+ HTTP 状态（None=连接失败）。"""
    latency_ms: float
    status: int | None


@dataclass
class Report:
    """一轮压测的聚合结果。由 summarize() 产出，可直接打印 / 落 CSV。"""
    total: int
    ok: int
    rate_limited: int
    server_error: int
    failed: int
    duration_s: float
    throughput_rps: float
    p50_ms: float
    p95_ms: float
    p99_ms: float
    max_ms: float
    meta: dict = field(default_factory=dict)

    @property
    def rate_limited_ratio(self) -> float:
        return self.rate_limited / self.total if self.total else 0.0

    @property
    def is_rate_limit_dominated(self) -> bool:
        """429 占比过高 → 测到的是限流，不是真实承载。"""
        return self.rate_limited_ratio > RATE_LIMITED_WARN_RATIO


def summarize(samples: list[Sample], duration_s: float,
              meta: dict | None = None) -> Report:
    """把采样列表聚合为 Report。纯函数：不碰网络、不读时钟。

    duration_s 为本轮实际墙钟耗时，用于算吞吐。
    """
    counts = {"ok": 0, "rate_limited": 0, "server_error": 0, "failed": 0}
    latencies: list[float] = []
    for s in samples:
        counts[classify_status(s.status)] += 1
        # 仅成功请求计入延迟分布，避免超时/拒绝把分位数污染成假高/假低。
        if classify_status(s.status) == "ok":
            latencies.append(s.latency_ms)
    latencies.sort()
    total = len(samples)
    throughput = (total / duration_s) if duration_s > 0 else 0.0
    return Report(
        total=total,
        ok=counts["ok"],
        rate_limited=counts["rate_limited"],
        server_error=counts["server_error"],
        failed=counts["failed"],
        duration_s=duration_s,
        throughput_rps=throughput,
        p50_ms=percentile(latencies, 50),
        p95_ms=percentile(latencies, 95),
        p99_ms=percentile(latencies, 99),
        max_ms=latencies[-1] if latencies else 0.0,
        meta=meta or {},
    )


def format_report(report: Report) -> str:
    """把 Report 渲染为人读文本块。"""
    lines = [
        "总请求       : {}".format(report.total),
        "成功 / 限流  : {} / {}".format(report.ok, report.rate_limited),
        "5xx / 失败   : {} / {}".format(report.server_error, report.failed),
        "耗时         : {:.1f}s".format(report.duration_s),
        "吞吐         : {:.1f} req/s".format(report.throughput_rps),
        "p50 / p95    : {:.1f} / {:.1f} ms".format(report.p50_ms, report.p95_ms),
        "p99 / max    : {:.1f} / {:.1f} ms".format(report.p99_ms, report.max_ms),
    ]
    if report.is_rate_limit_dominated:
        lines.append(
            "⚠ 429 占比 {:.0%} 偏高：当前每 IP 限流 {}/{}s，"
            "你测到的是『限流』而非『承载』。改压 /health 或临时调高 "
            "RATE_LIMIT_REQUESTS。".format(
                report.rate_limited_ratio, RATE_LIMIT_REQUESTS,
                RATE_LIMIT_WINDOW_SECONDS,
            )
        )
    return "\n".join(lines)


def write_csv(path: str | Path, reports: list[Report]) -> None:
    """把多轮 Report 落成一张 CSV（每行一轮）。meta 里的键平铺成列。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    meta_keys: list[str] = []
    for r in reports:
        for k in r.meta:
            if k not in meta_keys:
                meta_keys.append(k)
    fields = [
        "total", "ok", "rate_limited", "server_error", "failed",
        "duration_s", "throughput_rps", "p50_ms", "p95_ms", "p99_ms", "max_ms",
    ] + meta_keys
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(fields)
        for r in reports:
            row = [
                r.total, r.ok, r.rate_limited, r.server_error, r.failed,
                "{:.3f}".format(r.duration_s),
                "{:.2f}".format(r.throughput_rps),
                "{:.2f}".format(r.p50_ms), "{:.2f}".format(r.p95_ms),
                "{:.2f}".format(r.p99_ms), "{:.2f}".format(r.max_ms),
            ] + [r.meta.get(k, "") for k in meta_keys]
            writer.writerow(row)


def default_csv_path(name: str) -> Path:
    """压测结果默认落盘到 loadtest/results/<name>.csv。"""
    return Path(__file__).resolve().parent / "results" / name


def pids_listening_rss(port: int) -> int | None:
    """监听指定端口的进程 RSS（字节）之和；无 psutil 或找不到时返回 None。

    供 ws_soak.py 观测服务内存漂移。按端口精确定位，不按进程名。
    """
    try:
        import psutil
    except ImportError:
        return None
    total = 0
    found = False
    for conn in psutil.net_connections(kind="inet"):
        if (conn.laddr and conn.laddr.port == port
                and conn.status == psutil.CONN_LISTEN and conn.pid):
            try:
                total += psutil.Process(conn.pid).memory_info().rss
                found = True
            except Exception:
                pass
    return total if found else None


# 重新导出常量，供脚本判读阈值时引用（避免各脚本再 import config）。
__all__ = [
    "DEFAULT_PORT", "RATE_LIMIT_REQUESTS", "RATE_LIMIT_WINDOW_SECONDS",
    "WS_QUEUE_MAXSIZE", "RATE_LIMITED_WARN_RATIO",
    "base_url", "ws_url", "auth_headers",
    "percentile", "classify_status", "summarize", "format_report",
    "write_csv", "default_csv_path", "Sample", "Report",
    "pids_listening_rss",
]
