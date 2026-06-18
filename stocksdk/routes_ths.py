"""同花顺 iFinD HTTP 路由：/ths/*。

固定端点(history/basic/realtime) + 通用透传(call/funcs)。
全部同步 THS_ 函数均可调用；仅对会话管理/异步类做提示性标注，不再拦截。
"""
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel

import iFinDPy
from iFinDPy import THS_HistoryQuotes, THS_BasicData, THS_RealtimeQuotes

from stocksdk.security import rate_limit, require_key
from stocksdk.serialize import ths_result
from stocksdk.sessions import ensure_ths, lock

router = APIRouter(prefix="/ths", tags=["同花顺 iFinD"])

# 仅用于 /ths/funcs 的状态标注，不再用于拦截。
# 会话/底层管理类：会改服务自身的 iFinD 会话状态，调用需谨慎（如 Logout 会登出整个服务）。
_THS_SESSION = {"THS_iFinDLogin", "THS_iFinDLogout", "THS_QuotesPushing",
                "THS_UnQuotesPushing", "THS_SetLanguage", "THS_GetErrorInfo",
                "THS_Trans2DataFrame"}


class ThsCall(BaseModel):
    args: List[Any] = []
    kwargs: Dict[str, Any] = {}


def _raise_if_error(r):
    """iFinD dict 返回的错误码 → 502。"""
    if r.get("errorcode") not in (0, None):
        raise HTTPException(502, "iFinD 取数失败：{} {}".format(r.get("errorcode"), r.get("errmsg")))
    return r


@router.get("/history")
def ths_history(codes: str, indicators: str, begin: str, end: str, params: str = "",
                _=Depends(require_key), __=Depends(rate_limit)):
    """同花顺历史行情。例：/ths/history?codes=300033.SZ&indicators=open;close&begin=2024-01-01&end=2024-01-05"""
    with lock:
        ensure_ths()
        r = THS_HistoryQuotes(codes, indicators, params, begin, end)
    return _raise_if_error(r)


@router.get("/basic")
def ths_basic(codes: str, indicators: str, params: str = "",
              _=Depends(require_key), __=Depends(rate_limit)):
    """同花顺基础/截面数据。"""
    with lock:
        ensure_ths()
        r = THS_BasicData(codes, indicators, params)
    return _raise_if_error(r)


@router.get("/realtime")
def ths_realtime(codes: str, indicators: str, params: str = "",
                 _=Depends(require_key), __=Depends(rate_limit)):
    """同花顺实时行情。"""
    with lock:
        ensure_ths()
        r = THS_RealtimeQuotes(codes, indicators, params)
    return _raise_if_error(r)


@router.get("/funcs")
def ths_funcs(_=Depends(require_key)):
    """列出 iFinDPy 所有 THS_ 函数及类别标注（全部可调用）。"""
    out = {}
    for name in sorted(n for n in dir(iFinDPy) if n.startswith("THS_")):
        if not callable(getattr(iFinDPy, name)):
            continue
        if name.startswith("THS_Asy"):
            out[name] = "ok(异步,HTTP 同步不适配,建议用 WS)"
        elif name in _THS_SESSION:
            out[name] = "ok(会话管理,谨慎:可能影响整个服务)"
        else:
            out[name] = "ok"
    return out


@router.post("/call/{func}")
def ths_call(func_name: str = Path(..., alias="func"), body: ThsCall = ThsCall(),
             _=Depends(require_key), __=Depends(rate_limit)):
    """透传调用 iFinDPy.THS_<func>(*args, **kwargs)。例：func=EDB args=["指标","","2024-01-01","2024-06-01"]"""
    name = func_name if func_name.startswith("THS_") else "THS_" + func_name
    fn = getattr(iFinDPy, name, None)
    if fn is None or not callable(fn):
        raise HTTPException(404, "未知函数：{}".format(name))
    with lock:
        ensure_ths()
        try:
            r = fn(*body.args, **body.kwargs)
        except TypeError as e:
            raise HTTPException(400, "参数不匹配 {}：{}".format(name, e))
        except Exception as e:   # SDK 底层(C++)异常 → 502，避免裸 500
            raise HTTPException(502, "iFinD 调用异常 {}：{}".format(name, e))
    return ths_result(r)
