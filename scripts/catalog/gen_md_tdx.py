# -*- coding: utf-8 -*-
"""tdx_fields.csv -> 通达信TDX字段手册.md,按接口分组(入参表+返回字段表)。"""
import csv, io
from collections import OrderedDict

CSV = "docs/catalog/tdx/tdx_fields.csv"
MD = "docs/catalog/tdx/通达信TDX字段手册.md"

# 接口展示顺序与中文名(取数->财务/经济->板块->交易->公式->常量)
IFACE_CN = OrderedDict([
    ("get_market_data", "K线行情"), ("get_market_snapshot", "行情快照"),
    ("get_stock_info", "股票基础信息"), ("get_more_info", "更多股票信息"),
    ("get_pricevol", "量价数据"), ("get_divid_factors", "除权因子"),
    ("get_relation", "关联品种"), ("get_ipo_info", "新股IPO信息"),
    ("get_gb_info", "股本信息"), ("get_gb_info_by_date", "指定日期股本"),
    ("get_match_stkinfo", "证券信息检索"), ("get_report_data", "行情订阅推送"),
    ("get_trading_dates", "交易日历"), ("get_trackzs_etf_info", "跟踪指数ETF"),
    ("get_kzz_info", "可转债信息"),
    ("get_financial_data", "专业财务数据(FN指标)"), ("get_financial_data_by_date", "指定日期财务"),
    ("get_gp_one_data", "股票单个财务数据"),
    ("get_gpjy_value", "股票经济指标"), ("get_gpjy_value_by_date", "指定日期股票经济指标"),
    ("get_bkjy_value", "板块经济指标"), ("get_bkjy_value_by_date", "指定日期板块经济指标"),
    ("get_scjy_value", "市场经济指标(SC指标)"), ("get_scjy_value_by_date", "指定日期市场经济指标"),
    ("get_stock_list", "股票列表"), ("get_sector_list", "板块列表"),
    ("get_stock_list_in_sector", "板块成分股"), ("send_user_block", "自选/板块写入"),
    ("stock_account", "获取资金账户句柄"), ("query_stock_asset", "查询账户资产"),
    ("query_stock_orders", "查询委托"), ("query_stock_positions", "查询持仓"),
    ("order_stock", "下单"), ("cancel_order_stock", "撤单"),
    ("send_message", "发送消息"), ("send_warn", "发送预警"), ("send_file", "发送文件"),
    ("send_bt_data", "回测数据"), ("refresh_cache", "刷新缓存"), ("refresh_kline", "刷新K线"),
    ("exec_to_tdx", "执行到客户端"),
    ("formula_get_all", "公式列表"), ("formula_get_info", "公式信息"),
    ("formula_format_data", "公式格式化"), ("formula_set_data", "公式写数据"),
    ("formula_set_data_info", "公式数据信息"), ("formula_zb", "公式指标"),
    ("formula_process_mul_zb", "批量指标计算"),
    ("常量枚举", "常量枚举(市场/交易/委托状态)"),
])

def esc(s):
    return (s or "").replace("|", "\|").replace("\n", " ")

rows = list(csv.DictReader(io.open(CSV, encoding="utf-8-sig")))
by = OrderedDict()
for r in rows:
    by.setdefault(r["interface"], []).append(r)

total = len(rows)
n_if = len(by)
lines = []
lines.append("# 通达信 TDX(TdxQuant)字段手册\n")
lines.append("> **合法来源**:官方随终端附带的《TdxQuant接口说明文档》(231页 PDF),")
lines.append("> 用 PyMuPDF `find_tables()` 结构化抽取,**非爬取、非指标树遍历**(零封控风险)。")
lines.append("> 生成脚本:`scripts/catalog/extract_tdx.py` + `gen_md_tdx.py`;原始 PDF 见 `docs/catalog/tdx/_raw/`。\n")
lines.append(f"- 覆盖接口:**{n_if}** 个  字段/参数行:**{total}** 条")
lines.append("- `kind=PARAM` 为入参,`kind=RETURN` 为返回字段/常量")
lines.append("- **代码格式** `600519.SH`,**日期** `YYYYMMDD`(与 EM/iFinD/Wind 的 `YYYY-MM-DD` 不同)")
lines.append("- 财务/经济类(FN/SC 指标)需先在客户端**下载对应数据包**才能取数\n")
lines.append("---\n")

# 目录
lines.append("## 目录\n")
for iface in list(IFACE_CN) + [k for k in by if k not in IFACE_CN]:
    if iface in by:
        cn = IFACE_CN.get(iface, "")
        lines.append(f"- [`{iface}`](#{iface.replace('_','')}) {cn} — {len(by[iface])} 项")
lines.append("")

# 各接口
ordered = [k for k in IFACE_CN if k in by] + [k for k in by if k not in IFACE_CN]
for iface in ordered:
    recs = by[iface]
    cn = IFACE_CN.get(iface, "")
    anchor = iface.replace('_', '')
    lines.append(f'\n## <a id="{anchor}"></a>`{iface}` {cn}\n')
    params = [r for r in recs if r["kind"] == "PARAM"]
    rets = [r for r in recs if r["kind"] == "RETURN"]
    if params:
        lines.append("**入参**\n")
        lines.append("| 参数 | 必选 | 类型 | 说明 |")
        lines.append("|---|---|---|---|")
        for r in params:
            lines.append(f"| `{esc(r['field'])}` | {esc(r['flag'])} | {esc(r['dtype'])} | {esc(r['desc'])} |")
        lines.append("")
    if rets:
        has_flag = any(r["flag"] for r in rets)
        has_val = any(r["value"] for r in rets)
        lines.append("**返回字段**\n")
        if has_val:
            lines.append("| 字段 | 类型 | 取值 | 说明 |")
            lines.append("|---|---|---|---|")
            for r in rets:
                lines.append(f"| `{esc(r['field'])}` | {esc(r['dtype'])} | {esc(r['value'])} | {esc(r['desc'])} |")
        elif has_flag:
            lines.append("| 字段 | 默认返回 | 类型 | 说明 |")
            lines.append("|---|---|---|---|")
            for r in rets:
                lines.append(f"| `{esc(r['field'])}` | {esc(r['flag'])} | {esc(r['dtype'])} | {esc(r['desc'])} |")
        else:
            lines.append("| 字段 | 类型 | 说明 |")
            lines.append("|---|---|---|")
            for r in rets:
                lines.append(f"| `{esc(r['field'])}` | {esc(r['dtype'])} | {esc(r['desc'])} |")
        lines.append("")

io.open(MD, "w", encoding="utf-8").write("\n".join(lines))
print(f"生成 {MD}:{n_if} 接口 / {total} 行")
