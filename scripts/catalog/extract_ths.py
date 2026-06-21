"""Track A — 同花顺 iFinD 函数/指标参考榨取。

iFinD API 同样不提供"全量指标字典"导出接口（厂商只在 iFinD 桌面端
超级命令里给完整指标树）。本脚本产出 API 层可固化的参考：
  1. 取数函数清单（函数名/用途/签名）——来自 SDK 自省 + 手册
  2. 已知常用指标样例（手册正文出现的）
  3. 连通性校验（登录 + 一次取数，确认账号可用）
全量指标字段级清单仍需 iFinD 桌面端"超级命令/数据接口"导出（Track B）。

在 .venv-ths 下运行：
    .venv-ths\\Scripts\\python scripts\\catalog\\extract_ths.py
"""
import csv
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _ROOT)

import ths_api as ths  # noqa: E402

OUT_DIR = os.path.join(_ROOT, "docs", "catalog", "ths")
os.makedirs(OUT_DIR, exist_ok=True)

# 取数函数清单（手册 + SDK 自省）
FUNCTIONS = [
    ("THS_HistoryQuotes", "历史行情序列", "(codes, indicators, params, begin, end)"),
    ("THS_RealtimeQuotes", "实时行情", "(codes, indicators, params)"),
    ("THS_BasicData", "基础/截面数据", "(codes, indicators, params)"),
    ("THS_DateSequence", "日期序列指标", "(codes, indicators, params, begin, end)"),
    ("THS_DateSerial", "日期截面序列", "(codes, indicators, globalparam, begin, end)"),
    ("THS_DataPool", "数据池(板块成分/指数成分等)", "(poolname, paramname, indicators)"),
    ("THS_EDB", "宏观经济数据(EDB)", "(indicators, param, begin, end)"),
    ("THS_EDBQuery", "EDB 指标明细查询", "(indicators, begin, end)"),
    ("THS_DateQuery", "交易日/节假日查询", "(exchange, params, begin, end)"),
    ("THS_DateOffset", "交易日偏移", "(exchange, params, end)"),
    ("THS_DateCount", "区间交易日计数", "(exchange, params, begin, end)"),
    ("THS_HighFrequenceSequence", "高频(分钟级)序列", "(codes, indicators, params, begin, end)"),
    ("THS_Snapshot", "快照数据", "(codes, indicators, params, begin, end)"),
    ("THS_iwencai", "i问财自然语言选股", "(query, domain)"),
    ("THS_WCQuery", "i问财查询(结构化)", "(query, domain)"),
    ("THS_ReportQuery", "公告/报告查询", "(codes, reqtype, params)"),
    ("THS_DataStatistics", "流量/额度查询", "()"),
    ("THS_Trans2DataFrame", "结果转 DataFrame", "(result)"),
]

# 手册正文出现的常用指标样例（按维度）
INDICATOR_SAMPLES = [
    ("行情", "open;high;low;close;volume;amount", "THS_HistoryQuotes 历史行情"),
    ("实时", "open;high;now;changeRatio;amount", "THS_RealtimeQuotes 实时行情"),
    ("基础", "ths_stock_short_name_stock", "THS_BasicData 证券简称"),
    ("基础", "ths_listed_date_stock", "THS_BasicData 上市日期"),
    ("财务", "ths_total_assets_stock", "THS_BasicData 资产总计(示例)"),
    ("宏观", "M001620326", "THS_EDB EDB 指标ID(示例，需官网命令生成)"),
]


def _write_csv(name, header, rows):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("  wrote {} ({} rows) -> {}".format(name, len(rows), path))
    return path


def extract_functions():
    print("[1/3] 取数函数清单 ...")
    _write_csv("functions.csv", ["函数名", "用途", "签名"], FUNCTIONS)


def extract_indicator_samples():
    print("[2/3] 常用指标样例 ...")
    _write_csv("indicator_samples.csv", ["维度", "指标代码", "来源/说明"], INDICATOR_SAMPLES)


def verify_connectivity():
    """登录 + 一次真实取数，确认测试账号可用（写校验结果）。"""
    print("[3/3] 连通性校验 ...")
    rows = []
    try:
        ths._ensure_login()
        rows.append(["login", "OK", ""])
        df = ths.history("300033.SZ", "close", "2024-01-02", "2024-01-03")
        n = 0 if df is None else len(df)
        rows.append(["history(300033.SZ,close)", "OK", "rows={}".format(n)])
    except Exception as e:
        rows.append(["verify", "FAIL", str(e)[:80]])
    finally:
        ths.logout()
    _write_csv("connectivity.csv", ["检查项", "结果", "备注"], rows)


def main():
    print("=== iFinD Track A 参考榨取 ===")
    extract_functions()
    extract_indicator_samples()
    verify_connectivity()
    print("完成。注意：全量指标字段级清单需 iFinD 桌面端超级命令/数据接口导出（Track B）。")


if __name__ == "__main__":
    main()
