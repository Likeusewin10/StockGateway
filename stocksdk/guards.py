"""下单护栏：在 /qmt/order、/tdx/order 真正发单前做多重硬性校验。

四道护栏（配置由各交易源自行传入，默认从严）：
1. 交易总开关（如 QMT_TRADING_ENABLED / TDX_TRADING_ENABLED，默认关）——由路由层先判，这里不重复。
2. 单笔金额上限 max_notional（volume×price）。
3. 标的白名单 whitelist（留空=不限）。
4. 当日累计下单笔数 daily_cap。
另含交易时段校验（A 股 09:30–11:30 / 13:00–15:00），非时段拒单（除非 allow_offhours）。

护栏本身不读环境变量：QMT 与 TDX 是两个独立券商腿，配置各自独立，由调用方（路由）
读好自己的配置后传入。当日计数按 source 分桶（"qmt"/"tdx" 互不干扰）。
单 worker 部署下进程内计数足够，重启即重置。
"""
import datetime
import threading

from fastapi import HTTPException

# A 股连续竞价时段（含集合竞价边界，简化为 09:30–11:30 / 13:00–15:00）。
_MORNING = (datetime.time(9, 30), datetime.time(11, 30))
_AFTERNOON = (datetime.time(13, 0), datetime.time(15, 0))

_lock = threading.Lock()
_daily_count: dict[str, dict[str, int]] = {}   # {source: {YYYY-MM-DD: 已下单笔数}}


def _today_key(now: datetime.datetime) -> str:
    return now.strftime("%Y-%m-%d")


def _in_trading_hours(now: datetime.datetime) -> bool:
    t = now.time()
    if now.weekday() >= 5:   # 周六日
        return False
    return (_MORNING[0] <= t <= _MORNING[1]) or (_AFTERNOON[0] <= t <= _AFTERNOON[1])


def current_daily_count(source: str, now: datetime.datetime | None = None) -> int:
    """指定交易源当日已下单笔数（供 dry-run 预览 / 监控）。"""
    now = now or datetime.datetime.now()
    with _lock:
        return _daily_count.get(source, {}).get(_today_key(now), 0)


def enforce(source: str, stock_code: str, volume: int, price: float, *,
            max_notional: float, daily_cap: int, whitelist: list[str],
            allow_offhours: bool, now: datetime.datetime | None = None) -> None:
    """逐条校验，违反任一即抛 HTTPException(409)。不修改计数（仅检查）。

    配置项由调用方按自己的交易源传入（QMT/TDX 各自独立）。
    """
    now = now or datetime.datetime.now()

    if volume is None or volume <= 0:
        raise HTTPException(409, "护栏拒单[volume]：委托数量必须为正，got {}".format(volume))

    if whitelist and stock_code not in whitelist:
        raise HTTPException(409, "护栏拒单[whitelist]：{} 不在白名单".format(stock_code))

    # 金额护栏：限价单按 price 估算；市价单（price<=0）无法预估金额，跳过金额校验。
    if price and price > 0:
        notional = volume * price
        if notional > max_notional:
            raise HTTPException(
                409, "护栏拒单[max_notional]：单笔 {:.2f} 超上限 {:.2f}".format(notional, max_notional))

    if current_daily_count(source, now) >= daily_cap:
        raise HTTPException(409, "护栏拒单[daily_cap]：当日下单已达上限 {}".format(daily_cap))

    if not _in_trading_hours(now) and not allow_offhours:
        raise HTTPException(409, "护栏拒单[market_closed]：非交易时段（设 *_ALLOW_OFFHOURS 可放行）")


def record_order(source: str, now: datetime.datetime | None = None) -> int:
    """真实下单成功后调用，累加指定交易源当日计数，返回累加后的值。"""
    now = now or datetime.datetime.now()
    with _lock:
        bucket = _daily_count.setdefault(source, {})
        key = _today_key(now)
        bucket[key] = bucket.get(key, 0) + 1
        return bucket[key]
