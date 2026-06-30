"""测 wsd(日序列)是否接受 wss(截面)拒绝的字段名 —— 探有无独立 wsd 字段命名空间。

calib 证实 wss 字段名校验与品种无关。但 wsd 与 wss 可能有不同字段集。
取一批「wss 已验证有效」和一批「wss 拒绝(去前缀变体里 invalid 的)」的名,
分别喂 wsd,看 wsd 是否认可 wss 拒绝的那些。
用法:.venv-wind\\Scripts\\python scripts\\catalog\\wind_wsd_vs_wss.py
"""
import csv
import os

from WindPy import w   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FULL = os.path.join(ROOT, "docs", "catalog", "wind", "xla_fields_full.csv")
VALID = os.path.join(ROOT, "docs", "catalog", "wind", "windpy_fields.csv")

STOCK = "600519.SH"
INVALID_EC = -40522006


def load_codes(path, col="字段代码"):
    out = []
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            c = (r.get(col) or "").strip().lower()
            if c:
                out.append(c)
    return out


def wsd_ec(field):
    out = w.wsd(STOCK, field, "2026-06-26", "2026-06-29")
    return getattr(out, "ErrorCode", None)


def wss_ec(field):
    out = w.wss(STOCK, field, "tradeDate=20260629")
    return getattr(out, "ErrorCode", None)


def main():
    w.start(waitTime=60)
    valid = set(load_codes(VALID))
    full = load_codes(FULL)
    # 取一批 wss 拒绝的 xla 原码(不在 valid 里、且原样喂 wss 失败)
    rejected = [c for c in full if c not in valid][:40]
    wsd_only = []
    for c in rejected:
        if wss_ec(c) == INVALID_EC and wsd_ec(c) == 0:
            wsd_only.append(c)
    print(f"抽查 {len(rejected)} 个 wss 拒绝的 xla 码,其中 wsd 接受的: {len(wsd_only)}")
    print("样例:", wsd_only[:15])


if __name__ == "__main__":
    main()
