"""东财 EMQuantAPI HTTP 路由：/em/*。

固定端点(csd/css) + 通用透传(call/methods)。透传用 getattr 动态分发，
全部方法均可调用；仅对会话管理/异步/交易类做**提示性标注**，不再拦截。
"""
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from EmQuantAPI import c

from stocksdk.security import rate_limit, require_key
from stocksdk.serialize import em_result, merge_pandas_option
from stocksdk.sessions import em_exec, lock

router = APIRouter(prefix="/em", tags=["东财 EM"])

# 仅用于 /em/methods 的状态标注，不再用于拦截。
# 异步推送类：回调模型，同步 HTTP 单请求拿不到结果（建议改用 *snapshot 或 WS）。
_EM_ASYNC = {"csq", "csqcancel", "csqsnapshot", "chq", "chqcancel", "chqsnapshot",
             "cst", "cnq", "cnqcancel"}
# 交易/下单类：操作虚拟组合持仓。
_EM_TRADING = {"pcreate", "pctransfer", "porder", "preport", "pquery", "pdelete"}
# 会话/底层管理类：会改服务自身的 SDK 会话状态，调用需谨慎（如 stop 会登出整个服务）。
_EM_SESSION = {"start", "stop", "setproxy", "setserverlistdir", "setbuslinehost",
               "setspeciallinehost", "manualactivate", "EmQuantData", "EncodeType",
               "Type_AsynDataFunc", "Type_logOutFunc", "geterrstring"}


class EmCall(BaseModel):
    args: List[Any] = []
    options_pandas: bool = True   # 自动给最后一个 options 串补 Ispandas=1（若适用）


@router.get("/csd")
def em_csd(codes: str, indicators: str, startdate: str, enddate: str, options: str = "",
           _=Depends(require_key), __=Depends(rate_limit)):
    """东财序列数据。例：/em/csd?codes=300059.SZ&indicators=CLOSE&startdate=2024-01-01&enddate=2024-01-05"""
    opts = (options + ",Ispandas=1").lstrip(",") if "Ispandas" not in options else options
    with lock:
        return em_result(em_exec(lambda: c.csd(codes, indicators, startdate, enddate, opts)))


@router.get("/css")
def em_css(codes: str, indicators: str, options: str = "",
           _=Depends(require_key), __=Depends(rate_limit)):
    """东财截面数据。例：/em/css?codes=300059.SZ,000002.SZ&indicators=OPEN,CLOSE&options=TradeDate=20240105"""
    opts = (options + ",Ispandas=1").lstrip(",") if "Ispandas" not in options else options
    with lock:
        return em_result(em_exec(lambda: c.css(codes, indicators, opts)))


@router.get("/methods")
def em_methods(_=Depends(require_key)):
    """列出东财 c 对象所有可调用方法及其类别标注（全部可调用）。"""
    out = {}
    for name in sorted(n for n in dir(c) if not n.startswith("_")):
        if not callable(getattr(c, name)):
            continue
        if name in _EM_SESSION:
            status = "ok(会话管理,谨慎:可能影响整个服务)"
        elif name in _EM_ASYNC:
            status = "ok(异步推送,HTTP 同步不适配,建议用 *snapshot 或 WS)"
        elif name in _EM_TRADING:
            status = "ok(交易/组合)"
        else:
            status = "ok"
        out[name] = status
    return out


@router.post("/call/{method}")
def em_call(method: str, body: EmCall = EmCall(),
            _=Depends(require_key), __=Depends(rate_limit)):
    """透传调用东财 c.<method>(*args)。例：method=edb args=["EMM00087117","Ispandas=1"]"""
    if method.startswith("_"):
        raise HTTPException(403, "不可调用私有方法：{}".format(method))
    fn = getattr(c, method, None)
    if fn is None or not callable(fn):
        raise HTTPException(404, "未知方法：{}".format(method))
    args = merge_pandas_option(body.args, body.options_pandas)
    with lock:
        try:
            result = em_exec(lambda: fn(*args))
        except TypeError as e:
            raise HTTPException(400, "参数不匹配 {}：{}".format(method, e))
        except HTTPException:
            raise   # ensure_em 重登失败抛的 502 直接透传
        except Exception as e:   # SDK 底层异常 → 502，避免裸 500
            raise HTTPException(502, "EM 调用异常 {}：{}".format(method, e))
    return em_result(result)
