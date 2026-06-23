"""并发承载测试：N 路并发持续打目标端点，统计 p50/p95/p99 与吞吐。

默认压 /health —— 它**不持全局锁、不吃限流**，能干净地反映服务在高并发连接
下的握手/排队/调度能力，且零 SDK 配额消耗。

⚠ 架构提醒：本服务两套 SDK 单会话、单点登录，所有取数 `with lock:` 串行
（stocksdk/sessions.py）。因此压**取数端点**时，并发上升不会让取数吞吐翻倍，
延迟会随并发线性上升——这是设计预期，不是缺陷。要看真实取数排队，可用 mock
端点（见 README），别拿它的吞吐当 QPS 上限误判。

用法：
    .venv-api\\Scripts\\python loadtest\\concurrency.py --target /health \\
        --concurrency 1,4,16,64,256 --duration 15
"""
from __future__ import annotations

import argparse
import asyncio
import time

import httpx2

# 允许 `python loadtest/concurrency.py` 直接运行：把项目根放进 sys.path。
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loadtest._common import (
    Sample,
    auth_headers,
    base_url,
    default_csv_path,
    format_report,
    summarize,
    write_csv,
)


async def _worker(client: httpx2.AsyncClient, url: str, headers: dict,
                  deadline: float, samples: list[Sample]) -> None:
    """单路 worker：在 deadline 前不断发请求并采样。"""
    while time.monotonic() < deadline:
        t0 = time.monotonic()
        try:
            resp = await client.get(url, headers=headers)
            status = resp.status_code
        except Exception:
            status = None   # 连接级失败（超时/拒绝/重置）
        latency_ms = (time.monotonic() - t0) * 1000.0
        samples.append(Sample(latency_ms=latency_ms, status=status))


async def run_one(target: str, concurrency: int, duration: float,
                  host: str, port: int | None, timeout: float):
    """跑一个并发档位，返回 Report。"""
    url = base_url(host, port) + target
    headers = auth_headers()
    samples: list[Sample] = []
    limits = httpx2.Limits(max_connections=concurrency + 10,
                           max_keepalive_connections=concurrency + 10)
    async with httpx2.AsyncClient(timeout=timeout, limits=limits) as client:
        # 预热一发，触发连接建立与首登（取数端点首请求会惰性登录，避免计入分布）。
        try:
            await client.get(url, headers=headers)
        except Exception:
            pass
        wall0 = time.monotonic()
        deadline = wall0 + duration
        tasks = [
            asyncio.create_task(_worker(client, url, headers, deadline, samples))
            for _ in range(concurrency)
        ]
        await asyncio.gather(*tasks)
        wall = time.monotonic() - wall0
    return summarize(samples, duration_s=wall,
                     meta={"target": target, "concurrency": concurrency})


async def _main_async(args) -> int:
    levels = [int(x) for x in args.concurrency.split(",") if x.strip()]
    reports = []
    url = base_url(args.host, args.port) + args.target
    print("目标 {}  时长每档 {}s".format(url, args.duration))
    print("=" * 56)

    # 预检：先单发一次。失败则直接退出，避免写出「全失败」的误导性 CSV
    # （常见原因：服务没起、端口错、或 Git-Bash 把 /health 转成了 Windows 路径）。
    if not await _preflight(url):
        print("\n✗ 预检失败：目标不可达。请确认：")
        print("  1) 服务已在 {} 运行（curl 该地址应得 200）；".format(url))
        print("  2) 端口正确（默认取 config.DEFAULT_PORT）；")
        print("  3) 若用 Git-Bash，路径被转义——改用 cmd 运行，或设 "
              "MSYS_NO_PATHCONV=1。")
        return 2

    for c in levels:
        rep = await run_one(args.target, c, args.duration,
                            args.host, args.port, args.timeout)
        print("\n[并发 {}]".format(c))
        print(format_report(rep))
        reports.append(rep)

    out = default_csv_path(args.out)
    write_csv(out, reports)
    print("\nCSV 已落盘：{}".format(out))

    _print_verdict(args.target, reports)
    return 0


async def _preflight(url: str) -> bool:
    """单发一次确认目标可达（2xx/3xx 即可，429 也算可达）。"""
    try:
        async with httpx2.AsyncClient(timeout=5) as client:
            resp = await client.get(url, headers=auth_headers())
            return resp.status_code < 500
    except Exception:
        return False


def _print_verdict(target: str, reports: list) -> None:
    """对结果给出一句话判读，把『串行预期』与『真异常』分开。"""
    print("\n判读：")
    server_errs = sum(r.server_error for r in reports)
    failed = sum(r.failed for r in reports)
    if server_errs or failed:
        print("  ✗ 出现 {} 个 5xx、{} 个连接失败 —— 需排查（非预期）。".format(
            server_errs, failed))
    else:
        print("  ✓ 全程无 5xx、无连接失败。")
    if target.rstrip("/") in ("/health", ""):
        # /health 不持锁：吞吐应随并发上升
        if len(reports) >= 2 and reports[-1].throughput_rps > reports[0].throughput_rps:
            print("  ✓ /health 吞吐随并发上升：连接调度正常。")
        print("  ℹ /health 反映的是连接处理能力；取数端点受全局锁串行，"
              "另测见 README。")
    else:
        print("  ℹ 取数端点受全局锁串行：吞吐趋平、延迟随并发上升属设计预期，"
              "不是缺陷。")


def main() -> int:
    p = argparse.ArgumentParser(description="并发承载测试（默认压 /health）")
    p.add_argument("--target", default="/health", help="被压路径，默认 /health")
    p.add_argument("--concurrency", default="1,4,16,64",
                   help="并发档位，逗号分隔。默认 1,4,16,64")
    p.add_argument("--duration", type=float, default=15.0, help="每档秒数")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=None, help="默认取 config.DEFAULT_PORT")
    p.add_argument("--timeout", type=float, default=10.0, help="单请求超时秒")
    p.add_argument("--out", default="concurrency.csv", help="结果 CSV 文件名")
    args = p.parse_args()
    return asyncio.run(_main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
