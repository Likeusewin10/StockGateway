"""解析 iFinD 命令生成器爬取的 ifind_catalog.json,归一化成每品种一个 CSV。

输入:docs/catalog/_raw/ifind_catalog.json
      结构 {_meta:{types}, index:{type->[节点]}, block:{sector类->[...]}}
输出:docs/catalog/ths/{type}_indicators.csv

叶子判定:children==0 且 idxId 非空且不以 '_' 开头(以 _ 开头的是"全部指标"等虚拟根)。
idxPath 形如 //股票全部指标/股本结构,去掉前导 // 与首段"XX全部指标",得到分类路径。
paramList 是 JSON 串,提炼出可读参数名(去掉每字段通用的"截止日期/单位")。

用法:.venv-api\\Scripts\\python scripts\\catalog\\parse_ifind.py
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "docs", "catalog", "_raw", "ifind_catalog.json")
OUT = os.path.join(ROOT, "docs", "catalog", "ths")
os.makedirs(OUT, exist_ok=True)

HEADER = ["指标代码", "指标中文名", "英文代码", "单位", "分类", "参数", "支持序列"]

# 每字段几乎都有的通用参数,省略不展示(对照 EM 手册的做法)
_COMMON_PARAMS = {"截止日期", "单位", "交易日期", "报告期", "起始日期", "终止日期", "日期"}


def _is_leaf(node):
    idx = str(node.get("idxId", ""))
    return (not node.get("children")) and idx and not idx.startswith("_")


def _category(idx_path):
    """//股票全部指标/股本结构 -> 股本结构 ; 多层用 / 连接,去掉首段'XX全部指标'。"""
    p = (idx_path or "").lstrip("/")
    parts = [s for s in p.split("/") if s]
    if parts and parts[0].endswith("全部指标"):
        parts = parts[1:]
    return " / ".join(parts) if parts else "未分类"


def _params(param_list_str):
    """从 paramList JSON 串提炼有区分度的参数名(去掉通用的日期/单位)。"""
    if not param_list_str:
        return ""
    try:
        plist = json.loads(param_list_str)
    except (ValueError, TypeError):
        return ""
    names = []
    for p in plist:
        name = (p.get("pName") or "").strip()
        if not name or name in _COMMON_PARAMS:
            continue
        names.append(name)
    return "、".join(names)


def main():
    with open(RAW, encoding="utf-8") as f:
        data = json.load(f)

    summary = []
    for typ, nodes in data.get("index", {}).items():
        title = data["_meta"]["types"].get(typ, {}).get("title", typ)
        leaves = [n for n in nodes if _is_leaf(n)]
        # 去重:同 idxId 多路径只留一条(以首次出现为准)
        seen = set()
        rows = []
        for n in leaves:
            code = str(n.get("idxId", ""))
            if code in seen:
                continue
            seen.add(code)
            rows.append([
                code,
                (n.get("idxName") or "").strip(),
                (n.get("idxEnName") or "").strip(),
                (n.get("idxUnit") or "").strip(),
                _category(n.get("idxPath")),
                _params(n.get("paramList")),
                "是" if n.get("dateSequence") else "",
            ])
        # 按分类、代码排序,稳定可读
        rows.sort(key=lambda r: (r[4], r[0]))
        path = os.path.join(OUT, f"{typ}_indicators.csv")
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(HEADER)
            w.writerows(rows)
        summary.append((typ, title, len(rows)))
        print(f"{typ:8s} {title:8s} -> {len(rows):6d} 指标  {path}")

    total = sum(s[2] for s in summary)
    print(f"\n合计 {total} 个去重指标,{len(summary)} 个品种")


if __name__ == "__main__":
    main()
