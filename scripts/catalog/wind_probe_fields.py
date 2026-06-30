"""Wind 字段探测器 —— catalog 方案 C。

逐字段调本机 /wind/wss(单 field/单股),按 ErrorCode 区分:
  有效(字段存在,含取回值或 null) / 无效(invalid indicators -40522006)。
产出经实测验证的 Wind 字段表 docs/catalog/wind/probed_fields.csv。

⚠ 方案 C 固有边界:只能验证 wind_field_seeds.txt 里的候选,发现不了未知 field
  (Wind 全量字段树被加密锁死,无可编程旁路,见 .claude/plans/wind-catalog-crawl.plan.md)。

种子:scripts/catalog/wind_field_seeds.txt([section] 分类 + 每行一字段)
探测标的:多品种各选一只代表(股/债/基/指),提升字段命中率。
用法:.venv-api\\Scripts\\python scripts\\catalog\\wind_probe_fields.py
前提:本机 8000 服务在跑、.env 有 API_KEY、Wind 已登录。
"""
import csv
import gzip
import json
import os
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SEEDS = os.path.join(ROOT, "scripts", "catalog", "wind_field_seeds.txt")
OUT_DIR = os.path.join(ROOT, "docs", "catalog", "wind")
OUT = os.path.join(OUT_DIR, "probed_fields.csv")

BASE = "http://127.0.0.1:8000"
# 多品种代表(提升命中:某字段可能仅对债/基/指有效)
PROBES = [
    ("600519.SH", "股", "tradeDate=20260629"),
    ("000300.SH", "指", "tradeDate=20260629"),
    ("010107.SH", "债", "tradeDate=20260629"),
]

INVALID_MARK = "invalid indicators"  # -40522006


def _api_key():
    env = os.path.join(ROOT, ".env")
    with open(env, encoding="utf-8") as f:
        for line in f:
            if line.startswith("API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("\r")
    return ""


def _load_seeds():
    """返回 [(section, field, cname)],保留分类顺序。
    行格式:`field  中文名`(空白分隔,中文名可选)。"""
    out, sect = [], "未分类"
    with open(SEEDS, encoding="utf-8") as f:
        for raw in f:
            s = raw.split("#", 1)[0].strip()
            if not s:
                continue
            if s.startswith("[") and s.endswith("]"):
                sect = s[1:-1]
                continue
            parts = s.split(None, 1)
            field = parts[0].lower()
            cname = parts[1].strip() if len(parts) > 1 else ""
            out.append((sect, field, cname))
    return out


def _probe(key, code, field, options):
    """单字段探测。返回 (status, value_or_msg)。status: ok / invalid / error。
    429 限流时自动 sleep 重试(限流非字段无效,不可误判)。"""
    qs = urllib.parse.urlencode({"codes": code, "fields": field, "options": options})
    url = f"{BASE}/wind/wss?{qs}"
    for attempt in range(6):
        req = urllib.request.Request(url, headers={"X-API-Key": key, "Accept-Encoding": "gzip"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                data = json.loads(raw.decode("utf-8"))
            if isinstance(data, list) and data:
                rec = data[0]
                val = next((v for k, v in rec.items() if k.lower() == field), None)
                return "ok", val
            return "ok", None
        except urllib.error.HTTPError as e:
            body = e.read()
            try:
                body = gzip.decompress(body)
            except OSError:
                pass
            msg = body.decode("utf-8", "ignore")
            if e.code == 429:
                time.sleep(8)   # 限流:退避后重试,绝不当无效
                continue
            if INVALID_MARK in msg or "-40522006" in msg:
                return "invalid", msg[:80]
            return "error", f"HTTP{e.code}:{msg[:80]}"
        except Exception as e:  # noqa: BLE001
            return "error", str(e)[:80]
    return "error", "429 重试耗尽"


def main():
    key = _api_key()
    if not key:
        raise SystemExit("未找到 API_KEY,无法探测")
    seeds = _load_seeds()
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"种子字段 {len(seeds)} 个,逐字段探测(每字段最多试 {len(PROBES)} 个品种)...")

    rows = []
    for i, (sect, field, cname) in enumerate(seeds, 1):
        hit_code, hit_val, last = None, None, None
        for code, kind, opt in PROBES:
            status, val = _probe(key, code, field, opt)
            last = (status, val)
            if status == "ok":
                hit_code, hit_val = f"{code}({kind})", val
                break
            time.sleep(1.1)   # 节流:稳在 <60 次/分钟,避开限流
        valid = hit_code is not None
        rows.append([sect, field, field.upper(), cname, "是" if valid else "否",
                     hit_code or "", "" if hit_val is None else str(hit_val)[:40],
                     "" if valid else (last[1] if last else "")])
        if i % 20 == 0:
            nok = sum(1 for r in rows if r[4] == "是")
            print(f"  {i}/{len(seeds)} 探完,有效 {nok}")
        time.sleep(1.1)

    with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["分类", "字段代码", "字段(大写)", "中文名", "有效", "命中品种", "样例值", "备注"])
        w.writerows(rows)
    nok = sum(1 for r in rows if r[4] == "是")
    print(f"\n完成:{len(rows)} 字段,有效 {nok} / 无效 {len(rows)-nok} -> {OUT}")


if __name__ == "__main__":
    main()
