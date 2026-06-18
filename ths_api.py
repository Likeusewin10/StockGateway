"""同花顺 iFinD 简化封装。

调用方无需关心账密/登录：首次取数时自动用 .env 里的凭据登录，
之后复用连接不重登。默认返回 pandas.DataFrame。

用法（在 .venv-ths 下）：
    import ths_api as ths
    df = ths.history("300033.SZ", "open;high;low;close", "2024-01-01", "2024-01-05")
    df = ths.basic("300033.SZ", "ths_stock_short_name_stock", "")
"""
import atexit

from iFinDPy import (
    THS_iFinDLogin,
    THS_iFinDLogout,
    THS_HistoryQuotes,
    THS_BasicData,
    THS_RealtimeQuotes,
    THS_Trans2DataFrame,
)

from stocksdk.config import load_dotenv, require_ths_credentials

_logged_in = False


def _ensure_login():
    """首次调用时登录，之后复用。"""
    global _logged_in
    if _logged_in:
        return
    load_dotenv()
    user, pwd = require_ths_credentials()
    code = THS_iFinDLogin(user, pwd)
    if code != 0:
        raise RuntimeError("iFinD 登录失败，返回码 {}（单点登录冲突/权限/网络）".format(code))
    _logged_in = True
    atexit.register(_logout)


def _logout():
    global _logged_in
    if _logged_in:
        THS_iFinDLogout()
        _logged_in = False


def _to_df(result, as_df):
    """统一出错处理 + 可选转 DataFrame。"""
    if isinstance(result, dict) and result.get("errorcode") not in (0, None):
        raise RuntimeError("iFinD 取数失败：{} {}".format(
            result.get("errorcode"), result.get("errmsg")))
    if as_df:
        return THS_Trans2DataFrame(result)
    return result


def history(codes, indicators, begin, end, params="", as_df=True):
    """历史行情序列。codes 多个用逗号，indicators 多个用分号，日期 YYYY-MM-DD。"""
    _ensure_login()
    r = THS_HistoryQuotes(codes, indicators, params, begin, end)
    return _to_df(r, as_df)


def basic(codes, indicators, params="", as_df=True):
    """基础/截面数据。"""
    _ensure_login()
    r = THS_BasicData(codes, indicators, params)
    return _to_df(r, as_df)


def realtime(codes, indicators, params="", as_df=True):
    """实时行情。"""
    _ensure_login()
    r = THS_RealtimeQuotes(codes, indicators, params)
    return _to_df(r, as_df)


def logout():
    """手动登出（一般无需调用，退出时自动登出）。"""
    _logout()
