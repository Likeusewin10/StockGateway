"""通达信 TQ（TdxQuant）HTTP 路由：/tdx/*。

第四个数据源，与 /em /ths /wind 并列取数；同时是**独立券商交易腿**——与 QMT（/qmt/*）
平级、各自独立（不是替代，两个券商接口互不干扰）。取数只读；交易走与 QMT 同构的
安全分层。

安全分层（服务经 ngrok 公网，交易端点务必收紧）：
- 写操作（order/cancel）默认被 TDX_TRADING_ENABLED=false 全拦（503）。
- /tdx/order 默认 dry-run，只回显将发送的委托；confirm=true 才真发单。
- 真发单前过 guards 四道护栏（金额/白名单/当日笔数/交易时段），并写审计 jsonl。
读操作（bars/snapshot/asset/positions/orders/... /methods）不受交易开关限制。

🔴 TQ 下单常量与 QMT 不同：tqconst.STOCK_BUY=0/STOCK_SELL=1、PRICE_MY=0(限价)/
PRICE_SJ=1(市价)；order_stock/cancel_order_stock 返回 dict{'ErrorId','Msg','Value'}，
与 QMT 的返回码完全不同（归一化见 serialize.tdx_order_result/tdx_cancel_result）。
前提：本机通达信金融终端已开启并登录。
"""
import datetime
import json
from pathlib import Path
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from stocksdk import guards
from stocksdk.config import (
    get_tdx_code_whitelist,
    get_tdx_daily_order_cap,
    get_tdx_max_notional,
    is_tdx_offhours_allowed,
    is_tdx_trading_enabled,
)
from stocksdk.security import rate_limit, require_key
from stocksdk.serialize import tdx_cancel_result, tdx_order_result, tdx_result
from stocksdk.sessions import ensure_tdx, ensure_tdx_account, lock, tdx, tdx_account, tdx_exec

from tqcenter import tqconst   # noqa: E402  下单方向/报价类型常量（sessions 已完成 tqcenter 引导）

router = APIRouter(prefix="/tdx", tags=["通达信 TDX"])

_SIDE = {"buy": tqconst.STOCK_BUY, "sell": tqconst.STOCK_SELL}
_PRICE_TYPE = {"limit": tqconst.PRICE_MY, "market": tqconst.PRICE_SJ}

# 交易类：必须走带护栏的固定端点（/tdx/order|/tdx/cancel），透传一律 403。
_TDX_GUARDED = {"order_stock", "cancel_order_stock"}
# 需账户句柄的查询类：走固定端点（/tdx/asset|positions|orders）自动注入句柄，透传标注引导。
_TDX_ACCOUNT = {"stock_account", "query_stock_asset", "query_stock_positions", "query_stock_orders"}
# 写客户端状态/发消息类：会改通达信终端状态或向其推送，禁止透传。
_TDX_WRITE = {"send_message", "send_warn", "send_file", "send_bt_data", "send_user_block",
              "create_sector", "delete_sector", "rename_sector", "clear_sector",
              "exec_to_tdx", "download_file", "data_transfer"}
# 会话/底层管理类：会改服务自身的 TQ 会话状态，禁止透传（如 close 会断开整个服务）。
_TDX_SESSION = {"initialize", "close"}
# 异步推送类：回调模型，同步 HTTP 单请求拿不到结果（后续可仿 routes_ws 做 WS）。
_TDX_ASYNC = {"subscribe_hq", "unsubscribe_hq", "get_subscribe_hq_stock_list", "subscribe_quote"}
_TDX_BLOCKED = _TDX_GUARDED | _TDX_ACCOUNT | _TDX_WRITE | _TDX_SESSION

_AUDIT_DIR = Path(__file__).resolve().parent.parent / "audit"


def _split_csv(s: str) -> List[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


def _audit(event: dict) -> None:
    """每笔交易请求/响应落本机 jsonl（gitignore）。绝不因审计失败影响下单流程。"""
    try:
        _AUDIT_DIR.mkdir(exist_ok=True)
        event = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), **event}
        fname = _AUDIT_DIR / "tdx-{}.jsonl".format(datetime.date.today().isoformat())
        with fname.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _require_trading_enabled() -> None:
    if not is_tdx_trading_enabled():
        raise HTTPException(503, "TDX 交易未启用（设 TDX_TRADING_ENABLED=true 开启）")


# ----------------------------- 取数（只读，不受交易开关限制）-----------------------------

@router.get("/bars")
def tdx_bars(codes: str, fields: str = "", period: str = "1d",
             start: str = "", end: str = "", count: int = -1,
             dividend: str = "none", _=Depends(require_key), __=Depends(rate_limit)):
    """历史/当日 K 线。codes 逗号分隔；period 1d/1w/1m/5m/15m/30m/60m；dividend none/front/back。
    例：/tdx/bars?codes=600519.SH,000001.SZ&period=1d&count=5&dividend=front"""
    with lock:
        return tdx_result(tdx_exec(lambda: tdx.get_market_data(
            field_list=_split_csv(fields), stock_list=_split_csv(codes), period=period,
            start_time=start, end_time=end, count=count, dividend_type=dividend, fill_data=True)))


@router.get("/snapshot")
def tdx_snapshot(code: str, fields: str = "", _=Depends(require_key), __=Depends(rate_limit)):
    """单只证券最新行情快照（含五档买卖盘）。例：/tdx/snapshot?code=600519.SH"""
    with lock:
        return tdx_result(tdx_exec(lambda: tdx.get_market_snapshot(
            stock_code=code, field_list=_split_csv(fields))))


@router.get("/stock_info")
def tdx_stock_info(code: str, fields: str, _=Depends(require_key), __=Depends(rate_limit)):
    """证券基础财务/资料数据。fields 必填，逗号分隔（如 J_zgb,ActiveCapital）。"""
    with lock:
        return tdx_result(tdx_exec(lambda: tdx.get_stock_info(
            stock_code=code, field_list=_split_csv(fields))))


@router.get("/financial")
def tdx_financial(codes: str, fields: str, start: str = "", end: str = "",
                  report_type: str = "report_time",
                  _=Depends(require_key), __=Depends(rate_limit)):
    """专业财务数据（需客户端先下载专业财务数据）。fields 为 Fn 字段，如 Fn193,Fn194。
    report_type: report_time 按截止日期 / announce_time 按公告日期。"""
    with lock:
        return tdx_result(tdx_exec(lambda: tdx.get_financial_data(
            stock_list=_split_csv(codes), field_list=_split_csv(fields),
            start_time=start, end_time=end, report_type=report_type)))


@router.get("/sector")
def tdx_sector(block: str, block_type: int = 0, list_type: int = 0,
               _=Depends(require_key), __=Depends(rate_limit)):
    """板块成分股。block 为板块代码或名称；block_type 0 代码/名称 1 自定义板块简称 2 期货前缀。
    list_type 0 仅代码 / 1 代码+名称。"""
    with lock:
        return tdx_result(tdx_exec(lambda: tdx.get_stock_list_in_sector(
            block_code=block, block_type=block_type, list_type=list_type)))


@router.get("/stock_list")
def tdx_stock_list(market: str, list_type: int = 0,
                   _=Depends(require_key), __=Depends(rate_limit)):
    """按市场类型取股票代码列表。market 如 5 所有A股/50 沪深A股/23 沪深300/52 科创板/53 北交所。
    list_type 0 仅代码 / 1 代码+名称。"""
    with lock:
        return tdx_result(tdx_exec(lambda: tdx.get_stock_list(market=market, list_type=list_type)))


@router.get("/trading_dates")
def tdx_trading_dates(market: str, start: str = "", end: str = "", count: int = -1,
                      _=Depends(require_key), __=Depends(rate_limit)):
    """交易日列表（需客户端先下载上证指数 999999 盘后数据，仅 A 股）。market 如 SH/SZ。"""
    with lock:
        return tdx_result(tdx_exec(lambda: tdx.get_trading_dates(
            market=market, start_time=start, end_time=end, count=count)))


# ----------------------------- 交易查询（读，需账户句柄，不受交易开关限制）-----------------------------

@router.get("/health")
def tdx_health(_=Depends(require_key)):
    """深度健康：尝试初始化会话并取账户句柄。不抛错（未就绪返回 connected=false）。"""
    with lock:
        try:
            ensure_tdx()
            handle = ensure_tdx_account()
            return {"connected": True, "account": handle}
        except HTTPException as e:
            return {"connected": False, "detail": e.detail}
        except Exception as e:  # 缺账号配置(RuntimeError)等非 HTTP 异常也须优雅降级,不抛 500
            return {"connected": False, "detail": str(e)}


@router.get("/asset")
def tdx_get_asset(_=Depends(require_key), __=Depends(rate_limit)):
    """资金账户资产（余额/可用/资产/市值）。"""
    with lock:
        acc = ensure_tdx_account()
        return tdx_result(tdx_exec(lambda: tdx.query_stock_asset(account_id=acc)))


@router.get("/positions")
def tdx_get_positions(_=Depends(require_key), __=Depends(rate_limit)):
    """持仓列表。"""
    with lock:
        acc = ensure_tdx_account()
        return tdx_result(tdx_exec(lambda: tdx.query_stock_positions(account_id=acc)))


@router.get("/orders")
def tdx_get_orders(code: str = "", cancelable: int = 0,
                   _=Depends(require_key), __=Depends(rate_limit)):
    """当日委托列表。code 可选按证券代码过滤；cancelable=1 只看可撤委托。"""
    with lock:
        acc = ensure_tdx_account()
        return tdx_result(tdx_exec(lambda: tdx.query_stock_orders(
            account_id=acc, stock_code=code, cancelable_only=bool(cancelable))))


# ----------------------------- 交易写：下单/撤单 -----------------------------

class TdxOrderReq(BaseModel):
    side: str                       # buy | sell
    stock_code: str                 # 如 "600519.SH"
    volume: int                     # 股
    price_type: str = "limit"       # limit（自填价 PRICE_MY）| market（市价 PRICE_SJ）
    price: float = 0.0              # 限价单必填(>0)；市价单忽略
    confirm: bool = False           # 缺省 dry-run；true 才真发


class TdxCancelReq(BaseModel):
    stock_code: str                 # 撤单需证券代码（与 QMT 不同）
    order_id: int                   # 委托编号 Wtbh
    confirm: bool = False


def _resolve_order(body: TdxOrderReq) -> tuple[int, int, float, float]:
    """校验并解析下单参数 → (order_type, price_type_const, send_price, guard_price)。"""
    if body.side not in _SIDE:
        raise HTTPException(400, "side 必须为 buy|sell")
    if body.price_type not in _PRICE_TYPE:
        raise HTTPException(400, "price_type 必须为 limit|market")
    if body.price_type == "limit":
        if not body.price or body.price <= 0:
            raise HTTPException(400, "限价单必须提供正的 price")
        send_price, guard_price = body.price, body.price
    else:   # market：市价委托，price 传 0；金额无法预估，护栏跳过金额项
        send_price, guard_price = 0.0, 0.0
    return _SIDE[body.side], _PRICE_TYPE[body.price_type], send_price, guard_price


@router.post("/order")
def tdx_place_order(body: TdxOrderReq, _=Depends(require_key), __=Depends(rate_limit)):
    """下单。默认 dry-run 只回显；confirm=true 且过护栏才真发单。"""
    _require_trading_enabled()
    order_type, price_type, send_price, guard_price = _resolve_order(body)

    guards.enforce(
        "tdx", body.stock_code, body.volume, guard_price,
        max_notional=get_tdx_max_notional(), daily_cap=get_tdx_daily_order_cap(),
        whitelist=get_tdx_code_whitelist(), allow_offhours=is_tdx_offhours_allowed(),
    )   # 越限抛 409

    preview = {
        "side": body.side, "stock_code": body.stock_code, "volume": body.volume,
        "price_type": body.price_type, "price": send_price,
        "daily_order_count": guards.current_daily_count("tdx"),
    }
    if not body.confirm:
        _audit({"action": "order", "result": "dry_run", **preview})
        return {"dry_run": True, "would_send": preview}

    with lock:
        acc = ensure_tdx_account()
        res = tdx_exec(lambda: tdx.order_stock(
            account_id=acc, stock_code=body.stock_code, order_type=order_type,
            order_volume=body.volume, price_type=price_type, price=send_price, notify=0))
    out = tdx_order_result(res)   # Value==0/ErrorId!=0 → 502
    guards.record_order("tdx")
    _audit({"action": "order", "result": "sent", **out, **preview})
    return out


@router.post("/cancel")
def tdx_cancel(body: TdxCancelReq, _=Depends(require_key), __=Depends(rate_limit)):
    """撤单。默认 dry-run；confirm=true 才真撤。撤单需 stock_code + order_id。"""
    _require_trading_enabled()
    if not body.confirm:
        return {"dry_run": True,
                "would_cancel": {"stock_code": body.stock_code, "order_id": body.order_id}}
    with lock:
        acc = ensure_tdx_account()
        res = tdx_exec(lambda: tdx.cancel_order_stock(
            account_id=acc, stock_code=body.stock_code, order_id=body.order_id))
    out = tdx_cancel_result(res)
    _audit({"action": "cancel", "stock_code": body.stock_code,
            "order_id": body.order_id, **out})
    return out


# ----------------------------- 透传 / 方法清单 -----------------------------

@router.get("/methods")
def tdx_methods(_=Depends(require_key)):
    """列出 tqcenter.tq 所有可调用方法及类别标注。"""
    out = {}
    for name in sorted(n for n in dir(tdx) if not n.startswith("_")):
        if not callable(getattr(tdx, name, None)):
            continue
        if name in _TDX_GUARDED:
            out[name] = "blocked(交易类,请用 /tdx/order|/tdx/cancel 带护栏端点)"
        elif name in _TDX_ACCOUNT:
            out[name] = "blocked(需账户句柄,请用 /tdx/asset|positions|orders 端点)"
        elif name in _TDX_WRITE:
            out[name] = "blocked(写客户端状态,透传禁止,返回 403)"
        elif name in _TDX_SESSION:
            out[name] = "blocked(会话管理,透传禁止,可能断开服务连接)"
        elif name in _TDX_ASYNC:
            out[name] = "ok(异步推送,HTTP 同步不适配,建议用 WS)"
        else:
            out[name] = "ok"
    return out


class TdxCall(BaseModel):
    args: List[Any] = []
    kwargs: dict = {}


@router.post("/call/{method}")
def tdx_call(method: str, body: TdxCall = TdxCall(),
             _=Depends(require_key), __=Depends(rate_limit)):
    """透传调用只读取数类 tq.<method>(*args, **kwargs)。交易/账户/写/会话类一律 403
    （交易走 /tdx/order|/tdx/cancel，账户查询走 /tdx/asset|positions|orders）。
    例：method=get_divid_factors args=["688318.SH","",""]"""
    if method.startswith("_"):
        raise HTTPException(403, "不可调用私有方法：{}".format(method))
    if method in _TDX_BLOCKED:
        raise HTTPException(403, "禁止透传（交易/账户/写/会话类请走专用端点）：{}".format(method))
    fn = getattr(tdx, method, None)
    if fn is None or not callable(fn):
        raise HTTPException(404, "未知方法：{}".format(method))
    with lock:
        try:
            result = tdx_exec(lambda: fn(*body.args, **body.kwargs))
        except HTTPException:
            raise   # ensure_tdx 初始化失败抛的 502 直接透传
        except TypeError as e:
            raise HTTPException(400, "参数不匹配 {}：{}".format(method, e))
        except Exception as e:   # SDK 底层异常 → 502，避免裸 500
            raise HTTPException(502, "TDX 调用异常 {}：{}".format(method, e))
    return tdx_result(result)
