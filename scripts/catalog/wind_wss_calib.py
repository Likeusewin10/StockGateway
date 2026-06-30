"""Wind wss 批量字段行为标定 —— 摸清混合有效/无效字段时的返回语义。

决定批量探测策略前必须搞清:
  ① 一批 fields 里混入无效字段,wss 是整批 -40522006,还是只标无效项?
  ② 已知有效字段(xla 码)直接喂 wss 能不能认?认多少?
  ③ "有效但不适用该品种"的字段返回什么(ErrorCode=0+null 还是报错)?
用法:.venv-wind\\Scripts\\python scripts\\catalog\\wind_wss_calib.py
"""
from WindPy import w   # noqa: E402

STOCK = "600519.SH"
OPT = "tradeDate=20260629"


def probe(fields):
    """直接调 w.wss(不走 HTTP),返回 (ErrorCode, Fields列表, Data首列样例)。"""
    out = w.wss(STOCK, ",".join(fields), OPT)   # 不用 usedf,拿 WindData 看 Fields
    ec = getattr(out, "ErrorCode", None)
    fl = [str(x) for x in getattr(out, "Fields", [])]
    data = getattr(out, "Data", [])
    sample = [str(row[0]) if isinstance(row, list) and row else str(row) for row in data][:len(fl)]
    return ec, fl, sample


def main():
    r = w.start(waitTime=60)
    print(f"start ErrorCode={getattr(r, 'ErrorCode', '?')}\n")

    cases = {
        "1_纯无效": ["totally_fake_field_xyz"],
        "2_xla已知码(基础)": ["adtm", "atr"],
        "3_WindPy短名": ["close", "open", "pe_ttm"],
        "4_混合(有效+无效)": ["close", "totally_fake_field_xyz", "open"],
        "5_xla码批量": ["accrint_dayend_cnbd", "adtm", "atr", "amaccode_windcode"],
    }
    for name, fields in cases.items():
        ec, fl, sample = probe(fields)
        print(f"[{name}] 送 {len(fields)} 字段 {fields}")
        print(f"   ErrorCode={ec}  回 Fields={fl}")
        print(f"   样例值={sample}\n")


if __name__ == "__main__":
    main()
