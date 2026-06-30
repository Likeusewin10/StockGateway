"""把 docs/catalog/wind/probed_fields.csv 生成 Wind 字段手册(方案 C 实测版)。

仿 EM/iFinD 手册结构:总览 + 按分类 → 字段表,但明确标注「探测法实测、非全量」。
只收录「有效=是」的字段。

用法:.venv-api\\Scripts\\python scripts\\catalog\\gen_md_wind.py
输出:docs/catalog/Wind指标字段手册.md
"""
import csv
import os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(ROOT, "docs", "catalog", "wind", "probed_fields.csv")
OUT = os.path.join(ROOT, "docs", "catalog", "Wind指标字段手册.md")


def _esc(v):
    return (v or "").replace("|", "\\|").replace("\n", " ").strip()


def _anchor(sect):
    return "分类-" + sect.replace("/", "-").replace(" ", "")


def main():
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f) if r["有效"] == "是"]

    by_sect = OrderedDict()
    for r in rows:
        by_sect.setdefault(r["分类"], []).append(r)

    md = []
    md.append("# 万得 Wind 字段手册（探测法实测版）\n")
    md.append("> 🔴 **口径说明（必读）**：Wind 的全量字段字典被加密锁在本地终端内，"
              "无任何可编程旁路（公网帮助中心只放函数手册、本机不开端口、CDP 被屏蔽、字典文件加密）。"
              "本表是**方案 C 探测法**产物：用一份常用字段候选清单，逐字段调本机 `/wind/wss` 实测，"
              "只保留 Wind 确认存在的字段。**因此这是「经实测验证的常用字段子集」，不是 EM/iFinD 那种全量字典。**\n")
    md.append("> 字段代码可直接用于 `/wind/wsd`（日序列）/ `/wind/wss`（截面）的 `fields` 参数。"
              "部分财务字段取值需在 `options` 带 `rptDate=`/`year=` 等报告期参数（样例值为空即此类）。\n")
    md.append("> 数据来源:WindPy 真机 `w.wss` 探测(经本服务 `/wind/wss`);"
              "种子清单见 `scripts/catalog/wind_field_seeds.txt`,探测器 `scripts/catalog/wind_probe_fields.py`。\n")

    md.append("\n## 总览\n")
    md.append("| 分类 | 字段数 | 跳转 |")
    md.append("|---|---|---|")
    for sect, items in by_sect.items():
        md.append(f"| {sect} | {len(items)} | [↓](#{_anchor(sect)}) |")
    md.append(f"\n**合计 {len(rows)} 个实测有效字段,{len(by_sect)} 个分类。**\n")

    for sect, items in by_sect.items():
        md.append(f'\n<a id="{_anchor(sect)}"></a>')
        md.append(f"\n## {sect}（{len(items)} 个字段）\n")
        md.append("| 字段代码 | 中文名 | 命中品种 | 样例值 |")
        md.append("|---|---|---|---|")
        for r in items:
            md.append("| `{}` | {} | {} | {} |".format(
                _esc(r["字段代码"]), _esc(r["中文名"]),
                _esc(r["命中品种"]), _esc(r["样例值"])))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"生成 {OUT}  ({len(md)} 行,{len(rows)} 字段)")


if __name__ == "__main__":
    main()
