"""探 wsq/wses/wsee 是否有独立可枚举字段命名空间 + 校验机制标定。

WindPy 文档列 24 函数,我之前只验证 wss/wsd(共用一套字段字典,5359)。
但 wsq(实时,rt_ 前缀)/wses+wsee(板块,sec_*_avg)很可能是**独立命名空间**。
本脚本标定:① 这些函数对无效字段是否也返回 -40522006(可二分批量验证);
② 文档示例字段是否被各自函数认可;③ 跨函数字段是否互通。
用法:.venv-wind\\Scripts\\python scripts\\catalog\\wind_probe_other_funcs.py
"""
from WindPy import w   # noqa: E402

STOCK = "600519.SH"
SECTOR = "a001010100000000"   # 文档示例板块ID(全部A股类)


def ec(out):
    return getattr(out, "ErrorCode", None), [str(x) for x in getattr(out, "Fields", [])][:6]


def main():
    r = w.start(waitTime=60)
    print(f"start ErrorCode={getattr(r,'ErrorCode','?')}\n")

    print("=== wsq 实时行情(快照,func=None)===")
    for f in ["rt_last,rt_open", "rt_high,rt_low,rt_vol,rt_amt", "totally_fake_rt_xyz", "close"]:
        out = w.wsq(STOCK, f)
        print(f"  fields={f:35s} -> {ec(out)}")

    print("\n=== wses 板块日序列(单指标)===")
    for f in ["sec_close_avg", "sec_pe_avg", "totally_fake_sec_xyz"]:
        out = w.wses(SECTOR, f, "2026-06-26", "2026-06-29")
        print(f"  fields={f:25s} -> {ec(out)}")

    print("\n=== wsee 板块日截面 ===")
    for f in ["sec_close_avg", "sec_pe_avg,sec_pb_avg", "totally_fake_sec_xyz"]:
        out = w.wsee(SECTOR, f, "tradeDate=20260629")
        print(f"  fields={f:30s} -> {ec(out)}")

    print("\n=== 交叉:wss 的字段喂 wsq?wsq 的 rt_ 喂 wss?===")
    print("  wss(rt_last):", ec(w.wss(STOCK, "rt_last", "tradeDate=20260629")))
    print("  wsq(close):  ", ec(w.wsq(STOCK, "close")))


if __name__ == "__main__":
    main()
