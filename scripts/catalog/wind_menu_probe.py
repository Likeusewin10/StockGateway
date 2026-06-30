"""Wind w.menu() 深探 —— 摸清触发条件(c_menu 返回码 / 不同参数 / 更长等待)。

第一版 dump 收到 0 回调。可能:① menu 弹 GUI 不推数据;② 需特定 menu 参数;
③ 回调更晚到/需消息循环。本脚本逐项验证。
用法:.venv-wind\\Scripts\\python scripts\\catalog\\wind_menu_probe.py
"""
import os
import threading
import time

from WindPy import w, c_MenuCallbackType   # noqa: E402

_events = []
_lock = threading.Lock()


def _cb(state, reqid, errorid, indata, outPy):
    ev = {"state": int(state), "reqid": int(reqid), "errorid": int(errorid),
          "indata": str(indata)[:200] if indata is not None else None}
    try:
        if outPy:
            out = w.WindData()
            out.set(outPy, 3, asdate=True)
            ev["fields"] = [str(x) for x in getattr(out, "Fields", [])][:10]
            ev["codes"] = [str(x) for x in getattr(out, "Codes", [])][:10]
            ev["data0"] = str(getattr(out, "Data", [])[:2])[:200]
    except Exception as e:  # noqa: BLE001
        ev["err"] = str(e)
    with _lock:
        _events.append(ev)
    print(f"  >> CB state={ev['state']} reqid={ev['reqid']} indata={ev['indata']!r}")
    return 0


def main():
    r = w.start(waitTime=60)
    print(f"start ErrorCode={getattr(r, 'ErrorCode', '?')}")

    cb = c_MenuCallbackType(_cb)
    globals()["_cb_ref"] = cb
    w.c_setMenuCallback(cb)

    # c_menu 直接拿返回码(menu() 包装函数吞了返回值)
    for arg in ["", "wsd", "wss", "Sector", "root", "0"]:
        with _lock:
            before = len(_events)
        rc = w.c_menu(arg)
        print(f"c_menu({arg!r}) rc={rc}")
        time.sleep(3)
        with _lock:
            after = len(_events)
        print(f"  -> 该参数新增 {after - before} 回调")

    print("再等 10s 收尾...")
    time.sleep(10)
    with _lock:
        print(f"总计 {len(_events)} 回调事件")


if __name__ == "__main__":
    main()
