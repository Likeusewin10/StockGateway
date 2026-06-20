"""SDK 会话管理：单会话/单点登录，全局锁串行化所有取数。

两个 SDK 均单会话，本服务用一把全局锁串行化所有请求，
必须单 worker 运行（不要加 --workers）。会话首次使用时惰性登录。

会话自愈：底层会话会被悄悄踢掉（被别处同账号登录挤掉、iFinD 单点
登录冲突、令牌超时）。`em_exec`/`ths_exec` 在取数失败疑似会话失效时，
强制重登一次并重试，避免远程调用报"未登录/已登出"。
"""
import threading
from typing import Any, Callable

from fastapi import HTTPException

from EmQuantAPI import c
from iFinDPy import THS_iFinDLogin, THS_iFinDLogout

from stocksdk.config import require_ths_credentials

# 全局锁：SDK 单会话，所有取数串行化。整个服务唯一一把锁。
lock = threading.Lock()

_em_ready = False
_ths_ready = False

# 会话/登录失效类错误码（命中即强制重登重试）。
# EM：10001009 登录数超限/被挤、10001005/10001006 未登录类、10001020 令牌失效。
_EM_SESSION_CODES = {10001005, 10001006, 10001009, 10001019, 10001020}
# iFinD：负的会话码，-1010 已登出最常见。
_THS_SESSION_CODES = {-1001, -1010, -1011}
# 错误信息兜底关键词（码集漏判时按文本判定）。
_SESSION_KEYWORDS = ("login", "logged out", "not login", "登录", "登出", "未登录")


def ensure_em(force: bool = False) -> None:
    """东财 SDK 惰性登录（用本机 userInfo 令牌）。force=True 无视 flag 强制重登。失败抛 502。"""
    global _em_ready
    if _em_ready and not force:
        return
    r = c.start("ForceLogin=1", "")
    if r.ErrorCode != 0:
        _em_ready = False
        raise HTTPException(502, "EM 登录失败：{} {}".format(r.ErrorCode, r.ErrorMsg))
    _em_ready = True


def ensure_ths(force: bool = False) -> None:
    """同花顺 iFinD 惰性登录（用 .env 凭据）。force=True 先登出再登录，强制抢回会话。失败抛 502。"""
    global _ths_ready
    if _ths_ready and not force:
        return
    if force:
        try:
            THS_iFinDLogout()   # 先登出，避免叠加登录数
        except Exception:
            pass
    user, pwd = require_ths_credentials()
    code = THS_iFinDLogin(user, pwd)
    if code != 0:
        _ths_ready = False
        raise HTTPException(502, "iFinD 登录失败：{}".format(code))
    _ths_ready = True


def _text_has_session_keyword(text: Any) -> bool:
    if not text:
        return False
    s = str(text).lower()
    return any(k.lower() in s for k in _SESSION_KEYWORDS)


def _em_session_dead(result: Any) -> bool:
    """EM 返回对象是否表示会话/登录失效。"""
    code = getattr(result, "ErrorCode", None)
    if code in _EM_SESSION_CODES:
        return True
    if code not in (0, None):   # 仅在出错时才看文本，避免误判正常数据
        return _text_has_session_keyword(getattr(result, "ErrorMsg", ""))
    return False


def _ths_session_dead(result: Any) -> bool:
    """iFinD dict 返回是否表示会话/登录失效。"""
    if not isinstance(result, dict):
        return False
    code = result.get("errorcode")
    if code in _THS_SESSION_CODES:
        return True
    if code not in (0, None):
        return _text_has_session_keyword(result.get("errmsg", ""))
    return False


def em_exec(fn: Callable[[], Any]) -> Any:
    """在已登录会话里执行 EM 取数 thunk；若会话失效则强制重登并重试一次。

    调用方须已持有全局 lock（本函数不自己加锁，沿用现有串行化）。
    """
    ensure_em()
    r = fn()
    if _em_session_dead(r):
        ensure_em(force=True)
        r = fn()
    return r


def ths_exec(fn: Callable[[], Any]) -> Any:
    """在已登录会话里执行 iFinD 取数 thunk；若会话失效则强制重登并重试一次。

    调用方须已持有全局 lock（本函数不自己加锁，沿用现有串行化）。
    """
    ensure_ths()
    r = fn()
    if _ths_session_dead(r):
        ensure_ths(force=True)
        r = fn()
    return r
