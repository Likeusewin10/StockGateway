"""把 docs/catalog/ths/*.csv 生成给客户用的 Markdown 字段手册。

仿东方财富版结构:总览表 + 按品种 → 分类 → 指标表。
每个指标列出 代码 / 中文名 / 英文代码 / 单位 / 参数 / 支持序列,供产品设计查阅与调用。

用法:.venv-api\\Scripts\\python scripts\\catalog\\gen_md_ifind.py
输出:docs/catalog/同花顺iFinD指标字段手册.md
"""
import csv
import os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
THS = os.path.join(ROOT, "docs", "catalog", "ths")
OUT = os.path.join(ROOT, "docs", "catalog", "同花顺iFinD指标字段手册.md")

# 品种展示顺序与可读名(对照命令生成器顶层)
TYPE_ORDER = [
    ("stk", "A股股票"), ("bond", "债券"), ("fund", "基金理财"),
    ("index", "指数"), ("company", "企业"), ("global", "全球股票"),
    ("hk", "港股"), ("usk", "美股"), ("uk", "英股"),
    ("future", "期货"), ("option", "期权"), ("spot", "现货"),
    ("fxrate", "外汇"),
]


def _read(typ):
    path = os.path.join(THS, f"{typ}_indicators.csv")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _esc(v):
    return (v or "").replace("|", "\\|").replace("\n", " ").strip()


def _anchor(typ):
    return f"品种-{typ}"


def _section(md, typ, title, rows):
    """单品种:按分类(一级)分组 → 指标表。"""
    by_cat = OrderedDict()
    for r in rows:
        cat = r["分类"] or "未分类"
        by_cat.setdefault(cat, []).append(r)
    md.append(f'\n<a id="{_anchor(typ)}"></a>')
    md.append(f"\n## {title}（{len(by_cat)} 个分类 / {len(rows)} 个指标）\n")
    for cat, items in by_cat.items():
        md.append(f"\n### {cat}\n")
        md.append("| 指标代码 | 中文名 | 英文代码 | 单位 | 参数 | 序列 |")
        md.append("|---|---|---|---|---|---|")
        for r in items:
            md.append("| `{}` | {} | `{}` | {} | {} | {} |".format(
                _esc(r["指标代码"]), _esc(r["指标中文名"]), _esc(r["英文代码"]),
                _esc(r["单位"]), _esc(r["参数"]), _esc(r.get("支持序列", ""))))


def main():
    loaded = [(t, n, _read(t)) for t, n in TYPE_ORDER]
    loaded = [(t, n, rows) for t, n, rows in loaded if rows]
    total = sum(len(rows) for _, _, rows in loaded)

    md = []
    md.append("# 同花顺 iFinD 指标字段手册\n")
    md.append("> 供产品设计与接口调用查阅。「指标代码」(数字)与「英文代码」(ths_ 前缀)"
              "均可用于 `THS_BasicData` / `THS_HistoryQuotes` 等取数函数。\n")
    md.append("> 数据来源:同花顺数据接口命令生成器（quantapi.51ifind.com，超级命令后台接口全量抓取）。\n")
    md.append("> 「序列」列为「是」表示该指标支持按日期序列取数(`THS_DateSerial` / `THS_HistoryQuotes`)。\n")

    md.append("\n## 总览\n")
    md.append("| 品种 | 指标数 | 跳转 |")
    md.append("|---|---|---|")
    for t, n, rows in loaded:
        md.append(f"| {n} | {len(rows)} | [↓](#{_anchor(t)}) |")
    md.append(f"\n**合计 {total} 个指标(已按指标代码去重),覆盖 {len(loaded)} 个品种。**\n")
    md.append("\n> 板块类指标(沪深/美股/港股板块)与宏观经济库(EDB)为独立体系,"
              "原始数据已抓取于 `docs/catalog/_raw/ifind_catalog.json` 的 `block` 段,如需成册请说明。\n")

    for t, n, rows in loaded:
        md.append("\n---")
        _section(md, t, n, rows)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"生成 {OUT}  ({len(md)} 行,{total} 指标)")


if __name__ == "__main__":
    main()
