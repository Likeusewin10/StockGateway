"""
解析 Fiddler .saz 抓包存档,抽出所有到 Wind 服务器(114.80.154.45 等)的
请求 URL / 请求头(含 SessionId)/ 响应 JSON,定位命令生成器(CG)取字段树的端点。

用法:
    .venv-api\\Scripts\\python.exe scripts\\catalog\\parse_wind_saz.py <抓包.saz>

.saz 本质是 zip:raw/  下每个会话有 _c.txt(请求头)_s.txt(响应头)_m.xml(元数据),
响应体在 _s.txt 头之后。本脚本零三方依赖(标准库 zipfile)。
"""
import sys, zipfile, re, json, os

WIND_HOSTS = ("114.80.154.45", "wind.com.cn")
# 命令生成器取树最可能的路径关键词(据侦察:非 ApiHelpCenter/getMenus 那套死路)
TREE_HINTS = ("indicator", "field", "tree", "child", "node", "category",
              "builder", "codegen", "command", "getlist", "menu", "leaf",
              "wss", "wsd", "param")

def split_headers_body(raw: bytes):
    idx = raw.find(b"\r\n\r\n")
    if idx < 0:
        return raw.decode("utf-8", "replace"), b""
    return raw[:idx].decode("utf-8", "replace"), raw[idx + 4:]

def looks_like_field_json(body: bytes) -> bool:
    txt = body[:4000].decode("utf-8", "replace").lower()
    return any(h in txt for h in ("indicator", "字段", "s_dq_", "sec_name",
                                  "收盘", "wsd", "wss", "\"fields\"", "funcname"))

def main(saz_path: str):
    if not os.path.exists(saz_path):
        print(f"[!] 找不到文件: {saz_path}"); sys.exit(1)
    z = zipfile.ZipFile(saz_path)
    # 会话号 -> {c: bytes, s: bytes}
    sessions = {}
    for name in z.namelist():
        m = re.match(r"raw/(\d+)_([cs])\.txt$", name)
        if not m:
            continue
        sessions.setdefault(m.group(1), {})[m.group(2)] = z.read(name)

    print(f"[i] 会话总数: {len(sessions)}\n")
    hits = []
    for sid in sorted(sessions, key=int):
        pair = sessions[sid]
        if "c" not in pair:
            continue
        req_head, _ = split_headers_body(pair["c"])
        first = req_head.splitlines()[0] if req_head else ""
        if not any(h in req_head for h in WIND_HOSTS):
            continue
        url = first
        low = req_head.lower()
        is_tree = any(h in low for h in TREE_HINTS)
        resp_head, resp_body = ("", b"")
        if "s" in pair:
            resp_head, resp_body = split_headers_body(pair["s"])
        field_json = looks_like_field_json(resp_body) if resp_body else False
        if is_tree or field_json:
            # 抽 SessionId / 关键请求头
            sess = re.findall(r"(?i)(sessionid|session|wsessionid|token|authorization)\s*:\s*(\S+)", req_head)
            hits.append((sid, url, sess, field_json, len(resp_body), resp_body[:600]))

    if not hits:
        print("[!] 没找到明显的字段树请求。把 .saz 里到 114.80.154.45 的全部会话列出来人工看:")
        for sid in sorted(sessions, key=int):
            rh, _ = split_headers_body(sessions[sid].get("c", b""))
            if any(h in rh for h in WIND_HOSTS):
                print("   ", rh.splitlines()[0] if rh else sid)
        return

    print(f"[✓] 命中 {len(hits)} 个疑似字段树/含字段 JSON 的会话:\n")
    for sid, url, sess, fj, blen, preview in hits:
        print("=" * 70)
        print(f"会话#{sid}  {'★含字段JSON' if fj else ''}  响应体 {blen}B")
        print(f"  {url}")
        if sess:
            print(f"  鉴权头: {sess}")
        print(f"  响应预览: {preview.decode('utf-8','replace')[:400]}")
    print("\n[下一步] 把上面 ★ 的 URL 端点模板 + 鉴权头 填进 wind_cg_crawl.py 递归爬全树")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    main(sys.argv[1])
