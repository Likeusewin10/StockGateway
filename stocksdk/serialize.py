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


def wind_result(r):
    """Wind 返回统一成 JSON 友好结构。

    - usedf=True 时 r 是 (ErrorCode, DataFrame) 元组 → 错误码 != 0 抛 502，否则 df 转 records。
    - 否则 r 是 WindData(.ErrorCode/.Codes/.Fields/.Times/.Data) → 错误码 != 0 抛 502，
      否则返回结构化 dict（比裸 .Data 字段优先序列更可用）。
    - 坏证券码返回 ErrorCode=0 + Data=[[None,...]]，按正常数据返回（只看 ErrorCode 判失败）。
    """
    import pandas as pd
    if isinstance(r, tuple) and len(r) == 2:
        code, df = r
        if code != 0:
            raise HTTPException(502, "Wind 取数失败：{}".format(code))
        if isinstance(df, pd.DataFrame):
            return df.reset_index().to_dict(orient="records")
        return df
    if hasattr(r, "ErrorCode") and r.ErrorCode != 0:
        # .Data 失败时多为短消息(如 ['Login Failed!'])，但也可能是大列表；截断防 502 体爆量
        detail = str(getattr(r, "Data", ""))[:200]
        raise HTTPException(502, "Wind 取数失败：{} {}".format(r.ErrorCode, detail))
    return {
        "Codes": list(getattr(r, "Codes", []) or []),
        "Fields": list(getattr(r, "Fields", []) or []),
        "Times": list(getattr(r, "Times", []) or []),
        "Data": getattr(r, "Data", []),
    }


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


# ---- QMT（XtQuant）交易对象归一化 ----
# 字段名严格对照本机 xtquant/xttype.py 的 XtAsset/XtPosition/XtOrder/XtTrade。

def qmt_asset(a) -> dict:
    """XtAsset → dict。"""
    return {
        "account_id": getattr(a, "account_id", None),
        "cash": getattr(a, "cash", None),
        "frozen_cash": getattr(a, "frozen_cash", None),
        "market_value": getattr(a, "market_value", None),
        "total_asset": getattr(a, "total_asset", None),
    }


def qmt_position(p) -> dict:
    """XtPosition → dict。"""
    return {
        "account_id": getattr(p, "account_id", None),
        "stock_code": getattr(p, "stock_code", None),
        "volume": getattr(p, "volume", None),
        "can_use_volume": getattr(p, "can_use_volume", None),
        "open_price": getattr(p, "open_price", None),
        "market_value": getattr(p, "market_value", None),
        "frozen_volume": getattr(p, "frozen_volume", None),
        "on_road_volume": getattr(p, "on_road_volume", None),
        "yesterday_volume": getattr(p, "yesterday_volume", None),
    }


def qmt_order(o) -> dict:
    """XtOrder → dict。"""
    return {
        "account_id": getattr(o, "account_id", None),
        "stock_code": getattr(o, "stock_code", None),
        "order_id": getattr(o, "order_id", None),
        "order_sysid": getattr(o, "order_sysid", None),
        "order_time": getattr(o, "order_time", None),
        "order_type": getattr(o, "order_type", None),
        "order_volume": getattr(o, "order_volume", None),
        "price_type": getattr(o, "price_type", None),
        "price": getattr(o, "price", None),
        "traded_volume": getattr(o, "traded_volume", None),
        "traded_price": getattr(o, "traded_price", None),
        "order_status": getattr(o, "order_status", None),
        "status_msg": getattr(o, "status_msg", None),
        "strategy_name": getattr(o, "strategy_name", None),
        "order_remark": getattr(o, "order_remark", None),
    }


def qmt_trade(t) -> dict:
    """XtTrade → dict。"""
    return {
        "account_id": getattr(t, "account_id", None),
        "stock_code": getattr(t, "stock_code", None),
        "order_type": getattr(t, "order_type", None),
        "traded_id": getattr(t, "traded_id", None),
        "traded_time": getattr(t, "traded_time", None),
        "traded_price": getattr(t, "traded_price", None),
        "traded_volume": getattr(t, "traded_volume", None),
        "traded_amount": getattr(t, "traded_amount", None),
        "order_id": getattr(t, "order_id", None),
        "order_sysid": getattr(t, "order_sysid", None),
        "strategy_name": getattr(t, "strategy_name", None),
        "order_remark": getattr(t, "order_remark", None),
    }


def qmt_order_id_result(order_id) -> dict:
    """order_stock 返回值：>0 委托号；-1 委托失败 → 502。"""
    if order_id is None or order_id == -1:
        raise HTTPException(502, "QMT 下单失败：order_stock 返回 {}".format(order_id))
    return {"dry_run": False, "order_id": order_id}


def qmt_cancel_result(code) -> dict:
    """cancel_order_stock 返回值：0 成功；负数失败。

    -1 委托已完成、-2 未找到委托、-3 账号未登录 → 409（与既有委托状态冲突）。
    """
    _MSG = {0: "撤单已受理", -1: "委托已完成,无法撤单",
            -2: "未找到对应委托编号", -3: "账号未登录"}
    if code != 0:
        raise HTTPException(409, "QMT 撤单失败：{} {}".format(code, _MSG.get(code, "")))
    return {"cancel_result": code, "msg": _MSG.get(code, "")}
