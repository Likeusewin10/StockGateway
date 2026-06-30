"""Wind wss 字段有效性是否依赖品种 —— 决定探测要不要多品种。

calib 已知:-40522006=字段名不在字典(纯名级校验)。但债/基专属字段名
对股票查询会不会也报无效?若会,探测须多品种;若不会,单只股票即可。
用法:.venv-wind\\Scripts\\python scripts\\catalog\\wind_wss_calib2.py
"""
from WindPy import w   # noqa: E402

CODES = {"股": "600519.SH", "债": "019547.SH", "基": "510300.SH", "指": "000300.SH"}
OPT = "tradeDate=20260629"
# 一批含明显债专属(b_ 前缀)、基专属、估值、财务的 xla 码
FIELDS = ["b_agency_guarantor_abbr", "b_info_couponrate", "close", "pe_ttm",
          "nav", "fund_fundscale", "roe_ttm", "adtm"]


def main():
    r = w.start(waitTime=60)
    print(f"start ErrorCode={getattr(r, 'ErrorCode', '?')}\n")
    for kind, code in CODES.items():
        out = w.wss(code, ",".join(FIELDS), OPT)
        ec = getattr(out, "ErrorCode", None)
        fl = [str(x) for x in getattr(out, "Fields", [])]
        print(f"[{kind} {code}] ErrorCode={ec} Fields={fl}")


if __name__ == "__main__":
    main()
