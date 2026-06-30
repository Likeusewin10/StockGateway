"""Wind API 帮助中心(公网)全量文档爬虫 —— catalog 路①。

数据来源:https://wx.wind.com.cn/ApiHelpCenter (免登录,无反爬,服务器侧可直接抓)。
两个后台接口(树状,递归):
  GET /web/apiRefHelp/getMenus?lang=zh-CN            -> 菜单骨架(102 节点,无正文)
  GET /web/apiRefHelp/getListByParentId/{id}?local=zh-CN
       -> 该 parentId 下子节点,**子节点带 jsonData 正文**(notebook/markdown)

策略:从 getMenus 的全部节点 BFS,逐个 getListByParentId 展开,收集返回子节点
(含 jsonData),并把有子节点的继续入队,直到无新节点。去重靠 node id。

产出:docs/catalog/_raw/wind_help.json(已 gitignore)
  结构 {_meta:{ts,base}, nodes:{id->{id,parentId,title,jsonData,htmlData,textData}}}

仿 scripts/catalog/ifind_crawl.js 的递归思路,但纯 stdlib(urllib)、服务器侧、无登录态。
用法:.venv-api\\Scripts\\python scripts\\catalog\\wind_help_crawl.py
"""
import gzip
import json
import os
import time
import urllib.request

BASE = "https://wx.wind.com.cn/ApiHelpCenter/web/apiRefHelp"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DIR = os.path.join(ROOT, "docs", "catalog", "_raw")
OUT = os.path.join(RAW_DIR, "wind_help.json")

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip",
}


def _get(url, retries=3):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=_HEADERS)
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                return json.loads(raw.decode("utf-8"))
        except Exception as e:  # noqa: BLE001 — 网络抖动重试
            last = e
            time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(f"GET 失败 {url}: {last}")


def _node(n):
    return {
        "id": n.get("id"),
        "parentId": n.get("parentId"),
        "title": n.get("title"),
        "jsonData": n.get("jsonData"),
        "htmlData": n.get("htmlData"),
        "textData": n.get("textData"),
    }


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    print("[1/2] 取菜单骨架 getMenus ...")
    menus = _get(f"{BASE}/getMenus?lang=zh-CN")["data"]
    print(f"  菜单节点 {len(menus)}")

    nodes = {}            # id -> node(含正文)
    for m in menus:       # 先把骨架节点收下(正文待 getListByParentId 补)
        nodes[m["id"]] = _node(m)

    print("[2/2] BFS 递归 getListByParentId 取正文 ...")
    queue = [m["id"] for m in menus] + ["0"]   # 含根 '0',兜底顶层
    seen_expand = set()
    while queue:
        pid = queue.pop(0)
        if pid in seen_expand:
            continue
        seen_expand.add(pid)
        try:
            children = _get(f"{BASE}/getListByParentId/{pid}?local=zh-CN").get("data") or []
        except RuntimeError as e:
            print(f"  跳过 {pid[:8]}: {e}")
            continue
        for c in children:
            cid = c.get("id")
            if not cid:
                continue
            # 子节点带正文,覆盖骨架占位
            if c.get("jsonData") or c.get("htmlData") or cid not in nodes:
                nodes[cid] = _node(c)
            if cid not in seen_expand:
                queue.append(cid)
        time.sleep(0.03)
        if len(seen_expand) % 25 == 0:
            withc = sum(1 for n in nodes.values() if n.get("jsonData"))
            print(f"  已展开 {len(seen_expand)} 节点,累计 {len(nodes)} 节点(其中 {withc} 有正文)")

    withc = sum(1 for n in nodes.values() if n.get("jsonData"))
    catalog = {"_meta": {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "base": BASE},
               "nodes": nodes}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False)
    print(f"\n完成:{len(nodes)} 节点(其中 {withc} 有正文) -> {OUT}")


if __name__ == "__main__":
    main()
