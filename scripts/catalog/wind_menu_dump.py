"""Wind w.menu() 回调原始结构 dump —— 探明字段树格式(第一步,非归一化)。

目标:override WindPy 默认 MenuCallback,调 w.menu(),捕获回调推回的所有节点
(state/reqid/errorid/indata 字符串/apiout→WindData 的 Codes/Fields/Times/Data),
原样 dump 成 JSON,用于搞清数据格式,再决定如何递归展开成完整字段树。

⚠ 真机脚本:须在 .venv-wind 跑,Wind 终端须已登录。
  WindPy 连的是本机终端(WBox),与 8000 服务的 WindPy 会话是两个本地 API 客户端,
  正常可共存(同 Excel 插件 + WindPy);若服务会话被扰,其 wind_exec 会自愈重登。

用法:.venv-wind\\Scripts\\python scripts\\catalog\\wind_menu_dump.py [menu_id]
  不带参 = 调 w.menu("")(根);带参 = 调 w.menu(menu_id)(展开某节点)。
"""
import ctypes
import json
import os
import sys
import threading
import time

from WindPy import w, c_MenuCallbackType, c_apiout   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(ROOT, "docs", "catalog", "_raw")
os.makedirs(OUT_DIR, exist_ok=True)

# 捕获到的所有回调事件(线程安全)。
_events = []
_lock = threading.Lock()
_done = threading.Event()


def _winddata_to_dict(out):
    """WindData → 朴素 dict(只取 JSON 友好字段)。"""
    try:
        return {
            "ErrorCode": getattr(out, "ErrorCode", None),
            "StateCode": getattr(out, "StateCode", None),
            "RequestID": getattr(out, "RequestID", None),
            "Codes": [str(x) for x in getattr(out, "Codes", [])],
            "Fields": [str(x) for x in getattr(out, "Fields", [])],
            "Times": [str(x) for x in getattr(out, "Times", [])],
            # Data 可能是嵌套 list,逐项 str 化防 datetime/None 序列化炸裂。
            "Data": [[str(v) for v in row] if isinstance(row, list) else str(row)
                     for row in getattr(out, "Data", [])],
        }
    except Exception as e:  # noqa: BLE001
        return {"_parse_error": str(e)}


def _menu_callback(state, reqid, errorid, indata, outPy):
    """自定义 menu 回调:捕获每一次推送。签名见 WindPy.py c_MenuCallbackType。

    state: 1=首条/中间? 2=结束 3=? 4=? (按默认实现:1 print indata,2/3 注册子回调,4 忽略)
    indata: c_wchar_p 字符串(节点描述,默认实现直接 print)
    outPy: POINTER(c_apiout),含结构化 payload(末态时 set 成 WindData)
    """
    ev = {"state": int(state), "reqid": int(reqid), "errorid": int(errorid),
          "indata": indata if indata is not None else None}
    try:
        if outPy:
            out = w.WindData()
            out.set(outPy, 3, asdate=True)
            ev["winddata"] = _winddata_to_dict(out)
            # 不在这里 free——交给 WindPy 默认流程?为安全,这里不 free,避免双重释放。
    except Exception as e:  # noqa: BLE001
        ev["winddata_error"] = str(e)
    with _lock:
        _events.append(ev)
    # state==2 通常表示一组结束,放行主线程(但 menu 可能多组,故只做提示不强行 set)。
    if int(state) == 2:
        _done.set()
    return 0


def main():
    menu_id = sys.argv[1] if len(sys.argv) > 1 else ""
    print(f"[1] w.start() 连接本机 Wind 终端 ...")
    r = w.start(waitTime=60)
    print(f"    start ErrorCode={getattr(r, 'ErrorCode', '?')} Data={getattr(r, 'Data', '')}")
    if getattr(r, "ErrorCode", -1) != 0 or not w.isconnected():
        raise SystemExit(f"Wind 未连上,无法 dump。ErrorCode={getattr(r, 'ErrorCode', '?')}")

    # override 默认 menu 回调(必须保留强引用,否则 ctypes GC 掉导致崩溃)。
    cb = c_MenuCallbackType(_menu_callback)
    globals()["_cb_ref"] = cb   # 强引用钉住
    print(f"[2] 安装自定义 MenuCallback,调 w.menu({menu_id!r}) ...")
    w.c_setMenuCallback(cb)
    w.menu(menu_id)

    # menu 异步,回调在后台线程到达,等几秒收集。
    print("[3] 等待回调(最多 15s)...")
    for _ in range(15):
        time.sleep(1)
        with _lock:
            n = len(_events)
        if _done.is_set() and n > 0:
            time.sleep(2)   # 再多收 2s 防漏后续组
            break
    with _lock:
        snapshot = list(_events)
    print(f"[4] 收到 {len(snapshot)} 个回调事件")

    out_path = os.path.join(OUT_DIR, f"wind_menu_dump_{menu_id or 'root'}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"[5] 已写 {out_path}")

    # 控制台速览前几条
    for ev in snapshot[:8]:
        print(f"  state={ev['state']} reqid={ev['reqid']} err={ev['errorid']} "
              f"indata={str(ev.get('indata'))[:120]!r}")
        wd = ev.get("winddata")
        if wd and (wd.get("Codes") or wd.get("Fields") or wd.get("Data")):
            print(f"    Codes={wd['Codes'][:5]} Fields={wd['Fields'][:5]} "
                  f"Data[0:2]={wd['Data'][:2]}")


if __name__ == "__main__":
    main()
