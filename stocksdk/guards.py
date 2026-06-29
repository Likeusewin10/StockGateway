"""下单护栏：在 /qmt/order 真正发单前做多重硬性校验。

四道护栏（全部可经 .env 配置，默认从严）：
1. 交易总开关 QMT_TRADING_ENABLED（默认关）——由路由层先行判断，这里复核。
2. 单笔金额上限 QMT_MAX_NOTIONAL（volume×price）。
3. 标的白名单 QMT_CODE_WHITELIST（留空=不限）。
4. 当日累计下单笔数 QMT_DAILY_ORDER_CAP。
另含交易时段校验（A 股 09:30–11:30 / 13:00–15:00），非时段拒单（除非 QMT_ALLOW_OFFHOURS）。

护栏只读配置 + 一个进程内当日计数器；单 worker 部署下足够，重启即重置。
"""
import datetime
import threading

from fastapi import HTTPException

from stocksdk.config import (
    get_qmt_code_whitelist,
    get_qmt_daily_order_cap,
    get_qmt_max_notional,
    is_qmt_offhours_allowed,
)

# A 股连续竞价时段（含集合竞价边界，简化为 09:30–11:30 / 13:00–15:00）。
_MORNING = (datetime.time(9, 30), datetime.time(11, 30))
_AFTERNOON = (datetime.time(13, 0), datetime.time(15, 0))

_lock = threading.Lock()
_daily_count: dict[str, int] = {}   # {YYYY-MM-DD: 已下单笔数}


def _today_key(now: datetime.datetime) -> str:
    return now.strftime("%Y-%m-%d")


def _in_trading_hours(now: datetime.datetime) -> bool:
    t = now.time()
    if now.weekday() >= 5:   # 周六日
        return False
    return (_MORNING[0] <= t <= _MORNING[1]) or (_AFTERNOON[0] <= t <= _AFTERNOON[1])


def current_daily_count(now: datetime.datetime | None = None) -> int:
    """当日已下单笔数（供 dry-run 预览 / 监控）。"""
    now = now or datetime.datetime.now()
    with _lock:
        return _daily_count.get(_today_key(now), 0)


def enforce(stock_code: str, volume: int, price: float,
            now: datetime.datetime | None = None) -> None:
    """逐条校验，违反任一即抛 HTTPException(409)。不修改计数（仅检查）。"""
    now = now or datetime.datetime.now()

    if volume is None or volume <= 0:
        raise HTTPException(409, "护栏拒单[volume]：委托数量必须为正，got {}".format(volume))

    whitelist = get_qmt_code_whitelist()
    if whitelist and stock_code not in whitelist:
        raise HTTPException(409, "护栏拒单[whitelist]：{} 不在白名单".format(stock_code))

    # 金额护栏：限价单按 price 估算；最新价单（price<=0）无法预估金额，跳过金额校验。
    if price and price > 0:
        notional = volume * price
        cap = get_qmt_max_notional()
        if notional > cap:
            raise HTTPException(
                409, "护栏拒单[max_notional]：单笔 {:.2f} 超上限 {:.2f}".format(notional, cap))

    cap_count = get_qmt_daily_order_cap()
    if current_daily_count(now) >= cap_count:
        raise HTTPException(409, "护栏拒单[daily_cap]：当日下单已达上限 {}".format(cap_count))

    if not _in_trading_hours(now) and not is_qmt_offhours_allowed():
        raise HTTPException(409, "护栏拒单[market_closed]：非交易时段（设 QMT_ALLOW_OFFHOURS 可放行）")


def record_order(now: datetime.datetime | None = None) -> int:
    """真实下单成功后调用，累加当日计数，返回累加后的值。"""
    now = now or datetime.datetime.now()
    with _lock:
        key = _today_key(now)
        _daily_count[key] = _daily_count.get(key, 0) + 1
        return _daily_count[key]
