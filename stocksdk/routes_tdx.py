"""通达信 TQ（TdxQuant）HTTP 路由：/tdx/*。

第四个数据源，与 /em /ths /wind 并列，只读取数、不交易。固定端点
（bars/snapshot/stock_info/sector/financial）+ 通用透传（call/methods）。
🔴 交易/写操作类（order_stock/cancel_order_stock/send_* 等）硬拦截 403——
项目定位 QMT 是唯一交易源，TDX 与 EM/iFinD/Wind 同为只读（定位边界）。
前提：本机通达信金融终端已开启并登录。
"""
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from stocksdk.security import rate_limit, require_key
from stocksdk.serialize import tdx_result
from stocksdk.sessions import lock, tdx_exec, tdx

router = APIRouter(prefix="/tdx", tags=["通达信 TDX"])

# 🔴 交易/写操作类：违反「只读取数不交易」定位边界，硬拦截 403，不暴露。
_TDX_TRADING = {"order_stock", "cancel_order_stock", "stock_account",
                "query_stock_asset", "query_stock_positions", "query_stock_orders"}
# 写客户端状态/发消息类：会改通达信终端状态或向其推送，禁止透传。
_TDX_WRITE = {"send_message", "send_warn", "send_file", "send_bt_data", "send_user_block",
              "create_sector", "delete_sector", "rename_sector", "clear_sector",
              "exec_to_tdx", "download_file", "data_transfer"}
# 会话/底层管理类：会改服务自身的 TQ 会话状态，禁止透传（如 close 会断开整个服务）。
_TDX_SESSION = {"initialize", "close"}
# 异步推送类：回调模型，同步 HTTP 单请求拿不到结果（后续可仿 routes_ws 做 WS）。
_TDX_ASYNC = {"subscribe_hq", "unsubscribe_hq", "get_subscribe_hq_stock_list", "subscribe_quote"}
_TDX_BLOCKED = _TDX_TRADING | _TDX_WRITE | _TDX_SESSION


def _split_csv(s: str) -> List[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


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


@router.get("/methods")
def tdx_methods(_=Depends(require_key)):
    """列出 tqcenter.tq 所有可调用方法及类别标注（交易/写类标注为已拦截）。"""
    out = {}
    for name in sorted(n for n in dir(tdx) if not n.startswith("_")):
        if not callable(getattr(tdx, name, None)):
            continue
        if name in _TDX_TRADING:
            out[name] = "blocked(交易类,定位边界禁止,调用返回 403)"
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
    """透传调用只读类 tq.<method>(*args, **kwargs)。交易/写/会话类一律 403。
    例：method=get_divid_factors args=["688318.SH","",""]"""
    if method.startswith("_"):
        raise HTTPException(403, "不可调用私有方法：{}".format(method))
    if method in _TDX_BLOCKED:
        raise HTTPException(403, "禁止调用交易/写/会话类方法（本服务只读取数）：{}".format(method))
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
