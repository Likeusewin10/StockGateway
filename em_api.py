"""东方财富 EMQuantAPI 简化封装。

调用方无需关心登录：首次取数时自动用本机 userInfo 令牌登录，
之后复用连接不重登。默认返回 pandas.DataFrame（内部自动加 Ispandas=1）。

用法（在 .venv-em 下）：
    import em_api as em
    df = em.csd("300059.SZ", "CLOSE", "2024-01-01", "2024-01-05")
    df = em.css("300059.SZ,000002.SZ", "OPEN,CLOSE", "TradeDate=20240105")
"""
import atexit

from EmQuantAPI import c

_logged_in = False


def _ensure_login():
    """首次调用时用本机令牌登录，之后复用。"""
    global _logged_in
    if _logged_in:
        return
    r = c.start("ForceLogin=1", "")
    if r.ErrorCode != 0:
        raise RuntimeError("EM 登录失败：{} {}".format(r.ErrorCode, r.ErrorMsg))
    _logged_in = True
    atexit.register(_logout)


def _logout():
    global _logged_in
    if _logged_in:
        c.stop()
        _logged_in = False


def _merge_pandas(options):
    """确保 options 里带 Ispandas=1（用户没显式设置时）。"""
    if options and "Ispandas" in options:
        return options
    return (options + ",Ispandas=1").lstrip(",") if options else "Ispandas=1"


def _check(result):
    if hasattr(result, "ErrorCode") and result.ErrorCode != 0:
        raise RuntimeError("EM 取数失败：{} {}".format(result.ErrorCode, result.ErrorMsg))
    # Ispandas=1 时 SDK 返回 (ErrorCode, DataFrame) 元组
    if isinstance(result, tuple) and len(result) == 2:
        return result[1]
    return result


def csd(codes, indicators, startdate, enddate, options="", as_df=True):
    """序列数据。codes/indicators 多个用逗号，日期 YYYY-MM-DD。"""
    _ensure_login()
    opts = _merge_pandas(options) if as_df else options
    return _check(c.csd(codes, indicators, startdate, enddate, opts))


def css(codes, indicators, options="", as_df=True):
    """截面数据。"""
    _ensure_login()
    opts = _merge_pandas(options) if as_df else options
    return _check(c.css(codes, indicators, opts))


def cses(blockcodes, indicators, options="", as_df=True):
    """板块截面数据。"""
    _ensure_login()
    opts = _merge_pandas(options) if as_df else options
    return _check(c.cses(blockcodes, indicators, opts))


def tradedates(startdate, enddate, options=""):
    """交易日历。"""
    _ensure_login()
    return _check(c.tradedates(startdate, enddate, options))


def logout():
    """手动登出（一般无需调用，退出时自动登出）。"""
    _logout()
