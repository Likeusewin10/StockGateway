"""把 docs/catalog/wind/windpy_fields.csv(5301 个 WindPy 实测认可字段)生成
WindPy 字段手册——这是**真正可直接喂 /wind/wsd、/wind/wss 的命名口径**。

与 gen_md_wind.py(xla Excel 插件口径,9689 字段,仅供查中文名/找指标)区别见手册抬头。
按字段代码首段前缀粗分类。
用法:.venv-api\\Scripts\\python scripts\\catalog\\gen_md_windpy.py
输出:docs/catalog/WindPy字段手册.md
"""
import csv
import os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(ROOT, "docs", "catalog", "wind", "windpy_fields.csv")
OUT = os.path.join(ROOT, "docs", "catalog", "WindPy字段手册.md")

# 首段前缀 → 分类标签(WindPy 去前缀后仍保留的领域前缀)。无前缀/未知归「通用/行情」。
PREFIX = OrderedDict([
    ("cb", "可转债"), ("abs", "ABS资产证券化"), ("fund", "基金"), ("nav", "基金净值"),
    ("mf", "基金"), ("fs", "基金(专项)"), ("ipo", "新股发行"), ("div", "分红"),
    ("est", "盈利预测"), ("west", "一致预期"), ("esg", "ESG"), ("holder", "股东"),
    ("share", "股本"), ("mmf", "货币基金"), ("issue", "发行"), ("rate", "利率/评级"),
    ("yield", "收益率"), ("margin", "融资融券"), ("fa", "财务分析"), ("qfa", "单季财务"),
    ("tech", "技术指标"), ("risk", "风险指标"), ("val", "估值"), ("pe", "估值"),
    ("trade", "交易"), ("sec", "证券基础"), ("bond", "债券"), ("repo", "回购"),
    ("convert", "可转债转股"), ("fut", "期货"), ("opt", "期权"), ("index", "指数"),
])


def _esc(v):
    return (v or "").replace("|", "\\|").replace("\n", " ").strip()


def _cat(code):
    pre = code.split("_")[0]
    return PREFIX.get(pre, "通用/行情/其他")


def _anchor(cat):
    return "分类-" + cat.replace("/", "-").replace("(", "").replace(")", "").replace(" ", "")


def main():
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    by_cat = OrderedDict()
    for _, name in PREFIX.items():
        by_cat.setdefault(name, [])
    by_cat["通用/行情/其他"] = []
    for r in rows:
        by_cat[_cat(r["字段代码"])].append(r)
    by_cat = OrderedDict((k, v) for k, v in by_cat.items() if v)

    md = []
    md.append("# WindPy 字段手册（实测可用）\n")
    md.append("> 共 **{} 个字段**,**经 WindPy `wss` 真机逐字段批量验证认可**(Wind 字典层 "
              "`-40522006 invalid indicators` 是纯字段名级校验,与品种无关)。"
              "**本表字段代码可直接用于 `/wind/wsd`、`/wind/wss`**,是三套 Wind 字段口径里唯一"
              "「拿来即用」的那套。\n".format(len(rows)))
    md.append("> 🔴 **三套 Wind 字段口径区别(必读)**:\n>\n"
              "> | 口径 | 字段数 | 命名样例 | 用途 | 文件 |\n"
              "> |---|---|---|---|---|\n"
              "> | **WindPy 实测(本表)** | 5301 | `close`/`pe_ttm`/`roe` | **可直接喂 `/wind/wss`** | `windpy_fields.csv` |\n"
              "> | Excel 插件(xla) | 9689 | `s_dq_close`/`s_val_pe` | 查中文名/找指标,**不能直接喂 wss** | `xla_fields.csv` / `Wind指标字段手册.md` |\n"
              "> | 探测子集(早期) | 130 | `close`/`open` | 已并入本表 | `probed_fields.csv` |\n>\n"
              "> 本表由 xla 9689 码生成「原码 + 去 1 段前缀 + 去 2 段前缀」候选变体(25683 个),"
              "批量喂 wss、二分定位,留下 5301 个被 Wind 字典认可的名。中文名取生成该名的最短源 xla 码的中文名。\n")
    md.append("> ⚠ **口径残余风险**:去前缀变体的中文名来自 xla 源码,极少数「去前缀后撞名」"
              "的字段,其中文名可能与该 WindPy 名的真实语义略有出入;基础高频字段(行情/估值/财务)已交叉核对无误。"
              "生成脚本 `scripts/catalog/wind_verify_xla_fields.py`、`gen_md_windpy.py`。\n")

    md.append("\n## 总览\n")
    md.append("| 分类 | 字段数 | 跳转 |")
    md.append("|---|---|---|")
    for cat, items in by_cat.items():
        md.append(f"| {cat} | {len(items)} | [↓](#{_anchor(cat)}) |")
    md.append(f"\n**合计 {len(rows)} 个字段,{len(by_cat)} 个分类。**\n")

    for cat, items in by_cat.items():
        items.sort(key=lambda r: r["字段代码"])
        md.append(f'\n<a id="{_anchor(cat)}"></a>')
        md.append(f"\n## {cat}（{len(items)} 个字段）\n")
        md.append("| 字段代码 | 中文名 | 参数 | 来源 |")
        md.append("|---|---|---|---|")
        for r in items:
            md.append("| `{}` | {} | {} | {} |".format(
                _esc(r["字段代码"]), _esc(r["中文名"]),
                _esc(r.get("参数", "")), _esc(r.get("来源", ""))))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"生成 {OUT}  ({len(md)} 行,{len(rows)} 字段,{len(by_cat)} 分类)")


if __name__ == "__main__":
    main()
