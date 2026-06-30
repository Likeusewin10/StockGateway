"""SDK 会话管理：单会话/单点登录，全局锁串行化所有取数。

三个 SDK（EM / iFinD / Wind）均单会话，本服务用一把全局锁串行化所有请求，
必须单 worker 运行（不要加 --workers）。会话首次使用时惰性登录。

会话自愈：底层会话会被悄悄踢掉（被别处同账号登录挤掉、iFinD/Wind 单点
登录冲突、令牌超时）。`em_exec`/`ths_exec`/`wind_exec` 在取数失败疑似会话失效时，
强制重登一次并重试，避免远程调用报"未登录/已登出"。
"""
import os
import sys
import threading
from typing import Any, Callable

from fastapi import HTTPException

from EmQuantAPI import c
from iFinDPy import THS_iFinDLogin, THS_iFinDLogout
from WindPy import w

from stocksdk.config import (
    get_qmt_account,
    get_qmt_package_dir,
    get_qmt_session_id,
    get_qmt_userdata_path,
    get_tdx_pyplugins_dir,
    require_ths_credentials,
)


def _bootstrap_tdx_path() -> None:
    """把通达信 tqcenter 所在目录注入 sys.path（机制同 _bootstrap_xtquant_path）。

    tqcenter 依赖同目录的 TPyth*.dll/tdxrpc*.dll，故还用 os.add_dll_directory 加该目录。
    测试下 conftest 已把 tqcenter 桩塞进 sys.modules，真实导入被跳过，此注入无副作用。
    """
    pkg = get_tdx_pyplugins_dir()
    if not pkg or not os.path.isdir(pkg):
        return
    if pkg not in sys.path:
        sys.path.append(pkg)
    try:
        os.add_dll_directory(pkg)
    except (AttributeError, OSError):
        pass


_bootstrap_tdx_path()


def _bootstrap_xtquant_path() -> None:
    """把 xtquant 包目录与其原生 DLL 目录注入搜索路径。

    中文安装路径在 .pth 里按本地编码读不可靠，故在导入前显式注入：
    sys.path 加包目录，os.add_dll_directory 加 bin.x64（cp311 pyd 依赖那里的 DLL）。
    测试下 conftest 已把 xtquant 桩塞进 sys.modules，真实导入被跳过，此注入无副作用。
    """
    pkg = get_qmt_package_dir()
    if not pkg or not os.path.isdir(pkg):
        return
    if pkg not in sys.path:
        sys.path.append(pkg)
    bin_dir = os.path.dirname(os.path.dirname(pkg))   # ...\bin.x64
    if os.path.isdir(bin_dir):
        try:
            os.add_dll_directory(bin_dir)
        except (AttributeError, OSError):
            pass


_bootstrap_xtquant_path()

from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback   # noqa: E402
from xtquant.xttype import StockAccount   # noqa: E402

from tqcenter import tq as tdx   # noqa: E402  通达信 TQ 单例（类，方法直接 tdx.xxx()）

# 全局锁：SDK 单会话，所有取数串行化。整个服务唯一一把锁。
lock = threading.Lock()

_em_ready = False
_ths_ready = False
_wind_ready = False
_tdx_ready = False

# 会话/登录失效类错误码（命中即强制重登重试）。
# EM：10001009 登录数超限/被挤、10001005/10001006 未登录类、10001020 令牌失效。
_EM_SESSION_CODES = {10001005, 10001006, 10001009, 10001019, 10001020}
# iFinD：负的会话码，-1010 已登出最常见。
_THS_SESSION_CODES = {-1001, -1010, -1011}
# Wind：已实测 -2(start 失败)、-103(未连接)、-40520004(Login Failed,多实例/脏状态锁冲突)。
_WIND_SESSION_CODES = {-2, -103, -40520004}
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


def ensure_wind(force: bool = False) -> None:
    """Wind WindPy 惰性登录（依赖本机 Wind 终端后台登录鉴权，无需账号密码）。

    force=True 先 w.stop() 再 start，强制重连。校验 ErrorCode==0 且 isconnected()，
    否则抛 502。失败码集见 _WIND_SESSION_CODES（如 -2/-103/-40520004）。
    """
    global _wind_ready
    if _wind_ready and not force:
        return
    if force:
        try:
            w.stop()            # 先停，避免脏状态/多实例锁冲突
        except Exception:
            pass
    r = w.start(waitTime=60)
    code = getattr(r, "ErrorCode", -1)
    if code != 0 or not w.isconnected():
        _wind_ready = False
        raise HTTPException(502, "Wind 登录失败：{} {}".format(code, getattr(r, "Data", "")))
    _wind_ready = True


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


def _wind_session_dead(result: Any) -> bool:
    """Wind WindData / (ErrorCode, DataFrame) 返回是否表示会话/登录失效。

    usedf=True 时返回 (ErrorCode, DataFrame) 元组（wsd/wss 固定端点走此路），
    须按元组首位判码；否则是 WindData 对象，按 .ErrorCode 判。
    坏证券码会返回 ErrorCode=0 + Data=[[None,...]]，故只看 ErrorCode，不因 None 数据判失败。
    """
    if isinstance(result, tuple) and len(result) == 2:
        return result[0] in _WIND_SESSION_CODES
    code = getattr(result, "ErrorCode", None)
    if code in _WIND_SESSION_CODES:
        return True
    if code not in (0, None):
        return _text_has_session_keyword(getattr(result, "Data", ""))
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


def wind_exec(fn: Callable[[], Any]) -> Any:
    """在已登录会话里执行 Wind 取数 thunk；若会话失效则强制重登并重试一次。

    调用方须已持有全局 lock（本函数不自己加锁，沿用现有串行化）。
    """
    ensure_wind()
    r = fn()
    if _wind_session_dead(r):
        ensure_wind(force=True)
        r = fn()
    return r


# ============================================================================
# 通达信 TQ（TdxQuant）取数会话
#
# 与 EM/iFinD/Wind 同构的「单会话取数」：tqcenter.tq 是单例，首次使用时
# ensure_tdx() 调 tq.initialize() 连本机通达信终端，之后取数经全局 lock 串行。
# 前提：本机通达信金融终端已开启并登录（同 QMT 的 XtMiniQmt 模型）。
# 返回 dict 带 'ErrorId' 字段（'0' 为成功）；TQ 无显式会话失效码，连接断时
# initialize 会抛异常，由 tdx_exec 兜底重连重试一次。
# ============================================================================

# initialize 需要一个路径参数（官方样例传 __file__），仅用于 TQ 内部标识。
_TDX_INIT_PATH = os.path.abspath(__file__)


def ensure_tdx(force: bool = False) -> None:
    """通达信 TQ 惰性初始化（依赖本机终端已登录，无需账号密码）。

    force=True 无视 flag 重新 initialize。initialize 失败（终端未开/未登录）抛 502。
    调用方须已持有全局 lock。
    """
    global _tdx_ready
    if _tdx_ready and not force:
        return
    try:
        tdx.initialize(_TDX_INIT_PATH)
    except Exception as e:
        _tdx_ready = False
        raise HTTPException(502, "TDX 初始化失败（确认通达信终端已开启并登录）：{}".format(e))
    _tdx_ready = True


def _tdx_session_dead(result: Any) -> bool:
    """通达信 TQ 返回是否表示会话/连接失效。

    返回 dict 时看 ErrorId（非 '0'/0 且消息含登录关键词判失效）；
    None / 空（取数彻底失败，常因终端断连）也视为失效，触发一次重连重试。
    """
    if result is None:
        return True
    if isinstance(result, dict):
        eid = result.get("ErrorId")
        if eid not in ("0", 0, None):
            return _text_has_session_keyword(result.get("Error", "") or result.get("Msg", ""))
    return False


def tdx_exec(fn: Callable[[], Any]) -> Any:
    """在已初始化会话里执行 TDX 取数 thunk；连接失效则重新 initialize 并重试一次。

    调用方须已持有全局 lock（本函数不自己加锁，沿用现有串行化）。
    """
    ensure_tdx()
    try:
        r = fn()
    except Exception:
        ensure_tdx(force=True)
        r = fn()
        return r
    if _tdx_session_dead(r):
        ensure_tdx(force=True)
        r = fn()
    return r


# ============================================================================
# QMT（君弘君智 / 迅投 XtQuant）交易会话
#
# 与 EM/iFinD/Wind 的「无状态取数」不同，QMT 是长连接 trader + 异步回调推送：
# 服务首次使用时 ensure_qmt() 建立单例 XtQuantTrader 并 start/connect/subscribe，
# 之后下单/撤单/查询经全局 lock 串行。委托/成交/错误回调写入 _qmt_events（线程安全），
# 仅供审计/观测——查询端点直接走 query_stock_*（权威值），回调内绝不调 query_*（防卡死）。
#
# 前提：本机 XtMiniQmt.exe 已登录（极简/独立模式）。connect()!=0 视为未就绪 → 502。
# ============================================================================

from collections import deque   # noqa: E402

_qmt_trader: Any = None
_qmt_account: Any = None
_qmt_ready = False
_qmt_events: deque = deque(maxlen=500)   # 最近的委托/成交/错误回调（审计用）


class _QmtCallback(XtQuantTraderCallback):
    """交易回调：仅把事件入队，不在回调线程里调用任何 query_* 接口（否则后续回调卡死）。"""

    def on_disconnected(self):
        global _qmt_ready
        _qmt_ready = False
        _qmt_events.append({"event": "disconnected"})

    def on_stock_order(self, order):
        _qmt_events.append({"event": "order", "order_id": getattr(order, "order_id", None),
                            "stock_code": getattr(order, "stock_code", None),
                            "order_status": getattr(order, "order_status", None)})

    def on_stock_trade(self, trade):
        _qmt_events.append({"event": "trade", "order_id": getattr(trade, "order_id", None),
                            "stock_code": getattr(trade, "stock_code", None),
                            "traded_volume": getattr(trade, "traded_volume", None)})

    def on_order_error(self, err):
        _qmt_events.append({"event": "order_error", "order_id": getattr(err, "order_id", None),
                            "error_id": getattr(err, "error_id", None),
                            "error_msg": getattr(err, "error_msg", None)})

    def on_cancel_error(self, err):
        _qmt_events.append({"event": "cancel_error", "order_id": getattr(err, "order_id", None),
                            "error_id": getattr(err, "error_id", None),
                            "error_msg": getattr(err, "error_msg", None)})


def qmt_account() -> Any:
    """返回当前 StockAccount 对象（ensure_qmt 后可用）。"""
    return _qmt_account


def recent_qmt_events() -> list:
    """最近的交易回调事件快照（审计/观测）。"""
    return list(_qmt_events)


def ensure_qmt(force: bool = False) -> Any:
    """建立/复用 QMT 单例 trader 并连接终端。返回 trader；失败抛 502。

    依赖本机 XtMiniQmt 已登录。connect() 非 0 视为未就绪。
    调用方须已持有全局 lock（本函数不自己加锁）。
    """
    global _qmt_trader, _qmt_account, _qmt_ready
    if _qmt_ready and not force and _qmt_trader is not None:
        return _qmt_trader

    if _qmt_trader is None:
        path = get_qmt_userdata_path()
        session_id = get_qmt_session_id()
        _qmt_trader = XtQuantTrader(path, session_id)
        _qmt_trader.register_callback(_QmtCallback())
        _qmt_trader.start()

    account_id, account_type = get_qmt_account()
    _qmt_account = StockAccount(account_id, account_type)

    code = _qmt_trader.connect()
    if code != 0:
        _qmt_ready = False
        raise HTTPException(502, "QMT 连接失败：connect()={}（确认 XtMiniQmt 已登录）".format(code))
    _qmt_trader.subscribe(_qmt_account)
    _qmt_ready = True
    return _qmt_trader
