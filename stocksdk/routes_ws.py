"""WebSocket 实时推送路由：/em/ws、/ths/ws。

真·订阅推送：SDK 回调在后台线程触发，用 loop.call_soon_threadsafe
把数据塞进 asyncio.Queue，再由 pump 协程发给 WS。
注册/退订在 executor 线程里持全局锁执行；推送本身不碰锁。
鉴权走 query 参数 ?key=（WS 不便带请求头）。
"""
import asyncio
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from EmQuantAPI import c

from stocksdk.config import WS_QUEUE_MAXSIZE
from stocksdk.security import ws_authed
from stocksdk.serialize import em_quote_to_dict
from stocksdk.sessions import ensure_em, ensure_ths, lock

router = APIRouter(tags=["WebSocket 推送"])


async def _pump(ws: WebSocket, q: "asyncio.Queue"):
    """从队列取数据推给 WS，直到被取消。"""
    while True:
        item = await q.get()
        await ws.send_json(item)


async def _reject_unauthed(ws: WebSocket) -> bool:
    """未通过鉴权则发错误并关闭，返回 True 表示已拒绝。"""
    if ws_authed(ws):
        return False
    await ws.send_json({"event": "error", "msg": "缺少或错误的 key（用 ?key= 传）"})
    await ws.close(code=4401)
    return True


@router.websocket("/em/ws")
async def em_ws(ws: WebSocket):
    """东财实时行情 WebSocket 推送。连接后发 {"action":"subscribe","codes":...,"indicators":...}。"""
    await ws.accept()
    if await _reject_unauthed(ws):
        return

    loop = asyncio.get_running_loop()
    q: asyncio.Queue = asyncio.Queue(maxsize=WS_QUEUE_MAXSIZE)
    serials: list = []   # 本连接的所有订阅号，断开时统一退订

    def _callback(quantdata):
        # SDK 后台线程触发：跨线程把数据塞进事件循环的队列
        try:
            loop.call_soon_threadsafe(q.put_nowait, em_quote_to_dict(quantdata))
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
                    with lock:
                        ensure_em()
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


@router.websocket("/ths/ws")
async def ths_ws(ws: WebSocket):
    """同花顺实时行情 WebSocket 推送。发 {"action":"subscribe","codes":...,"indicators":...}。
    iFinD 推送按代码订阅/退订（无 serial）。"""
    from iFinDPy import THS_QuotesPushing, THS_UnQuotesPushing
    await ws.accept()
    if await _reject_unauthed(ws):
        return

    loop = asyncio.get_running_loop()
    q: asyncio.Queue = asyncio.Queue(maxsize=WS_QUEUE_MAXSIZE)
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
                    with lock:
                        ensure_ths()
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
