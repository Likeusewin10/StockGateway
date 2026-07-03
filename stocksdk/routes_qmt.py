"""君弘君智（迅投 QMT / XtQuant）交易路由：/qmt/*。

项目定位由「只读」扩为「读+交易」：QMT 是唯一交易源（EM/iFinD/Wind 仍只读）。

安全分层（服务经 ngrok 公网，交易端点务必收紧）：
- 写操作（order/cancel/写类 call）默认被 QMT_TRADING_ENABLED=false 全拦（503）。
- /qmt/order 默认 dry-run，只回显将发送的委托；confirm=true 才真发单。
- 真发单前过 guards 四道护栏（金额/白名单/当日笔数/交易时段），并写审计 jsonl。
读操作（asset/positions/orders/trades/health/events/methods）不受交易开关限制。
"""
import datetime
import json
from pathlib import Path
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from xtquant import xtconstant, xtdata

from stocksdk import guards
from stocksdk.config import (
    get_qmt_code_whitelist,
    get_qmt_daily_order_cap,
    get_qmt_max_notional,
    is_qmt_offhours_allowed,
    is_qmt_trading_enabled,
)
from stocksdk.security import rate_limit, require_key
from stocksdk.serialize import (
    qmt_asset,
    qmt_cancel_result,
    qmt_order,
    qmt_order_id_result,
    qmt_position,
    qmt_trade,
)
from stocksdk.sessions import ensure_qmt, lock, qmt_account, recent_qmt_events

router = APIRouter(prefix="/qmt", tags=["君弘君智 QMT 交易"])

_SIDE = {"buy": xtconstant.STOCK_BUY, "sell": xtconstant.STOCK_SELL}
_PRICE_TYPE = {"limit": xtconstant.FIX_PRICE, "latest": xtconstant.LATEST_PRICE}

# 透传禁用：交易类必须走带护栏的固定端点；会话/底层类会破坏服务连接。
_QMT_GUARDED = {"order_stock", "order_stock_async", "cancel_order_stock",
                "cancel_order_stock_async", "cancel_order_stock_sysid",
                "cancel_order_stock_sysid_async"}
_QMT_SESSION = {"start", "stop", "connect", "register_callback", "subscribe",
                "unsubscribe", "run_forever", "sleep",
                "set_relaxed_response_order_enabled"}

_AUDIT_DIR = Path(__file__).resolve().parent.parent / "audit"


def _audit(event: dict) -> None:
    """每笔交易请求/响应落本机 jsonl（gitignore）。绝不因审计失败影响下单流程。"""
    try:
        _AUDIT_DIR.mkdir(exist_ok=True)
        event = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), **event}
        fname = _AUDIT_DIR / "qmt-{}.jsonl".format(datetime.date.today().isoformat())
        with fname.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _require_trading_enabled() -> None:
    if not is_qmt_trading_enabled():
        raise HTTPException(503, "QMT 交易未启用（设 QMT_TRADING_ENABLED=true 开启）")


# ----------------------------- 读：账户/持仓/委托/成交 -----------------------------

@router.get("/health")
def qmt_health(_=Depends(require_key)):
    """深度健康：尝试连接终端并返回 connected。不抛错（未就绪返回 connected=false）。"""
    with lock:
        try:
            ensure_qmt()
            acc = qmt_account()
            return {"connected": True, "account": getattr(acc, "account_id", None)}
        except HTTPException as e:
            return {"connected": False, "detail": e.detail}


@router.get("/asset")
def qmt_get_asset(_=Depends(require_key), __=Depends(rate_limit)):
    """资金账户：可用/冻结/市值/总资产。"""
    with lock:
        ensure_qmt()
        return qmt_asset(ensure_qmt().query_stock_asset(qmt_account()))


@router.get("/positions")
def qmt_get_positions(_=Depends(require_key), __=Depends(rate_limit)):
    """持仓列表。"""
    with lock:
        trader = ensure_qmt()
        return [qmt_position(p) for p in (trader.query_stock_positions(qmt_account()) or [])]


@router.get("/orders")
def qmt_get_orders(cancelable: int = 0, _=Depends(require_key), __=Depends(rate_limit)):
    """委托列表。cancelable=1 只返回可撤委托。"""
    with lock:
        trader = ensure_qmt()
        res = trader.query_stock_orders(qmt_account(), bool(cancelable)) or []
        return [qmt_order(o) for o in res]


@router.get("/trades")
def qmt_get_trades(_=Depends(require_key), __=Depends(rate_limit)):
    """成交列表。"""
    with lock:
        trader = ensure_qmt()
        return [qmt_trade(t) for t in (trader.query_stock_trades(qmt_account()) or [])]


@router.get("/events")
def qmt_get_events(_=Depends(require_key)):
    """最近的交易回调事件（委托/成交/错误/断连），审计与观测用。"""
    return {"events": recent_qmt_events(),
            "daily_order_count": guards.current_daily_count("qmt")}


# ----------------------------- 写：下单/撤单 -----------------------------

class OrderReq(BaseModel):
    side: str                       # buy | sell
    stock_code: str                 # 如 "600000.SH"
    volume: int                     # 股
    price_type: str = "limit"       # limit | latest
    price: float = 0.0              # 限价单必填(>0)；最新价单忽略
    strategy: str = "sts"
    remark: str = ""
    confirm: bool = False           # 缺省 dry-run；true 才真发


class CancelReq(BaseModel):
    order_id: int
    confirm: bool = False


def _resolve_order(body: OrderReq) -> tuple[int, int, float, float]:
    """校验并解析下单参数 → (order_type, price_type_const, send_price, guard_price)。"""
    if body.side not in _SIDE:
        raise HTTPException(400, "side 必须为 buy|sell")
    if body.price_type not in _PRICE_TYPE:
        raise HTTPException(400, "price_type 必须为 limit|latest")
    if body.price_type == "limit":
        if not body.price or body.price <= 0:
            raise HTTPException(400, "限价单必须提供正的 price")
        send_price, guard_price = body.price, body.price
    else:   # latest：最新价委托，price 传 -1；金额无法预估，护栏跳过金额项
        send_price, guard_price = -1.0, 0.0
    return _SIDE[body.side], _PRICE_TYPE[body.price_type], send_price, guard_price


@router.post("/order")
def qmt_place_order(body: OrderReq, _=Depends(require_key), __=Depends(rate_limit)):
    """下单。默认 dry-run 只回显；confirm=true 且过护栏才真发单。"""
    _require_trading_enabled()
    order_type, price_type, send_price, guard_price = _resolve_order(body)

    guards.enforce(
        "qmt", body.stock_code, body.volume, guard_price,
        max_notional=get_qmt_max_notional(), daily_cap=get_qmt_daily_order_cap(),
        whitelist=get_qmt_code_whitelist(), allow_offhours=is_qmt_offhours_allowed(),
    )   # 越限抛 409

    preview = {
        "side": body.side, "stock_code": body.stock_code, "volume": body.volume,
        "price_type": body.price_type, "price": send_price,
        "strategy": body.strategy, "remark": body.remark,
        "daily_order_count": guards.current_daily_count("qmt"),
    }
    if not body.confirm:
        _audit({"action": "order", "result": "dry_run", **preview})
        return {"dry_run": True, "would_send": preview}

    with lock:
        trader = ensure_qmt()
        order_id = trader.order_stock(
            qmt_account(), body.stock_code, order_type, body.volume,
            price_type, send_price, body.strategy, body.remark)
    if order_id != -1:
        guards.record_order("qmt")
    _audit({"action": "order", "result": "sent", "order_id": order_id, **preview})
    return qmt_order_id_result(order_id)


@router.post("/cancel")
def qmt_cancel(body: CancelReq, _=Depends(require_key), __=Depends(rate_limit)):
    """撤单。默认 dry-run；confirm=true 才真撤。"""
    _require_trading_enabled()
    if not body.confirm:
        return {"dry_run": True, "would_cancel": {"order_id": body.order_id}}
    with lock:
        trader = ensure_qmt()
        code = trader.cancel_order_stock(qmt_account(), body.order_id)
    _audit({"action": "cancel", "order_id": body.order_id, "cancel_result": code})
    return qmt_cancel_result(code)


# ----------------------------- 透传 / 方法清单 -----------------------------

class QmtCall(BaseModel):
    args: List[Any] = []


def _obj_to_json(x: Any) -> Any:
    if isinstance(x, (list, tuple)):
        return [_obj_to_json(i) for i in x]
    if hasattr(x, "__dict__"):
        return {k: v for k, v in vars(x).items()}
    return x


@router.get("/methods")
def qmt_methods(_=Depends(require_key)):
    """列出 XtQuantTrader 可调用方法及类别标注。"""
    trader = None
    try:
        with lock:
            trader = ensure_qmt()
    except HTTPException:
        pass
    out = {}
    target = trader if trader is not None else None
    names = [n for n in dir(target) if not n.startswith("_")] if target else []
    for name in sorted(names):
        if not callable(getattr(target, name, None)):
            continue
        if name in _QMT_GUARDED:
            out[name] = "blocked(交易类,请用 /qmt/order|/qmt/cancel 带护栏端点)"
        elif name in _QMT_SESSION:
            out[name] = "blocked(会话/底层管理,透传禁止,可能断开服务连接)"
        elif name.startswith("query_"):
            out[name] = "ok(只读查询)"
        else:
            out[name] = "ok"
    return out


@router.post("/call/{method}")
def qmt_call(method: str, body: QmtCall = QmtCall(),
             _=Depends(require_key), __=Depends(rate_limit)):
    """透传只读类 XtQuantTrader 方法。交易/会话类一律拒绝(走专用端点)。"""
    if method.startswith("_"):
        raise HTTPException(403, "不可调用私有方法：{}".format(method))
    if method in _QMT_GUARDED:
        raise HTTPException(403, "交易类禁止透传，请用 /qmt/order 或 /qmt/cancel：{}".format(method))
    if method in _QMT_SESSION:
        raise HTTPException(403, "会话/底层管理方法禁止透传：{}".format(method))
    with lock:
        trader = ensure_qmt()
        fn = getattr(trader, method, None)
        if fn is None or not callable(fn):
            raise HTTPException(404, "未知方法：{}".format(method))
        try:
            return _obj_to_json(fn(*body.args))
        except HTTPException:
            raise
        except TypeError as e:
            raise HTTPException(400, "参数不匹配 {}：{}".format(method, e))
        except Exception as e:
            raise HTTPException(502, "QMT 调用异常 {}：{}".format(method, e))


# ============================= 行情数据（xtdata） =============================
# xtdata 是 QMT 的行情模块（K线/tick/板块/交易日/合约），与 xttrader 独立，
# 不需交易权限、不走 _require_trading_enabled，但仍需本机 QMT/miniQMT 终端在跑取数。
# 全部只读；download 仅把历史数据落本地缓存。失败统一 502。

_DATA_PASSTHROUGH_BLOCK = {"subscribe_quote", "subscribe_whole_quote", "unsubscribe_quote",
                           "run", "connect", "reconnect", "disconnect"}


def _jsonify_market(obj: Any) -> Any:
    """xtdata 返回的 DataFrame/ndarray/dict 转 JSON 友好结构（NaN→null）。"""
    import numpy as np
    import pandas as pd
    if isinstance(obj, dict):
        return {str(k): _jsonify_market(v) for k, v in obj.items()}
    if isinstance(obj, (pd.DataFrame, pd.Series)):
        return json.loads(obj.to_json(orient="split", date_format="iso"))
    if isinstance(obj, np.ndarray):
        return _jsonify_market(obj.tolist())
    if isinstance(obj, (list, tuple)):
        return [_jsonify_market(x) for x in obj]
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    return obj


def _split_csv(s: str) -> List[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


def _xtdata_guard(fn, *a, **k):
    """执行 xtdata 调用；终端未连/取数异常统一映射 502。"""
    try:
        return fn(*a, **k)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(502, "QMT 行情取数失败（确认 miniQMT 已启动）：{}".format(e))


@router.get("/data/kline")
def qmt_data_kline(codes: str, fields: str = "", period: str = "1d",
                   start: str = "", end: str = "", count: int = -1,
                   dividend: str = "none", _=Depends(require_key), __=Depends(rate_limit)):
    """历史/当日 K 线。codes,fields 逗号分隔；period 1m/5m/1d/tick；dividend none/front/back。"""
    res = _xtdata_guard(xtdata.get_market_data_ex, _split_csv(fields), _split_csv(codes),
                        period, start, end, count, dividend, True)
    return _jsonify_market(res)


@router.get("/data/tick")
def qmt_data_tick(codes: str, _=Depends(require_key), __=Depends(rate_limit)):
    """盘口最新 tick 快照。codes 逗号分隔。"""
    return _jsonify_market(_xtdata_guard(xtdata.get_full_tick, _split_csv(codes)))


@router.get("/data/sector")
def qmt_data_sector(name: str, _=Depends(require_key), __=Depends(rate_limit)):
    """板块成分股列表。name 如 '沪深A股' '沪深300'。"""
    return _jsonify_market(_xtdata_guard(xtdata.get_stock_list_in_sector, name))


@router.get("/data/trading_dates")
def qmt_data_trading_dates(market: str, start: str = "", end: str = "", count: int = -1,
                           _=Depends(require_key), __=Depends(rate_limit)):
    """交易日列表（毫秒时间戳）。market 如 SH/SZ。"""
    return _jsonify_market(_xtdata_guard(xtdata.get_trading_dates, market, start, end, count))


@router.get("/data/instrument")
def qmt_data_instrument(code: str, complete: int = 0,
                        _=Depends(require_key), __=Depends(rate_limit)):
    """合约详情。"""
    return _jsonify_market(_xtdata_guard(xtdata.get_instrument_detail, code, bool(complete)))


class DownloadReq(BaseModel):
    code: str
    period: str = "1d"
    start: str = ""
    end: str = ""


@router.post("/data/download")
def qmt_data_download(body: DownloadReq, _=Depends(require_key), __=Depends(rate_limit)):
    """下载历史数据到本地缓存（取历史 K 线前通常需先下载）。"""
    _xtdata_guard(xtdata.download_history_data, body.code, body.period, body.start, body.end)
    return {"status": "ok", "code": body.code, "period": body.period}


@router.get("/data/methods")
def qmt_data_methods(_=Depends(require_key)):
    """列出 xtdata 可调用方法（订阅/连接类标注为透传禁止）。"""
    out = {}
    for name in sorted(n for n in dir(xtdata) if not n.startswith("_")):
        if not callable(getattr(xtdata, name, None)):
            continue
        out[name] = "blocked(订阅/连接类,透传禁止)" if name in _DATA_PASSTHROUGH_BLOCK else "ok"
    return out


@router.post("/data/call/{method}")
def qmt_data_call(method: str, body: QmtCall = QmtCall(),
                  _=Depends(require_key), __=Depends(rate_limit)):
    """透传 xtdata 只读方法。订阅/连接类与私有方法拒绝。"""
    if method.startswith("_"):
        raise HTTPException(403, "不可调用私有方法：{}".format(method))
    if method in _DATA_PASSTHROUGH_BLOCK:
        raise HTTPException(403, "订阅/连接类方法禁止透传：{}".format(method))
    fn = getattr(xtdata, method, None)
    if fn is None or not callable(fn):
        raise HTTPException(404, "未知方法：{}".format(method))
    try:
        return _jsonify_market(fn(*body.args))
    except HTTPException:
        raise
    except TypeError as e:
        raise HTTPException(400, "参数不匹配 {}：{}".format(method, e))
    except Exception as e:
        raise HTTPException(502, "QMT 行情调用异常 {}：{}".format(method, e))
