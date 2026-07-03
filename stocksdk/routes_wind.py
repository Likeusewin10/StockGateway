"""万得 WindPy HTTP 路由：/wind/*。

固定端点(wsd/wss) + 通用透传(call/methods)。透传用 getattr 动态分发。
交易/调仓类(tlogon/torder/wupf 等)默认被 WIND_TRADING_ENABLED=false 拦(503)；
开启后经 /wind/call 放行并写审计 wind-*.jsonl。Wind 交易函数签名各异、无固定 order
端点，故走「总开关 + 审计」两层（不做逐笔 dry-run/护栏），靠 API Key + 总开关兜底。
固定端点默认 usedf=True 直接拿 DataFrame。
"""
import datetime
import json
from pathlib import Path
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from WindPy import w

from stocksdk.config import is_wind_trading_enabled
from stocksdk.security import rate_limit, require_key
from stocksdk.serialize import wind_result
from stocksdk.sessions import lock, wind_exec

router = APIRouter(prefix="/wind", tags=["万得 Wind"])

# 交易/写操作类：默认被 WIND_TRADING_ENABLED 总开关拦(503)，开启后经 /wind/call 放行 + 审计。
# 含 WindPy 各许可下可能出现的交易/调仓/划拨函数，宁可多列。
_WIND_TRADING = {"tlogon", "tlogout", "torder", "tcancel", "tquery", "wupf",
                 "tsmt", "tficcorder", "tportfolioorder", "tassettransfer",
                 # C 级底层封装（c_tXxx）同样纳入，走同一总开关 + 审计
                 "c_tlogon", "c_tlogout", "c_torder", "c_tcancel", "c_tquery", "c_wupf"}
# 异步推送类：回调模型，同步 HTTP 单请求拿不到结果（建议改用 WS，仿 routes_ws）。
_WIND_ASYNC = {"wsq", "cancelRequest"}
# 会话/底层管理类：会改服务自身的 Wind 会话状态，调用需谨慎（如 stop 会登出整个服务）。
_WIND_SESSION = {"start", "stop", "isconnected", "menu", "setLanguage"}

_AUDIT_DIR = Path(__file__).resolve().parent.parent / "audit"


def _audit(event: dict) -> None:
    """Wind 交易/写调用落本机 jsonl（gitignore）。绝不因审计失败影响调用流程。"""
    try:
        _AUDIT_DIR.mkdir(exist_ok=True)
        event = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), **event}
        fname = _AUDIT_DIR / "wind-{}.jsonl".format(datetime.date.today().isoformat())
        with fname.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")
    except Exception:
        pass


class WindCall(BaseModel):
    args: List[Any] = []
    usedf: bool = True   # 默认 usedf=True 返回 DataFrame（最省事路径）


@router.get("/wsd")
def wind_wsd(codes: str, fields: str, startdate: str, enddate: str, options: str = "",
             _=Depends(require_key), __=Depends(rate_limit)):
    """Wind 日序列数据。例：/wind/wsd?codes=600030.SH&fields=close&startdate=2024-01-01&enddate=2024-01-05"""
    with lock:
        return wind_result(wind_exec(
            lambda: w.wsd(codes, fields, startdate, enddate, options, usedf=True)))


@router.get("/wss")
def wind_wss(codes: str, fields: str, options: str = "",
             _=Depends(require_key), __=Depends(rate_limit)):
    """Wind 日截面数据。例：/wind/wss?codes=600030.SH,000001.SZ&fields=sec_name,close&options=tradeDate=20240105"""
    with lock:
        return wind_result(wind_exec(lambda: w.wss(codes, fields, options, usedf=True)))


@router.get("/methods")
def wind_methods(_=Depends(require_key)):
    """列出 Wind w 对象所有可调用方法及其类别标注（交易类标注为已拦截）。"""
    out = {}
    for name in sorted(n for n in dir(w) if not n.startswith("_")):
        if not callable(getattr(w, name)):
            continue
        if name.lower() in _WIND_TRADING:
            status = "guarded(交易/写操作,需 WIND_TRADING_ENABLED=true,经 /wind/call 放行+审计)"
        elif name in _WIND_ASYNC:
            status = "ok(异步推送,HTTP 同步不适配,建议用 WS)"
        elif name in _WIND_SESSION:
            status = "ok(会话管理,谨慎:可能影响整个服务)"
        else:
            status = "ok"
        out[name] = status
    return out


@router.post("/call/{method}")
def wind_call(method: str, body: WindCall = WindCall(),
              _=Depends(require_key), __=Depends(rate_limit)):
    """透传调用 Wind w.<method>(*args, usedf=...)。例：method=edb args=["M0017126","2024-01-01","2024-06-01"]

    交易/写类（torder/tlogon/wupf 等）需 WIND_TRADING_ENABLED=true 才放行，且写审计。"""
    if method.startswith("_"):
        raise HTTPException(403, "不可调用私有方法：{}".format(method))
    is_trading = method.lower() in _WIND_TRADING
    if is_trading and not is_wind_trading_enabled():
        raise HTTPException(503, "Wind 交易未启用（设 WIND_TRADING_ENABLED=true 开启）：{}".format(method))
    fn = getattr(w, method, None)
    if fn is None or not callable(fn):
        raise HTTPException(404, "未知方法：{}".format(method))
    if is_trading:
        _audit({"action": "trade_call", "method": method, "args": body.args})
    with lock:
        try:
            result = wind_exec(lambda: fn(*body.args, usedf=body.usedf))
        except TypeError:
            # 部分方法不接受 usedf 关键字（如日期函数 tdays、多数交易函数），退回不带 usedf 重试
            try:
                result = wind_exec(lambda: fn(*body.args))
            except TypeError as e:
                raise HTTPException(400, "参数不匹配 {}：{}".format(method, e))
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(502, "Wind 调用异常 {}：{}".format(method, e))
        except HTTPException:
            raise   # ensure_wind 重登失败抛的 502 直接透传
        except Exception as e:   # SDK 底层异常 → 502，避免裸 500
            raise HTTPException(502, "Wind 调用异常 {}：{}".format(method, e))
    if is_trading:
        _audit({"action": "trade_result", "method": method, "result": str(result)[:500]})
    return wind_result(result)
