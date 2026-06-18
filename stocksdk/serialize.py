"""SDK 返回值归一化为 JSON 友好结构。

东财与同花顺返回类型各异（DataFrame / 自定义对象 / dict），
这里统一成可 JSON 序列化的结构，并把 SDK 错误码翻译成 HTTP 502。
"""
from fastapi import HTTPException


def em_result(result):
    """EM 返回统一成 JSON 友好结构。Ispandas=1 时直接是 DataFrame。"""
    import pandas as pd
    if isinstance(result, tuple) and len(result) == 2:
        result = result[1]
    if isinstance(result, pd.DataFrame):
        return result.reset_index().to_dict(orient="records")
    if hasattr(result, "ErrorCode") and result.ErrorCode != 0:
        raise HTTPException(502, "EM 取数失败：{} {}".format(result.ErrorCode, result.ErrorMsg))
    return getattr(result, "Data", result)


def ths_result(r):
    """iFinD 返回统一成 JSON：dict 直接返回，DataFrame 转 records。"""
    import pandas as pd
    if isinstance(r, pd.DataFrame):
        return r.reset_index().to_dict(orient="records")
    if isinstance(r, dict) and r.get("errorcode") not in (0, None):
        raise HTTPException(502, "iFinD 取数失败：{} {}".format(r.get("errorcode"), r.get("errmsg")))
    return r


def em_quote_to_dict(qd):
    """EmQuantData 推送对象 → JSON 友好 dict。"""
    if getattr(qd, "ErrorCode", 0) not in (0, None):
        return {"event": "error", "code": qd.ErrorCode, "msg": getattr(qd, "ErrorMsg", "")}
    return {
        "event": "quote",
        "codes": list(getattr(qd, "Codes", []) or []),
        "indicators": list(getattr(qd, "Indicators", []) or []),
        "data": getattr(qd, "Data", {}) or {},
    }


def merge_pandas_option(args, options_pandas):
    """透传调用时，仅当最后一个参数看起来像 options/params 串(含 =)时补 Ispandas=1。

    否则它可能是日期/代码(如 csd 的 enddate、tradedates 的 enddate)，追加会破坏取值。
    返回新列表，不修改入参（保持不可变）。
    """
    args = list(args)
    if (options_pandas and args and isinstance(args[-1], str)
            and "=" in args[-1] and "Ispandas" not in args[-1]):
        args = args[:-1] + [args[-1] + ",Ispandas=1"]
    return args
