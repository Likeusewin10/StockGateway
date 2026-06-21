"""把已爬的指标 CSV 生成给客户端用的 Markdown 字段手册。

EM 三类：截面(css)、序列(csd)、专题报表(ctr)。按 品种 → 分类 分组，
每个指标列出 代码 / 中文名 / 单位 / 参数 / 适用范围，供产品设计查阅与调用。

用法：.venv-api\\Scripts\\python scripts\\catalog\\gen_md.py
输出：docs/catalog/东方财富EM指标字段手册.md
"""
import csv
import os
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EM = os.path.join(ROOT, "docs", "catalog", "em")
OUT = os.path.join(ROOT, "docs", "catalog", "东方财富EM指标字段手册.md")

# csd 的“品种id”→可读名（首3位映射，见命令生成器顶层分类）
CSD_VAR = {"110": "序列(全品种通用)"}


def _read(path):
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _esc(v):
    """Markdown 表格转义：竖线与换行。"""
    return (v or "").replace("|", "\\|").replace("\n", " ").strip()


def _section_css(md, rows):
    """截面 css：品种 → 分类 → 指标表。"""
    by_var = OrderedDict()
    for r in rows:
        by_var.setdefault(r["品种"], OrderedDict())
        by_var[r["品种"]].setdefault(r["分类"], []).append(r)
    for var, cats in by_var.items():
        total = sum(len(v) for v in cats.values())
        md.append(f"\n### {var}（{len(cats)} 个分类 / {total} 个指标）\n")
        for cat, items in cats.items():
            md.append(f"\n#### {cat}\n")
            md.append("| 指标代码 | 中文名 | 单位 | 参数 | 适用范围 |")
            md.append("|---|---|---|---|---|")
            for r in items:
                md.append("| `{}` | {} | {} | {} | {} |".format(
                    _esc(r["指标代码"]), _esc(r["指标中文名"]),
                    _esc(r["单位"]), _esc(r["参数"]), _esc(r["适用范围"])))


def _section_ctr(md, rows):
    """专题报表 ctr：品种 → 报表 → 字段表。"""
    by_var = OrderedDict()
    for r in rows:
        by_var.setdefault(r["品种"], OrderedDict())
        key = (r["报表名"], r["报表代码CtrName"])
        by_var[r["品种"]].setdefault(key, []).append(r)
    for var, reports in by_var.items():
        md.append(f"\n### {var}（{len(reports)} 张报表）\n")
        for (rname, ccode), fields in reports.items():
            md.append(f"\n#### {rname}  `{ccode}`（{len(fields)} 字段）\n")
            md.append("| 字段代码 | 字段中文名 |")
            md.append("|---|---|")
            for r in fields:
                md.append("| `{}` | {} |".format(_esc(r["字段代码"]), _esc(r["字段中文名"])))


def _section_csd(md, rows):
    """序列 csd：按适用范围分组（品种id 不直观，用适用范围更可读）。"""
    by_scope = OrderedDict()
    for r in rows:
        by_scope.setdefault(r["适用范围"] or "通用", []).append(r)
    for scope, items in by_scope.items():
        md.append(f"\n### {scope}（{len(items)} 个序列指标）\n")
        md.append("| 指标代码 | 中文名 | 单位 | 参数 |")
        md.append("|---|---|---|---|")
        for r in items:
            md.append("| `{}` | {} | {} | {} |".format(
                _esc(r["指标代码"]), _esc(r["指标中文名"]),
                _esc(r["单位"]), _esc(r["参数"])))


def main():
    css = _read(os.path.join(EM, "css_indicators.csv"))
    ctr = _read(os.path.join(EM, "ctr_indicators.csv"))
    csd = _read(os.path.join(EM, "csd_indicators.csv"))

    md = []
    md.append("# 东方财富 EM / Choice 指标字段手册\n")
    md.append("> 供产品设计与接口调用查阅。每个指标的「指标代码」可直接用于对应取数函数。\n")
    md.append("> 数据来源：东方财富量化接口命令生成器（quantapi.eastmoney.com）。\n")
    md.append("\n## 总览\n")
    md.append("| 类别 | 取数函数 | 数量 | 说明 |")
    md.append("|---|---|---|---|")
    md.append(f"| 截面数据 | `c.css(codes, indicators, options)` | {len(css)} | 某时点的基本资料/财务/估值等 |")
    md.append(f"| 序列数据 | `c.csd(codes, indicators, start, end, options)` | {len(csd)} | 时间区间的行情/估值序列 |")
    md.append(f"| 专题报表 | `c.ctr(ctrName, indicators, options)` | {len(ctr)} | 报表型数据（三大财报等） |")
    md.append(f"\n**合计约 {len(css)+len(csd)+len(ctr)} 个字段。**\n")
    md.append("\n> 宏观经济库（EDB，GDP/CPI/M2/利率等数万条时间序列）暂未纳入，"
              "如需按领域单独导出请说明。\n")

    md.append("\n---\n\n# 一、截面数据（CSS）\n")
    _section_css(md, css)
    md.append("\n---\n\n# 二、序列数据（CSD）\n")
    _section_csd(md, csd)
    md.append("\n---\n\n# 三、专题报表（CTR）\n")
    _section_ctr(md, ctr)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print("生成 {} （{} 行）".format(OUT, len(md)))


if __name__ == "__main__":
    main()
