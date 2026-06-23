"""WebSocket 长稳 / 背压测试：开 M 路实时订阅连接，跑若干分钟，观测稳定性。

关注点（对照 routes_ws.py / config.WS_QUEUE_MAXSIZE）：
  - 连接是否能稳定保持、断连后能否说明原因；
  - 推送收包速率；
  - 是否触发每连接 1000 条的队列上限（背压）；
  - 服务进程 RSS 是否随时间单调上涨（订阅泄漏 / 内存漂移）。

注意：EM 行情订阅（csq）可能因账号无该权限而返回 error 事件——此时「订阅失败」
不算本测试的崩溃，连接保持存活才是主信号。iFinD 端（/ths/ws）通常可推送。

用法：
    .venv-api\\Scripts\\python loadtest\\ws_soak.py --path /ths/ws \\
        --codes 300033.SZ --indicators latest --connections 16 --duration 180
"""
from __future__ import annotations

import argparse
import asyncio
import json
import time

import websockets

# 允许 `python loadtest/ws_soak.py` 直接运行：把项目根放进 sys.path。
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loadtest._common import (
    DEFAULT_PORT,
    WS_QUEUE_MAXSIZE,
    pids_listening_rss,
    ws_url,
)


class ConnStat:
    """单连接累计统计。"""
    def __init__(self) -> None:
        self.recv = 0
        self.errors = 0
        self.subscribed = False
        self.closed_reason: str | None = None


async def _one_conn(idx: int, path: str, codes: str, indicators: str,
                    deadline: float, host: str, port: int) -> ConnStat:
    stat = ConnStat()
    url = ws_url(path, host=host, port=port)
    try:
        async with websockets.connect(url, open_timeout=10,
                                      max_queue=WS_QUEUE_MAXSIZE) as ws:
            await ws.send(json.dumps({
                "action": "subscribe", "codes": codes, "indicators": indicators,
            }))
            while time.monotonic() < deadline:
                remaining = deadline - time.monotonic()
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=min(remaining, 5))
                except asyncio.TimeoutError:
                    continue   # 没数据不算错，继续等（行情非交易时段可能静默）
                stat.recv += 1
                try:
                    msg = json.loads(raw)
                except Exception:
                    continue
                event = msg.get("event")
                if event == "subscribed":
                    stat.subscribed = True
                elif event == "error":
                    stat.errors += 1
    except Exception as e:
        stat.closed_reason = "{}: {}".format(type(e).__name__, e)
    return stat


async def _sample_rss(port: int, deadline: float, samples: list[int]) -> None:
    """每 5s 采一次服务进程 RSS（字节），用于看内存漂移。"""
    while time.monotonic() < deadline:
        rss = pids_listening_rss(port)
        if rss is not None:
            samples.append(rss)
        await asyncio.sleep(5)


async def _main_async(args) -> int:
    port = args.port or DEFAULT_PORT
    print("WS 长稳：{} 路 → {}  时长 {}s".format(
        args.connections, ws_url(args.path, port=port).split("?")[0], args.duration))
    print("订阅 codes={} indicators={}".format(args.codes, args.indicators))
    print("=" * 56)

    deadline = time.monotonic() + args.duration
    rss_samples: list[int] = []
    rss_task = asyncio.create_task(_sample_rss(port, deadline, rss_samples))

    conns = [
        _one_conn(i, args.path, args.codes, args.indicators, deadline,
                  args.host, port)
        for i in range(args.connections)
    ]
    stats = await asyncio.gather(*conns)
    rss_task.cancel()

    _report(stats, rss_samples)
    return 0


def _report(stats: list[ConnStat], rss_samples: list[int]) -> None:
    total_recv = sum(s.recv for s in stats)
    subscribed = sum(1 for s in stats if s.subscribed)
    errored = sum(1 for s in stats if s.errors)
    dropped = [s for s in stats if s.closed_reason]

    print("\n结果：")
    print("  连接数         : {}".format(len(stats)))
    print("  订阅成功连接   : {}".format(subscribed))
    print("  收到推送总数   : {}".format(total_recv))
    print("  含 error 事件  : {} 连接".format(errored))
    print("  异常断开       : {} 连接".format(len(dropped)))
    for s in dropped[:5]:
        print("      - {}".format(s.closed_reason))

    if rss_samples:
        lo, hi = min(rss_samples), max(rss_samples)
        drift = (hi - lo) / (1024 * 1024)
        print("  服务 RSS       : {:.0f} → {:.0f} MiB（漂移 {:.1f} MiB，{} 次采样）".format(
            lo / 1048576, hi / 1048576, drift, len(rss_samples)))

    print("\n判读：")
    if dropped:
        print("  ✗ 有连接异常断开 —— 需排查（非交易时段静默不算）。")
    else:
        print("  ✓ 无连接异常断开：长连接稳定。")
    if subscribed == 0:
        print("  ℹ 无订阅成功：若是 EM(/em/ws) 多为账号无 csq 行情权限，属已知；"
              "换 /ths/ws 验证推送链路。")
    if rss_samples and (max(rss_samples) - min(rss_samples)) > 100 * 1048576:
        print("  ⚠ RSS 漂移 >100 MiB：留意订阅泄漏 / 队列堆积。")


def main() -> int:
    p = argparse.ArgumentParser(description="WebSocket 长稳 / 背压测试")
    p.add_argument("--path", default="/ths/ws", help="/em/ws 或 /ths/ws，默认 /ths/ws")
    p.add_argument("--codes", default="300033.SZ", help="订阅代码")
    p.add_argument("--indicators", default="latest", help="订阅指标")
    p.add_argument("--connections", type=int, default=16, help="并发连接数")
    p.add_argument("--duration", type=float, default=180.0, help="持续秒数")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=None)
    args = p.parse_args()
    return asyncio.run(_main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
