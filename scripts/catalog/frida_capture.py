"""
Frida 驱动:attach 到 WBox,加载 frida_ssl_dump.js,把截获的明文 HTTP
请求/响应落盘到 docs/catalog/_raw/。请求写 *_req.txt,响应原始字节写 *_resp.bin
(响应可能 gzip,后续解压)。同时打印疑似 CG 取树端点。

用法(在装了 frida 的 venv):
    python scripts\\catalog\\frida_capture.py           # attach WBox 默认
    python scripts\\catalog\\frida_capture.py wmain      # 换进程名

停止:Ctrl+C(或后台运行时到时读文件)。
"""
import sys, os, time, frida

PROC = sys.argv[1] if len(sys.argv) > 1 else "WBox"
OUTDIR = os.path.join("docs", "catalog", "_raw")
os.makedirs(OUTDIR, exist_ok=True)
REQ = os.path.join(OUTDIR, "cg_capture_req.txt")
RESP = os.path.join(OUTDIR, "cg_capture_resp.bin")
LOG = os.path.join(OUTDIR, "cg_capture.log")

# 清空旧文件
for p in (REQ, RESP, LOG):
    open(p, "wb").close()

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def on_message(message, data):
    if message.get("type") == "send":
        p = message["payload"]
        t = p.get("t")
        if t == "req" and data:
            with open(REQ, "ab") as f:
                f.write(b"\n===== REQUEST ssl=%s len=%d =====\n" % (p["ssl"].encode(), p["len"]))
                f.write(data)
            # 抽首行 + Host + SessionId 头,实时提示
            head = data[:600].decode("utf-8", "replace")
            first = head.splitlines()[0] if head else ""
            log(f"REQ {first}")
            for ln in head.splitlines():
                if any(k in ln.lower() for k in ("sessionid", "session", "token", "cookie", "authorization")):
                    log(f"   ↳ {ln[:200]}")
        elif t == "resp" and data:
            with open(RESP, "ab") as f:
                f.write(b"\n===== RESPONSE ssl=%s len=%d =====\n" % (p["ssl"].encode(), p["len"]))
                f.write(data)
            head = data[:200].decode("utf-8", "replace").replace("\n", " ")
            log(f"RESP {p['len']}B  {head[:120]}")
        elif t in ("info", "err"):
            log(f"[{t}] {p.get('msg')}")
        elif t == "mods":
            log(f"[mods] TLS相关={p.get('list')}  (总模块数={p.get('total')})")
        elif t == "allmods":
            log(f"[allmods] {p.get('list')}")
        elif t == "exports":
            log(f"[exports] {p.get('mod')} -> {p.get('names')}")
    elif message.get("type") == "error":
        log(f"[frida-error] {message.get('description')}")

def resolve_target(proc):
    if proc.isdigit():
        return int(proc)
    dev = frida.get_local_device()
    for p in dev.enumerate_processes():
        if proc.lower() in (p.name or "").lower():
            return p.pid
    return proc  # 交给 frida.attach 兜底

def main():
    target = resolve_target(PROC)
    log(f"attaching to {PROC} -> {target} ...")
    session = frida.attach(target)
    js = open(os.path.join("scripts", "catalog", "frida_ssl_dump.js"), encoding="utf-8").read()
    script = session.create_script(js)
    script.on("message", on_message)
    script.load()
    dur = int(sys.argv[2]) if len(sys.argv) > 2 else 90
    log(f"已挂钩。现在去 Wind 打开命令生成器、展开几个指标分类。捕获 {dur}s 后自动停止...")
    end = time.time() + dur
    while time.time() < end:
        time.sleep(1)
    log("捕获结束。产物: docs/catalog/_raw/cg_capture_req.txt / _resp.bin / .log")
    try:
        script.unload(); session.detach()
    except Exception:
        pass

if __name__ == "__main__":
    main()
