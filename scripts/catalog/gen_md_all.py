# -*- coding: utf-8 -*-
"""把 docs/catalog/ 下四源(EM/iFinD/Wind/TDX)的全部字段 CSV 汇总成一个 Markdown 总表。

结构:总览统计表 + 四大源分节。每源下按其自然主键(品种/分类/接口)分组成表,
列出字段代码 / 中文名 / 单位 / 参数 等,供消费方产品设计与取数查阅。

这是把已有各源独立手册(东方财富EM/同花顺iFinD/Wind/WindPy/通达信TDX)合并为
单一入口的「全字段字典总表」,内容与各源 CSV 保持一致(本脚本只读 CSV,不改数据)。

用法:.venv-api\\Scripts\\python scripts\\catalog\\gen_md_all.py
输出:docs/catalog/全字段字典总表.md
"""
import csv
import os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAT = os.path.join(ROOT, "docs", "catalog")
OUT = os.path.join(CAT, "全字段字典总表.md")


def _read(*parts):
    path = os.path.join(CAT, *parts)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _esc(v):
    """Markdown 表格转义:竖线与换行。"""
    return (v or "").replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def _table(md, headers, rows, cols):
    """输出一张 Markdown 表。cols=从每行取值的 key 列表,与 headers 对齐。"""
    md.append("| " + " | ".join(headers) + " |")
    md.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        md.append("| " + " | ".join(_esc(r.get(c, "")) for c in cols) + " |")
    md.append("")


def _group(rows, key):
    g = OrderedDict()
    for r in rows:
        g.setdefault(r.get(key, "") or "(未分类)", []).append(r)
    return g


# ---------------------------------------------------------------- EM(东方财富)
def section_em(md, stats):
    md.append("\n## 一、东方财富 EMQuantAPI(EM)\n")
    md.append("> 取自 `quantapi.eastmoney.com` 命令生成器后台接口。截面 css / 序列 csd / "
              "专题报表 ctr 三类,另附 EDB 字段模板、资讯板块、行业板块种子。\n")

    # css:品种 → 分类
    css = _read("em", "css_indicators.csv")
    stats.append(("EM", "css 截面指标", len(css)))
    md.append(f"\n### 1.1 截面指标 css(按品种 → 分类,共 {len(css)} 个)\n")
    md.append("> 端点 `GET /em/css`。列:指标代码 / 中文名 / 单位 / 参数 / 适用范围\n")
    for var, vrows in _group(css, "品种").items():
        cats = _group(vrows, "分类")
        md.append(f"\n#### EM·css·{var}（{len(cats)} 分类 / {len(vrows)} 指标）\n")
        for cat, items in cats.items():
            md.append(f"\n**{cat}**\n")
            _table(md, ["指标代码", "中文名", "单位", "参数", "适用范围"], items,
                   ["指标代码", "指标中文名", "单位", "参数", "适用范围"])

    # csd:品种id
    csd = _read("em", "csd_indicators.csv")
    stats.append(("EM", "csd 序列指标", len(csd)))
    md.append(f"\n### 1.2 序列指标 csd（共 {len(csd)} 个）\n")
    md.append("> 端点 `GET /em/csd`。列:指标代码 / 中文名 / 单位 / 参数 / 适用范围\n")
    for var, vrows in _group(csd, "品种id").items():
        md.append(f"\n#### EM·csd·品种id {var}（{len(vrows)} 指标）\n")
        _table(md, ["指标代码", "中文名", "单位", "参数", "适用范围"], vrows,
               ["指标代码", "指标中文名", "单位", "参数", "适用范围"])

    # ctr:品种 → 报表
    ctr = _read("em", "ctr_indicators.csv")
    stats.append(("EM", "ctr 专题报表字段", len(ctr)))
    md.append(f"\n### 1.3 专题报表 ctr（按品种 → 报表,共 {len(ctr)} 个字段）\n")
    md.append("> 端点 `GET /em/ctr`。列:字段代码 / 字段中文名（报表代码见分节标题）\n")
    for var, vrows in _group(ctr, "品种").items():
        reps = _group(vrows, "报表名")
        md.append(f"\n#### EM·ctr·{var}（{len(reps)} 张报表 / {len(vrows)} 字段）\n")
        for rep, items in reps.items():
            code = items[0].get("报表代码CtrName", "")
            md.append(f"\n**{rep}**　`{code}`\n")
            _table(md, ["字段代码", "字段中文名"], items, ["字段代码", "字段中文名"])

    # edb / news / sector
    edb = _read("em", "edb_field_schema.csv")
    if edb:
        stats.append(("EM", "EDB 字段模板", len(edb)))
        md.append(f"\n### 1.4 EDB 宏观字段模板（{len(edb)} 项）\n")
        _table(md, ["字段简称", "中文简称", "备注"], edb, ["字段简称", "中文简称", "备注"])

    news = _read("em", "news_boards.csv")
    if news:
        stats.append(("EM", "资讯板块", len(news)))
        md.append(f"\n### 1.5 资讯板块 news_boards（{len(news)} 个）\n")
        _table(md, ["板块代码", "板块名称", "母板块"], news, ["板块代码", "板块名称", "母板块"])

    seed = _read("em", "sector_seeds.csv")
    if seed:
        stats.append(("EM", "行业板块种子", len(seed)))
        md.append(f"\n### 1.6 行业板块种子 sector_seeds（{len(seed)} 个）\n")
        _table(md, ["板块代码", "板块名称", "成分数量", "成分样例(前3)"], seed,
               ["板块代码pukey", "板块名称", "成分数量", "成分样例(前3)"])


# ---------------------------------------------------------------- iFinD(同花顺)
IFIND_TYPES = [
    ("stk", "A股股票"), ("bond", "债券"), ("fund", "基金理财"),
    ("index", "指数"), ("company", "企业"), ("global", "全球股票"),
    ("hk", "港股"), ("usk", "美股"), ("uk", "英股"),
    ("future", "期货"), ("option", "期权"), ("spot", "现货"),
    ("fxrate", "外汇"),
]


def section_ifind(md, stats):
    md.append("\n## 二、同花顺 iFinD\n")
    md.append("> 取自 `quantapi.51ifind.com` 命令生成器后台接口,13 个品种。"
              "列:指标代码 / 中文名 / 英文代码 / 单位 / 参数 / 支持序列\n")
    for i, (typ, cn) in enumerate(IFIND_TYPES, 1):
        rows = _read("ths", f"{typ}_indicators.csv")
        if not rows:
            continue
        stats.append(("iFinD", cn, len(rows)))
        cats = _group(rows, "分类")
        md.append(f"\n### 2.{i} {cn}（{typ}，{len(cats)} 分类 / {len(rows)} 指标）\n")
        for cat, items in cats.items():
            md.append(f"\n**{cat}**\n")
            _table(md, ["指标代码", "中文名", "英文代码", "单位", "参数", "支持序列"], items,
                   ["指标代码", "指标中文名", "英文代码", "单位", "参数", "支持序列"])

    fn = _read("ths", "functions.csv")
    if fn:
        md.append(f"\n### 2.14 常用函数 functions（{len(fn)} 个）\n")
        _table(md, ["函数名", "用途", "签名"], fn, ["函数名", "用途", "签名"])

    samp = _read("ths", "indicator_samples.csv")
    if samp:
        md.append(f"\n### 2.15 指标样例 indicator_samples（{len(samp)} 条）\n")
        _table(md, ["维度", "指标代码", "来源/说明"], samp, ["维度", "指标代码", "来源/说明"])


# ---------------------------------------------------------------- Wind
def section_wind(md, stats):
    md.append("\n## 三、Wind(WindPy)\n")
    md.append("> Wind 有三套口径,勿混用:①WindPy 实测可用(可直接喂 `/wind/wsd|wss`);"
              "②Excel 插件 xla 并集(仅查中文名/找码,不能直接喂 wss);③探测子集。\n")

    wp = _read("wind", "windpy_fields.csv")
    if wp:
        stats.append(("Wind", "WindPy 实测可用", len(wp)))
        md.append(f"\n### 3.1 WindPy 实测可用字段（{len(wp)} 个，可直接喂 wsd/wss）\n")
        _table(md, ["字段代码", "字段(大写)", "中文名", "参数", "来源"], wp,
               ["字段代码", "字段(大写)", "中文名", "参数", "来源"])

    xla = _read("wind", "xla_fields.csv")
    if xla:
        stats.append(("Wind", "Excel 插件 xla 并集", len(xla)))
        md.append(f"\n### 3.2 Excel 插件 xla 字段并集（{len(xla)} 个，仅供查名/找码）\n")
        _table(md, ["字段代码", "字段(大写)", "中文名", "参数"], xla,
               ["字段代码", "字段(大写)", "中文名", "参数"])

    xlaf = _read("wind", "xla_fields_full.csv")
    if xlaf:
        stats.append(("Wind", "xla 全参数版(WindFunc_s)", len(xlaf)))
        md.append(f"\n### 3.3 xla 全参数版 xla_fields_full（{len(xlaf)} 个，参数更全，与 3.2 重叠）\n")
        _table(md, ["字段代码", "字段(大写)", "中文名", "参数"], xlaf,
               ["字段代码", "字段(大写)", "中文名", "参数"])

    pb = _read("wind", "probed_fields.csv")
    if pb:
        stats.append(("Wind", "探测子集", len(pb)))
        md.append(f"\n### 3.4 探测子集 probed_fields（{len(pb)} 个，带实测样例）\n")
        _table(md, ["分类", "字段代码", "字段(大写)", "中文名", "有效", "命中品种", "样例值", "备注"], pb,
               ["分类", "字段代码", "字段(大写)", "中文名", "有效", "命中品种", "样例值", "备注"])


# ---------------------------------------------------------------- TDX(通达信)
TDX_IFACE_CN = {
    "get_market_data": "K线行情", "get_market_snapshot": "行情快照",
    "get_stock_info": "股票基础信息", "get_more_info": "更多股票信息",
    "get_pricevol": "量价数据", "get_divid_factors": "除权因子",
    "get_relation": "关联品种", "get_ipo_info": "新股IPO信息",
    "get_gb_info": "股本信息", "get_gb_info_by_date": "指定日期股本",
    "get_match_stkinfo": "证券信息检索", "get_report_data": "行情订阅推送",
    "get_trading_dates": "交易日历", "get_trackzs_etf_info": "跟踪指数ETF",
    "get_kzz_info": "可转债信息",
    "get_financial_data": "专业财务数据(FN)", "get_financial_data_by_date": "指定日期财务",
    "get_gp_one_data": "股票单个财务数据",
    "get_gpjy_value": "股票经济指标", "get_gpjy_value_by_date": "指定日期股票经济指标",
    "get_bkjy_value": "板块经济指标", "get_bkjy_value_by_date": "指定日期板块经济指标",
    "get_scjy_value": "市场经济指标(SC)", "get_scjy_value_by_date": "指定日期市场经济指标",
    "get_stock_list": "股票列表", "get_sector_list": "板块列表",
    "get_stock_list_in_sector": "板块成分股", "send_user_block": "自选/板块写入",
    "stock_account": "获取资金账户句柄", "query_stock_asset": "查询账户资产",
    "query_stock_orders": "查询委托", "query_stock_positions": "查询持仓",
    "order_stock": "下单", "cancel_order_stock": "撤单",
}


def section_tdx(md, stats):
    md.append("\n## 四、通达信 TQ(TDX / TdxQuant)\n")
    md.append("> 取自随终端附带的《TdxQuant接口说明文档》PDF(231页)结构化抽表。"
              "按接口分组,PARAM=入参 / RETURN=返回字段。代码用标准格式(`600519.SH`),日期 `YYYYMMDD`。\n")
    tdx = _read("tdx", "tdx_fields.csv")
    stats.append(("TDX", "接口字段总行", len(tdx)))
    ifaces = _group(tdx, "interface")
    idx = 0
    for iface, rows in ifaces.items():
        idx += 1
        cn = TDX_IFACE_CN.get(iface, "")
        title = f"{iface}" + (f"（{cn}）" if cn else "")
        md.append(f"\n### 4.{idx} {title}（{len(rows)} 字段）\n")
        params = [r for r in rows if r.get("kind") == "PARAM"]
        rets = [r for r in rows if r.get("kind") == "RETURN"]
        other = [r for r in rows if r.get("kind") not in ("PARAM", "RETURN")]
        if params:
            md.append("\n**入参 PARAM**\n")
            _table(md, ["字段", "必填", "类型", "默认/取值", "说明"], params,
                   ["field", "flag", "dtype", "value", "desc"])
        if rets:
            md.append("\n**返回 RETURN**\n")
            _table(md, ["字段", "标志", "类型", "取值", "说明"], rets,
                   ["field", "flag", "dtype", "value", "desc"])
        if other:
            md.append("\n**其它**\n")
            _table(md, ["字段", "kind", "标志", "类型", "取值", "说明"], other,
                   ["field", "kind", "flag", "dtype", "value", "desc"])


# ---------------------------------------------------------------- 主流程
def main():
    md = []
    stats = []  # (源, 子表, 行数)

    md.append("# StockSDK 全字段字典总表\n")
    md.append("> 本文件由 `scripts/catalog/gen_md_all.py` 从 `docs/catalog/` 下四源"
              "(东方财富EM / 同花顺iFinD / Wind / 通达信TDX)的全部字段 CSV 自动汇总生成,"
              "**只读 CSV、不改数据**,与各源独立手册内容一致。给消费方做产品/接口设计与取数查阅用。\n")
    md.append("> ⚠ 这是**字段字典**(有哪些指标可取),不是运行时取数结果。"
              "取数走各源端点(`/em/* /ths/* /wind/* /tdx/*`),字段口径以本表为准。\n")
    md.append("> 🔴 取数纪律:**查本表按需取用,禁止联网遍历指标树**(遍历是 iFinD 被封根因)。\n")

    # 先算各分节内容(顺带填 stats),再把总览插到前面
    body = []
    section_em(body, stats)
    section_ifind(body, stats)
    section_wind(body, stats)
    section_tdx(body, stats)

    # 总览统计
    md.append("\n## 总览\n")
    by_src = OrderedDict()
    for src, sub, n in stats:
        by_src.setdefault(src, 0)
        by_src[src] += n
    md.append("| 数据源 | 子表 | 字段/行数 |")
    md.append("|---|---|---:|")
    for src, sub, n in stats:
        md.append(f"| {src} | {sub} | {n:,} |")
    md.append(f"| **合计** | **{len(stats)} 张子表** | **{sum(n for _, _, n in stats):,}** |")
    md.append("")
    md.append("各源小计:" + " / ".join(f"{s} {c:,}" for s, c in by_src.items()) + "。\n")
    md.append("> 端点速查:EM `/em/css|csd|ctr` · iFinD `/ths/*` · "
              "Wind `/wind/wsd|wss`(仅 3.1 WindPy 口径可直接喂) · TDX `/tdx/*`。\n")

    md.extend(body)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    total = sum(n for _, _, n in stats)
    print(f"生成 {OUT}")
    print(f"子表 {len(stats)} 张,字段/行合计 {total:,},文件 {os.path.getsize(OUT) / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
