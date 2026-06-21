"""Track A — 东方财富 EM/Choice 程序化目录榨取。

把 API 层"能枚举"的目录抓成 CSV，落到 docs/catalog/em/。
注意：EM SDK 不提供"全量指标字典"导出接口（厂商只在 Choice 桌面端
超级命令里给完整指标树），所以本脚本只覆盖可枚举的维度：
  1. 板块/指标体系树（sector，从常见板块根码递归）
  2. 资讯板块清单（cfnquery）
  3. 交易日历样本（tradedates，验证可用性）
全量财务/技术/EDB 字段级清单仍需 Choice 桌面端导出（Track B）。

在 .venv-em 下运行：
    .venv-em\\Scripts\\python scripts\\catalog\\extract_em.py
"""
import csv
import os
import sys

# 让脚本能 import 仓库根目录的 em_api
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _ROOT)

from EmQuantAPI import c  # noqa: E402
import em_api as em  # noqa: E402

OUT_DIR = os.path.join(_ROOT, "docs", "catalog", "em")
os.makedirs(OUT_DIR, exist_ok=True)

# 附注9 常见板块代码（指标手册抄录）——作为 sector 递归的根种子
SECTOR_SEEDS = {
    "001004": "全部A股",
    "001005": "上证A股",
    "001006": "深证A股",
    "001010": "创业板",
    "001009": "中小板",
    "001008": "深证主板",
    "001017": "ST",
    "001018": "*ST",
    "001044": "全部A股(非金融石油石化)",
    "001045": "融资融券标的",
    "001046": "可转债标的",
    "001041": "深股通",
    "001038": "沪股通",
    "001047": "沪深股通",
    "009006195": "沪深300成份",
    "009006062": "中证500成份",
    "009007552": "中证1000成份",
    "009007063": "上证50指数成份",
    "009007060": "上证180指数成份",
}


def _write_csv(name, header, rows):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("  wrote {} ({} rows) -> {}".format(name, len(rows), path))
    return path


def extract_news_boards():
    """资讯板块树（cfnquery）——cfn/cnq 资讯订阅可用的板块全集。"""
    print("[1/3] 资讯板块树 cfnquery ...")
    d = c.cfnquery("")
    if d.ErrorCode != 0:
        print("  跳过：cfnquery 失败 {} {}".format(d.ErrorCode, d.ErrorMsg))
        return
    rows = []
    for code in d.Codes:
        vals = d.Data.get(code, [])
        secname = vals[1] if len(vals) > 1 else ""
        psecname = vals[2] if len(vals) > 2 else ""
        rows.append([code, secname, psecname])
    _write_csv("news_boards.csv", ["板块代码", "板块名称", "母板块"], rows)


def extract_sector_constituents():
    """各常见板块/指数成分（sector）——验证体系编码可用 + 给出成分规模。"""
    print("[2/3] 板块成分 sector ...")
    rows = []
    for pukey, name in SECTOR_SEEDS.items():
        try:
            d = c.sector(pukey, "2024-12-31", "Ispandas=0")
            if d.ErrorCode != 0:
                rows.append([pukey, name, "ERR", d.ErrorMsg])
                continue
            sample = ",".join(d.Codes[:3])
            rows.append([pukey, name, len(d.Codes), sample])
        except Exception as e:  # SDK 偶发 C++ 异常
            rows.append([pukey, name, "EXC", str(e)[:60]])
    _write_csv(
        "sector_seeds.csv",
        ["板块代码pukey", "板块名称", "成分数量", "成分样例(前3)"],
        rows,
    )


def extract_edb_field_schema():
    """EDB 字段 schema（附注12 抄录）——edbquery 返回的字段定义。"""
    print("[3/3] EDB 字段 schema（手册抄录）...")
    rows = [
        ["ID", "指标ID", ""],
        ["Name", "指标名称", ""],
        ["Unit", "单位", ""],
        ["Source", "来源", ""],
        ["Region", "国家/地区", ""],
        ["Frequency", "日期频率", "1日 2周 3旬 4半月 5月 6季 7半年 8年 9不定期"],
        ["Startdate", "起始日期", ""],
        ["Enddate", "截止日期", ""],
        ["Updatetime", "更新时间", ""],
    ]
    _write_csv("edb_field_schema.csv", ["字段简称", "中文简称", "备注"], rows)


def main():
    print("=== EM/Choice Track A 目录榨取 ===")
    em._ensure_login()
    try:
        extract_news_boards()
        extract_sector_constituents()
        extract_edb_field_schema()
    finally:
        em.logout()
    print("完成。注意：全量财务/技术/EDB 指标字段级清单需 Choice 桌面端超级命令导出（Track B）。")


if __name__ == "__main__":
    main()
