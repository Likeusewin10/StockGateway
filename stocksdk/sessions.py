"""SDK 会话管理：单会话/单点登录，全局锁串行化所有取数。

两个 SDK 均单会话，本服务用一把全局锁串行化所有请求，
必须单 worker 运行（不要加 --workers）。会话首次使用时惰性登录。
"""
import threading

from fastapi import HTTPException

from EmQuantAPI import c
from iFinDPy import THS_iFinDLogin

from stocksdk.config import require_ths_credentials

# 全局锁：SDK 单会话，所有取数串行化。整个服务唯一一把锁。
lock = threading.Lock()

_em_ready = False
_ths_ready = False


def ensure_em() -> None:
    """东财 SDK 惰性登录（用本机 userInfo 令牌）。失败抛 502。"""
    global _em_ready
    if _em_ready:
        return
    r = c.start("ForceLogin=1", "")
    if r.ErrorCode != 0:
        raise HTTPException(502, "EM 登录失败：{} {}".format(r.ErrorCode, r.ErrorMsg))
    _em_ready = True


def ensure_ths() -> None:
    """同花顺 iFinD 惰性登录（用 .env 凭据）。失败抛 502。"""
    global _ths_ready
    if _ths_ready:
        return
    user, pwd = require_ths_credentials()
    code = THS_iFinDLogin(user, pwd)
    if code != 0:
        raise HTTPException(502, "iFinD 登录失败：{}".format(code))
    _ths_ready = True
