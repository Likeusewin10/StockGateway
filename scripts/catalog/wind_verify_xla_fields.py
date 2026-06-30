"""Wind WindPy 字段全量验证器 v2 —— xla 候选 + 去前缀变体,批量喂 wss 分拣 WindPy 认可名。

v1(wind_verify_xla_fields.py)只测 xla 原码,9698→113。但 xla 是 Excel 插件口径
(`s_dq_amount`),WindPy wss 用短名(去品种/类别前缀,如 `amount` 或 `dq_amount`)。
v2 为每个 xla 码生成候选变体:
  - 原码                         s_dq_amount
  - 去 1 段前缀                  dq_amount
  - 去 2 段前缀                  amount
全部候选去重后批量验证(wss -40522006 是纯名级校验,与品种无关,见 calib2),
失败批二分定位。有效名回溯到生成它的 xla 码,带回中文名(多码映射同名时取最短码的中文名)。

直接 import WindPy 调用,须 .venv-wind 跑、Wind 终端已登录。
产出:docs/catalog/wind/windpy_fields.csv(代码+大写+中文名+参数+来源标注)。
用法:.venv-wind\\Scripts\\python scripts\\catalog\\wind_verify_xla_fields.py [--batch N]
"""
import csv
import os
import sys
import time

from WindPy import w   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
XLA_CSV = os.path.join(ROOT, "docs", "catalog", "wind", "xla_fields.csv")
XLA_FULL_CSV = os.path.join(ROOT, "docs", "catalog", "wind", "xla_fields_full.csv")
PROBED_CSV = os.path.join(ROOT, "docs", "catalog", "wind", "probed_fields.csv")
OUT = os.path.join(ROOT, "docs", "catalog", "wind", "windpy_fields.csv")

STOCK = "600519.SH"
OPT = "tradeDate=20260629"
BATCH = 400
INVALID_EC = -40522006


def load_xla():
    """合并两个 xla 提取(WindFunc.xla 9698 + WindFunc_s.xla 7887,并集 ~10069)。"""
    rows = []
    seen = set()
    for path in (XLA_CSV, XLA_FULL_CSV):
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                code = (r.get("字段代码") or "").strip().lower()
                if code and code not in seen:
                    seen.add(code)
                    rows.append((code, (r.get("中文名") or "").strip(),
                                 (r.get("参数") or "").strip()))
    return rows


def load_probed():
    """已实测 130 个 WindPy 短名(带中文名),作为权威候选并入。"""
    out = {}
    if not os.path.exists(PROBED_CSV):
        return out
    with open(PROBED_CSV, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if (r.get("有效") or "").strip() == "是":
                code = (r.get("字段代码") or "").strip().lower()
                if code:
                    out[code] = (r.get("中文名") or "").strip()
    return out


def variants(code):
    """生成候选短名:原码 + 渐进去前缀(去 1 段、2 段、3 段)。
    例 s_fa_roe_ttm → {s_fa_roe_ttm, fa_roe_ttm, roe_ttm, ttm}。
    末段单字也保留(让 wss 字典裁定),最大化候选覆盖。"""
    segs = code.split("_")
    cands = {code}
    for drop in (1, 2, 3):
        if len(segs) > drop:
            cands.add("_".join(segs[drop:]))
    return cands


def wss_ec(fields):
    out = w.wss(STOCK, ",".join(fields), OPT)
    return getattr(out, "ErrorCode", None)


def classify(fields, stats):
    if not fields:
        return set()
    ec = wss_ec(fields)
    stats["calls"] += 1
    if ec == 0:
        return set(fields)
    if ec == INVALID_EC:
        if len(fields) == 1:
            return set()
        mid = len(fields) // 2
        return classify(fields[:mid], stats) | classify(fields[mid:], stats)
    time.sleep(2)                       # 会话/限速兜底重试
    ec2 = wss_ec(fields)
    stats["calls"] += 1
    if ec2 == 0:
        return set(fields)
    if ec2 == INVALID_EC and len(fields) > 1:
        mid = len(fields) // 2
        return classify(fields[:mid], stats) | classify(fields[mid:], stats)
    return set()


def main():
    global BATCH
    if "--batch" in sys.argv:
        BATCH = int(sys.argv[sys.argv.index("--batch") + 1])

    r = w.start(waitTime=60)
    if getattr(r, "ErrorCode", -1) != 0 or not w.isconnected():
        raise SystemExit(f"Wind 未连上 ErrorCode={getattr(r, 'ErrorCode', '?')}")

    xla = load_xla()
    probed = load_probed()
    # 候选名 → 最佳中文名(取最短源码的中文名作代表;含参数)。
    cand_cn = {}       # name -> (cname, params, origin)
    for code, cn, pa in xla:
        for v in variants(code):
            cur = cand_cn.get(v)
            # 优先更短的源码(更可能是规范短名),其次有中文名的
            if cur is None or len(code) < cur[3]:
                cand_cn[v] = (cn, pa, "xla去前缀变体" if v != code else "xla原码", len(code))
    for code, cn in probed.items():     # 实测短名权威,覆盖
        cand_cn[code] = (cn, "", "探测法实测", 0)

    cands = sorted(cand_cn.keys())
    print(f"xla {len(xla)} 码 + 探测 {len(probed)} → 候选变体去重 {len(cands)} 个,批 {BATCH}")

    valid = set()
    stats = {"calls": 0}
    t0 = time.monotonic()
    for i in range(0, len(cands), BATCH):
        chunk = cands[i:i + BATCH]
        valid |= classify(chunk, stats)
        done = min(i + BATCH, len(cands))
        print(f"  {done}/{len(cands)}  有效累计 {len(valid)}  调用 {stats['calls']}  "
              f"{time.monotonic()-t0:.0f}s")

    rows = []
    for name in sorted(valid):
        cn, pa, origin, _ = cand_cn[name]
        rows.append([name, name.upper(), cn, pa, origin])
    with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["字段代码", "字段(大写)", "中文名", "参数", "来源"])
        wr.writerows(rows)
    print(f"\n完成:候选 {len(cands)} → WindPy 认可 {len(valid)} 个,"
          f"API 调用 {stats['calls']} 次 -> {OUT}")


if __name__ == "__main__":
    main()
