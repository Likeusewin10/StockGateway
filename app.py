"""股票数据 HTTP 服务：其他项目通过 ip:端口 + 参数取数，无需写 SDK 代码。

启动（在 .venv-api 下）：
    .venv-api\\Scripts\\python -m uvicorn app:app --host 0.0.0.0 --port 8000

说明：
- 两个 SDK 均单会话/单点登录，本服务用全局锁串行化所有请求，
  必须单 worker 运行（不要加 --workers）。
- 默认无鉴权，仅限内网使用。不要直接暴露到公网。
- 交互式文档：http://<ip>:8000/docs
"""
import os
import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader

# ---- 加载 .env ----
for _line in Path(__file__).with_name(".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _, _v = _line.partition("=")
        os.environ.setdefault(_k.strip(), _v.strip())

from EmQuantAPI import c
import iFinDPy
from iFinDPy import (
    THS_iFinDLogin,
    THS_iFinDLogout,
    THS_HistoryQuotes,
    THS_BasicData,
    THS_RealtimeQuotes,
)

# 全局锁：SDK 单会话，所有取数串行化
_lock = threading.Lock()
_em_ready = False
_ths_ready = False


def _ensure_em():
    global _em_ready
    if not _em_ready:
        r = c.start("ForceLogin=1", "")
        if r.ErrorCode != 0:
            raise HTTPException(502, "EM 登录失败：{} {}".format(r.ErrorCode, r.ErrorMsg))
        _em_ready = True


def _ensure_ths():
    global _ths_ready
    if not _ths_ready:
        code = THS_iFinDLogin(os.environ["THS_USER"], os.environ["THS_PWD"])
        if code != 0:
            raise HTTPException(502, "iFinD 登录失败：{}".format(code))
        _ths_ready = True


def _em_result(result):
    """EM 返回统一成 JSON 友好结构。Ispandas=1 时直接是 DataFrame。"""
    import pandas as pd
    if isinstance(result, tuple) and len(result) == 2:
        result = result[1]
    if isinstance(result, pd.DataFrame):
        return result.reset_index().to_dict(orient="records")
    if hasattr(result, "ErrorCode") and result.ErrorCode != 0:
        raise HTTPException(502, "EM 取数失败：{} {}".format(result.ErrorCode, result.ErrorMsg))
    return getattr(result, "Data", result)


app = FastAPI(title="股票数据服务", description="EM + iFinD 统一取数接口")

# ---- API Key 鉴权 ----
# .env 里设了 API_KEY 则所有取数接口要求请求头 X-API-Key 匹配；留空则不鉴权。
_API_KEY = os.environ.get("API_KEY", "").strip()
_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_key(key: str = Security(_api_key_header)):
    if not _API_KEY:          # 未配置 key：不鉴权（仅本机/内网场景）
        return
    if key != _API_KEY:
        raise HTTPException(401, "缺少或错误的 X-API-Key")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/em/csd")
def em_csd(codes: str, indicators: str, startdate: str, enddate: str, options: str = "", _=Depends(require_key)):
    """东财序列数据。例：/em/csd?codes=300059.SZ&indicators=CLOSE&startdate=2024-01-01&enddate=2024-01-05"""
    opts = (options + ",Ispandas=1").lstrip(",") if "Ispandas" not in options else options
    with _lock:
        _ensure_em()
        return _em_result(c.csd(codes, indicators, startdate, enddate, opts))


@app.get("/em/css")
def em_css(codes: str, indicators: str, options: str = "", _=Depends(require_key)):
    """东财截面数据。例：/em/css?codes=300059.SZ,000002.SZ&indicators=OPEN,CLOSE&options=TradeDate=20240105"""
    opts = (options + ",Ispandas=1").lstrip(",") if "Ispandas" not in options else options
    with _lock:
        _ensure_em()
        return _em_result(c.css(codes, indicators, opts))


@app.get("/ths/history")
def ths_history(codes: str, indicators: str, begin: str, end: str, params: str = "", _=Depends(require_key)):
    """同花顺历史行情。例：/ths/history?codes=300033.SZ&indicators=open;close&begin=2024-01-01&end=2024-01-05"""
    with _lock:
        _ensure_ths()
        r = THS_HistoryQuotes(codes, indicators, params, begin, end)
    if r.get("errorcode") not in (0, None):
        raise HTTPException(502, "iFinD 取数失败：{} {}".format(r.get("errorcode"), r.get("errmsg")))
    return r


@app.get("/ths/basic")
def ths_basic(codes: str, indicators: str, params: str = "", _=Depends(require_key)):
    """同花顺基础/截面数据。"""
    with _lock:
        _ensure_ths()
        r = THS_BasicData(codes, indicators, params)
    if r.get("errorcode") not in (0, None):
        raise HTTPException(502, "iFinD 取数失败：{} {}".format(r.get("errorcode"), r.get("errmsg")))
    return r


@app.get("/ths/realtime")
def ths_realtime(codes: str, indicators: str, params: str = "", _=Depends(require_key)):
    """同花顺实时行情。"""
    with _lock:
        _ensure_ths()
        r = THS_RealtimeQuotes(codes, indicators, params)
    if r.get("errorcode") not in (0, None):
        raise HTTPException(502, "iFinD 取数失败：{} {}".format(r.get("errorcode"), r.get("errmsg")))
    return r


# ====================================================================
# 通用透传：用 getattr 动态分发到 SDK 任意方法，无需逐个手写端点。
# POST /em/call/{method}   body: {"args": [...], "options_pandas": true}
# POST /ths/call/{func}    body: {"args": [...], "kwargs": {...}}
# GET  /em/methods  /ths/funcs  自省可调用名。
# ====================================================================
from typing import Any, Dict, List
from pydantic import BaseModel

# 异步推送类：回调模型，同步 HTTP 单请求拿不到结果，默认禁用（用 *snapshot 同步替代）。
_EM_ASYNC = {"csq", "csqcancel", "csqsnapshot", "chq", "chqcancel", "chqsnapshot",
             "cst", "cnq", "cnqcancel"}
# 交易/下单类：有资金风险，默认禁，ALLOW_TRADING=1 才放开。
_EM_TRADING = {"pcreate", "pctransfer", "porder", "preport", "pquery", "pdelete"}
# 会话/底层管理类：不应通过取数接口暴露。
_EM_BLOCKED = {"start", "stop", "setproxy", "setserverlistdir", "setbuslinehost",
               "setspeciallinehost", "manualactivate", "EmQuantData", "EncodeType",
               "Type_AsynDataFunc", "Type_logOutFunc", "geterrstring"}

_ALLOW_TRADING = os.environ.get("ALLOW_TRADING", "").strip() == "1"


class EmCall(BaseModel):
    args: List[Any] = []
    options_pandas: bool = True   # 自动给最后一个 options 串补 Ispandas=1（若适用）


@app.get("/em/methods")
def em_methods(_=Depends(require_key)):
    """列出东财 c 对象所有可调用方法及其是否可用。"""
    out = {}
    for name in sorted(n for n in dir(c) if not n.startswith("_")):
        if not callable(getattr(c, name)):
            continue
        if name in _EM_BLOCKED:
            status = "blocked(会话管理)"
        elif name in _EM_ASYNC:
            status = "blocked(异步推送)"
        elif name in _EM_TRADING:
            status = "ok" if _ALLOW_TRADING else "blocked(交易,设ALLOW_TRADING=1)"
        else:
            status = "ok"
        out[name] = status
    return out


@app.post("/em/call/{method}")
def em_call(method: str, body: EmCall = EmCall(), _=Depends(require_key)):
    """透传调用东财 c.<method>(*args)。例：method=edb args=["EMM00087117","Ispandas=1"]"""
    if method.startswith("_") or method in _EM_BLOCKED:
        raise HTTPException(403, "方法不可用：{}".format(method))
    if method in _EM_ASYNC:
        raise HTTPException(403, "异步推送类不支持 HTTP 同步调用：{}（改用 *snapshot）".format(method))
    if method in _EM_TRADING and not _ALLOW_TRADING:
        raise HTTPException(403, "交易类默认禁用：{}（设 ALLOW_TRADING=1 放开）".format(method))
    fn = getattr(c, method, None)
    if fn is None or not callable(fn):
        raise HTTPException(404, "未知方法：{}".format(method))
    args = list(body.args)
    # 仅当最后一个参数“看起来像 options/params 串(含 =)”时才补 Ispandas=1；
    # 否则它可能是日期/代码(如 csd 的 enddate、tradedates 的 enddate)，追加会破坏取值。
    if (body.options_pandas and args and isinstance(args[-1], str)
            and "=" in args[-1] and "Ispandas" not in args[-1]):
        args[-1] = args[-1] + ",Ispandas=1"
    with _lock:
        _ensure_em()
        try:
            result = fn(*args)
        except TypeError as e:
            raise HTTPException(400, "参数不匹配 {}：{}".format(method, e))
        except Exception as e:   # SDK 底层异常 → 502，避免裸 500
            raise HTTPException(502, "EM 调用异常 {}：{}".format(method, e))
    return _em_result(result)


# ---- 同花顺 iFinD 通用透传 ----
_THS_BLOCKED = {"THS_iFinDLogin", "THS_iFinDLogout", "THS_QuotesPushing",
                "THS_UnQuotesPushing", "THS_SetLanguage", "THS_GetErrorInfo",
                "THS_Trans2DataFrame"}


class ThsCall(BaseModel):
    args: List[Any] = []
    kwargs: Dict[str, Any] = {}


def _ths_result(r):
    """iFinD 返回统一成 JSON：dict 直接返回，DataFrame 转 records。"""
    import pandas as pd
    if isinstance(r, pd.DataFrame):
        return r.reset_index().to_dict(orient="records")
    if isinstance(r, dict) and r.get("errorcode") not in (0, None):
        raise HTTPException(502, "iFinD 取数失败：{} {}".format(r.get("errorcode"), r.get("errmsg")))
    return r


@app.get("/ths/funcs")
def ths_funcs(_=Depends(require_key)):
    """列出 iFinDPy 所有同步 THS_ 函数（异步 THS_Asy* 不列）。"""
    out = {}
    for name in sorted(n for n in dir(iFinDPy) if n.startswith("THS_")):
        if name.startswith("THS_Asy"):
            continue
        if not callable(getattr(iFinDPy, name)):
            continue
        out[name] = "blocked(会话管理)" if name in _THS_BLOCKED else "ok"
    return out


@app.post("/ths/call/{func}")
def ths_call(func: str, body: ThsCall = ThsCall(), _=Depends(require_key)):
    """透传调用 iFinDPy.THS_<func>(*args, **kwargs)。例：func=EDB args=["指标","","2024-01-01","2024-06-01"]"""
    name = func if func.startswith("THS_") else "THS_" + func
    if name.startswith("THS_Asy"):
        raise HTTPException(403, "异步类不支持 HTTP 同步调用：{}".format(name))
    if name in _THS_BLOCKED:
        raise HTTPException(403, "方法不可用：{}".format(name))
    fn = getattr(iFinDPy, name, None)
    if fn is None or not callable(fn):
        raise HTTPException(404, "未知函数：{}".format(name))
    with _lock:
        _ensure_ths()
        try:
            r = fn(*body.args, **body.kwargs)
        except TypeError as e:
            raise HTTPException(400, "参数不匹配 {}：{}".format(name, e))
        except Exception as e:   # SDK 底层(C++)异常 → 502，避免裸 500
            raise HTTPException(502, "iFinD 调用异常 {}：{}".format(name, e))
    return _ths_result(r)


# ====================================================================
# WebSocket 实时推送：真·订阅推送。SDK 回调在后台线程触发，
# 用 loop.call_soon_threadsafe 把数据塞进 asyncio.Queue，再由 pump 协程发给 WS。
# 注册/退订在 executor 线程里持全局锁执行；推送本身不碰锁。
# 鉴权走 query 参数 ?key=（WS 不便带请求头）。
#   WS /em/ws   收发 JSON：{"action":"subscribe","codes":"300059.SZ","indicators":"now,open"}
#   WS /ths/ws  收发 JSON：{"action":"subscribe","codes":"300033.SZ","indicators":"latest"}
# ====================================================================
import asyncio
import json
from fastapi import WebSocket, WebSocketDisconnect


def _em_quote_to_dict(qd):
    """EmQuantData 推送对象 → JSON 友好 dict。"""
    if getattr(qd, "ErrorCode", 0) not in (0, None):
        return {"event": "error", "code": qd.ErrorCode, "msg": getattr(qd, "ErrorMsg", "")}
    return {
        "event": "quote",
        "codes": list(getattr(qd, "Codes", []) or []),
        "indicators": list(getattr(qd, "Indicators", []) or []),
        "data": getattr(qd, "Data", {}) or {},
    }


async def _pump(ws: WebSocket, q: "asyncio.Queue"):
    """从队列取数据推给 WS，直到被取消。"""
    while True:
        item = await q.get()
        await ws.send_json(item)


def _ws_authed(ws: WebSocket) -> bool:
    if not _API_KEY:
        return True
    return ws.query_params.get("key") == _API_KEY


# 占位：WS 端点在下方追加


@app.websocket("/em/ws")
async def em_ws(ws: WebSocket):
    """东财实时行情 WebSocket 推送。连接后发 {"action":"subscribe","codes":...,"indicators":...}。"""
    await ws.accept()
    if not _ws_authed(ws):
        await ws.send_json({"event": "error", "msg": "缺少或错误的 key（用 ?key= 传）"})
        await ws.close(code=4401)
        return

    loop = asyncio.get_running_loop()
    q: asyncio.Queue = asyncio.Queue(maxsize=1000)
    serials: list = []   # 本连接的所有订阅号，断开时统一退订

    def _callback(quantdata):
        # SDK 后台线程触发：跨线程把数据塞进事件循环的队列
        try:
            loop.call_soon_threadsafe(q.put_nowait, _em_quote_to_dict(quantdata))
        except Exception:
            pass
        return 0

    pump = asyncio.create_task(_pump(ws, q))
    try:
        while True:
            msg = await ws.receive_text()
            try:
                req = json.loads(msg)
            except Exception:
                await ws.send_json({"event": "error", "msg": "非法 JSON"})
                continue
            action = req.get("action")
            if action == "subscribe":
                codes = req.get("codes", "")
                indicators = req.get("indicators", "")
                options = req.get("options", "")

                def _do_sub():
                    with _lock:
                        _ensure_em()
                        return c.csq(codes, indicators, options, _callback)

                r = await loop.run_in_executor(None, _do_sub)
                sid = getattr(r, "SerialID", None)
                if getattr(r, "ErrorCode", 0) not in (0, None):
                    await ws.send_json({"event": "error",
                                        "msg": "订阅失败 {} {}".format(r.ErrorCode, getattr(r, "ErrorMsg", ""))})
                else:
                    serials.append(sid)
                    await ws.send_json({"event": "subscribed", "serial": sid,
                                        "codes": codes, "indicators": indicators})
            elif action == "unsubscribe":
                sid = req.get("serial")
                if sid is not None:
                    await loop.run_in_executor(None, lambda: c.csqcancel(sid))
                    if sid in serials:
                        serials.remove(sid)
                    await ws.send_json({"event": "unsubscribed", "serial": sid})
            else:
                await ws.send_json({"event": "error", "msg": "未知 action：{}".format(action)})
    except WebSocketDisconnect:
        pass
    finally:
        pump.cancel()
        for sid in serials:    # 断开自动退订全部，避免 SDK 侧订阅泄漏
            try:
                await loop.run_in_executor(None, lambda s=sid: c.csqcancel(s))
            except Exception:
                pass


@app.websocket("/ths/ws")
async def ths_ws(ws: WebSocket):
    """同花顺实时行情 WebSocket 推送。发 {"action":"subscribe","codes":...,"indicators":...}。
    iFinD 推送按代码订阅/退订（无 serial）。"""
    from iFinDPy import THS_QuotesPushing, THS_UnQuotesPushing
    await ws.accept()
    if not _ws_authed(ws):
        await ws.send_json({"event": "error", "msg": "缺少或错误的 key（用 ?key= 传）"})
        await ws.close(code=4401)
        return

    loop = asyncio.get_running_loop()
    q: asyncio.Queue = asyncio.Queue(maxsize=1000)
    subs: list = []   # (codes, indicators) 断开时退订

    def _callback(*cbargs):
        # OnRealTimeCallback(pUserdata, id, sResult, len, errorcode, reserved)
        # sResult 为 JSON 字符串；位置可能因平台略有差异，扫描参数取出可解析的那段。
        payload = None
        for a in cbargs:
            if isinstance(a, (bytes, bytearray)):
                try:
                    a = a.decode("utf-8", "ignore")
                except Exception:
                    continue
            if isinstance(a, str) and a.strip().startswith("{"):
                try:
                    payload = json.loads(a)
                    break
                except Exception:
                    payload = {"raw": a}
        try:
            loop.call_soon_threadsafe(q.put_nowait, {"event": "quote", "data": payload})
        except Exception:
            pass

    pump = asyncio.create_task(_pump(ws, q))
    try:
        while True:
            msg = await ws.receive_text()
            try:
                req = json.loads(msg)
            except Exception:
                await ws.send_json({"event": "error", "msg": "非法 JSON"})
                continue
            action = req.get("action")
            if action == "subscribe":
                codes = req.get("codes", "")
                indicators = req.get("indicators", "")

                def _do_sub():
                    with _lock:
                        _ensure_ths()
                        return THS_QuotesPushing(codes, indicators, _callback)

                r = await loop.run_in_executor(None, _do_sub)
                ec = r.get("errorcode") if isinstance(r, dict) else None
                if ec not in (0, None):
                    await ws.send_json({"event": "error",
                                        "msg": "订阅失败 {} {}".format(ec, r.get("errmsg"))})
                else:
                    subs.append((codes, indicators))
                    await ws.send_json({"event": "subscribed",
                                        "codes": codes, "indicators": indicators})
            elif action == "unsubscribe":
                codes = req.get("codes", "")
                indicators = req.get("indicators", "")
                await loop.run_in_executor(None, lambda: THS_UnQuotesPushing(codes, indicators))
                await ws.send_json({"event": "unsubscribed", "codes": codes})
            else:
                await ws.send_json({"event": "error", "msg": "未知 action：{}".format(action)})
    except WebSocketDisconnect:
        pass
    finally:
        pump.cancel()
        for codes, indicators in subs:
            try:
                await loop.run_in_executor(None, lambda cc=codes, ii=indicators: THS_UnQuotesPushing(cc, ii))
            except Exception:
                pass

