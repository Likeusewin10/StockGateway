# -*- coding: utf-8 -*-
"""从《TdxQuant接口说明文档》PDF 抽取全部接口字段表 → CSV。

合法来源:官方随终端附带的接口说明文档(非爬取/非探测,零封控风险)。
用 PyMuPDF find_tables() 抽字段表,按表头分类,按函数签名归属接口。
交易函数区(stock_account/query_*/order_stock/cancel_order_stock)与常量枚举区
方法名不带 get_/send_ 前缀,签名正则抓不到,用 PAGE_OVERRIDE(0-based)显式归属。
"""
import fitz, re, csv, io
from collections import Counter, OrderedDict, defaultdict

PDF = "docs/catalog/tdx/_raw/TdxQuant接口说明文档.pdf"
OUT = "docs/catalog/tdx/tdx_fields.csv"

SIG = re.compile(r'(?:def\s+)?((?:get|send|refresh|formula|exec)_[a-z_]+)\s*\(')
DTYPES = {"double", "int", "str", "float", "long", "bool", "number",
          "list", "list[str]", "dict", "datetime", "long long", "double[]"}

# 交易函数区 + 常量枚举区:方法名不带前缀,签名正则抓不到,按页显式归属(0-based idx)
PAGE_OVERRIDE = {
    151: "stock_account", 152: "query_stock_asset", 153: "query_stock_asset",
    154: "query_stock_orders", 155: "query_stock_orders",
    156: "query_stock_positions", 157: "query_stock_positions",
    158: "order_stock", 159: "order_stock",
    160: "cancel_order_stock", 161: "cancel_order_stock",
    169: "常量枚举", 170: "常量枚举", 171: "常量枚举", 172: "常量枚举",
}

def fix_code(c):
    c = (c or "").strip()
    c = re.sub(r'\s*_\s*$', '', c)   # 去 find_tables 抽出的尾部伪下划线
    c = re.sub(r'\s+', '_', c)       # 内部空格原本是下划线
    c = re.sub(r'_+', '_', c)        # 折叠重复下划线
    c = c.rstrip('_')                # TQ 字段码不以下划线结尾,去残留尾部
    return c

def clean(c):
    return re.sub(r'\s+', ' ', (c or "").strip())

def keep_cols(header):
    return [i for i, h in enumerate(header) if (h or "").strip()]

def classify(header):
    j = " ".join((h or "") for h in header)
    if "是否必选" in j or "是否可选" in j or j.strip().startswith("参数"):
        return "PARAM"
    if "默认返回" in j:
        return "RETURN"
    if "名称" in j and "类型" in j and "说明" in j:
        return "RETURN"
    return None

def page_func(page):
    m = None
    for m in SIG.finditer(page.get_text()):
        pass
    return m.group(1) if m else None

def parse_return(cells):
    """按行自动判返回版式:
    RET_A 名称/默认返回/类型/说明 -> cells[1]=Y/N 标志
    RET_B 名称/类型/数值/说明     -> cells[1]=类型
    """
    c1 = clean(cells[1]) if len(cells) > 1 else ""
    c2 = clean(cells[2]) if len(cells) > 2 else ""
    c3 = clean(cells[3]) if len(cells) > 3 else ""
    if c1 in ("Y", "N", "是", "否", "y", "n"):
        return c1, c2, "", c3            # flag, dtype, value, desc
    if c1.lower() in DTYPES:
        return "", c1, c2, c3            # dtype, value, desc
    # 兜底:当作 RET_A
    return c1, c2, "", c3

def main():
    doc = fitz.open(PDF)
    out = []
    current = None
    for pno in range(doc.page_count):
        page = doc[pno]
        tabs = page.find_tables()
        if not tabs.tables:
            continue
        f = page_func(page)
        for t in tabs.tables:
            raw = t.extract()
            if not raw:
                continue
            kind = classify(raw[0])
            if kind is None:
                continue
            ki = keep_cols(raw[0])
            if len(ki) < 3:
                continue
            if pno in PAGE_OVERRIDE:
                iface = PAGE_OVERRIDE[pno]
            else:
                if f:
                    current = f
                iface = current or f"未定名@p{pno+1}"
            for r in raw[1:]:
                cells = [r[i] if i < len(r) else "" for i in ki]
                code = fix_code(cells[0])
                if not code or code in ("数据", "名称", "参数"):
                    continue
                if kind == "PARAM":
                    flag = clean(cells[1]) if len(cells) > 1 else ""
                    dtype = clean(cells[2]) if len(cells) > 2 else ""
                    val, desc = "", clean(cells[3]) if len(cells) > 3 else ""
                else:
                    flag, dtype, val, desc = parse_return(cells)
                out.append([pno + 1, iface, kind, code, flag, dtype, val, desc])
    with io.open(OUT, "w", encoding="utf-8-sig", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(["page", "interface", "kind", "field", "flag", "dtype", "value", "desc"])
        w.writerows(out)
    kc = Counter(r[2] for r in out)
    ic = OrderedDict()
    for r in out:
        ic[r[1]] = ic.get(r[1], 0) + 1
    print(f"总行数: {len(out)}  类型: {dict(kc)}  接口数: {len(ic)}")
    for iface, n in ic.items():
        print(f"  {iface}: {n}")

if __name__ == "__main__":
    main()
