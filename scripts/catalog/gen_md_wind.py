"""把 docs/catalog/wind/xla_fields.csv(方法A,WindFunc.xla 提取的全量字段)
生成 Wind 字段手册。按字段代码前缀归类(Wind 命名体系:s_证券/f_基金/b_债券…)。

用法:.venv-api\\Scripts\\python scripts\\catalog\\gen_md_wind.py
输出:docs/catalog/Wind指标字段手册.md
"""
import csv
import os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(ROOT, "docs", "catalog", "wind", "xla_fields.csv")
OUT = os.path.join(ROOT, "docs", "catalog", "Wind指标字段手册.md")

# 前缀 → 品种/分类(Wind 字段命名体系)
PREFIX = OrderedDict([
    ("s", "证券(股票/通用)"), ("f", "基金"), ("b", "债券"), ("cb", "可转债"),
    ("hks", "港股"), ("tws", "台股"), ("w", "通用/指数"), ("fs", "基金(专项)"),
    ("i", "指数"), ("fut", "期货"), ("fa", "财务分析"), ("o", "期权"),
    ("his", "历史行情"), ("mrg", "融资融券"), ("qfa", "单季财务"),
])
# 非字段的辅助函数(VBA 内部),排除
SKIP = {"moveoptionalparam", "windcodevals", "windcodexy", "getvaliddate",
        "getvalidafterdate", "getvalidcurtype", "getvaliddbl", "getyear",
        "getguidcode", "selfwrittencode", "prewindcode"}


def _esc(v):
    return (v or "").replace("|", "\\|").replace("\n", " ").strip()


def _cat(code):
    pre = code.split("_")[0]
    if pre in PREFIX:
        return PREFIX[pre]
    return "技术指标/其他"


def _anchor(cat):
    return "分类-" + cat.replace("/", "-").replace("(", "").replace(")", "").replace(" ", "")


def main():
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f) if r["字段代码"] not in SKIP]

    by_cat = OrderedDict()
    # 先按 PREFIX 顺序建桶,再归入
    for _, name in PREFIX.items():
        by_cat.setdefault(name, [])
    by_cat["技术指标/其他"] = []
    for r in rows:
        by_cat[_cat(r["字段代码"])].append(r)
    by_cat = OrderedDict((k, v) for k, v in by_cat.items() if v)

    md = []
    md.append("# 万得 Wind 字段手册（Excel 插件 xla 口径 / 指标索引）\n")
    md.append("> ⚠ **本表不是 WindPy 可直接调用的字段表**——要喂 `/wind/wsd`、`/wind/wss` 请用 "
              "[`WindPy字段手册.md`](WindPy字段手册.md)（5301 个实测可用名）。本表是 **Excel 插件命名口径**"
              "(`s_dq_close`/`s_val_pe`/`s_fa_roe_ttm`,带品种/类别前缀),仅用于**查中文名、找指标、做产品设计**。\n")
    md.append("> 共 **{} 个字段**,从 Wind 金融终端 Excel 插件 `WindFunc.xla`(函数向导)"
              "解析提取(OLE2 复合文档 → MS-OVBA 解压 VBA 源码 → 按 `'中文名,字段代码` + Function 签名抽取)。\n".format(len(rows)))
    md.append("> 🔴 **三套 Wind 字段口径(必读)**:① **WindPy 实测可用**(5301,`close`,见 `WindPy字段手册.md`,**可直接喂 wss**);"
              "② **本表 Excel 插件 xla**(9689,`s_dq_close`,**查指标用,不能直接喂 wss**);③ 探测子集(130,已并入①)。"
              "本表 9689 码经「原码 + 去前缀变体」批量喂 wss 验证,仅 113 个原码 + 去前缀后共 5301 个被 WindPy 字典认可——"
              "故 **xla 9689 ≠ WindPy 全集**,二者是不同命名体系。\n")
    md.append("> 「参数」列为该字段在 `options`/调用里可带的设置项(如报告期 `rptDate`/`year`、币种等)。"
              "来源:`DataBrowse/XLA/WindFunc.xla`;提取脚本 `scripts/catalog/extract_wind_xla.py`。\n")

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
        md.append("| 字段代码 | 中文名 | 参数 |")
        md.append("|---|---|---|")
        for r in items:
            md.append("| `{}` | {} | {} |".format(
                _esc(r["字段代码"]), _esc(r["中文名"]), _esc(r.get("参数", ""))))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"生成 {OUT}  ({len(md)} 行,{len(rows)} 字段,{len(by_cat)} 分类)")


if __name__ == "__main__":
    main()
