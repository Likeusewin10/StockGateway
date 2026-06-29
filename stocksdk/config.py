"""集中配置：唯一的 .env 加载器 + 类型化设置/常量。

只依赖标准库，三个 venv（api/em/ths）均可导入。
凭据一律从环境变量 / .env 读取，无硬编码。
"""
import os
from pathlib import Path

# ---- 常量（原散落在各处的魔法数字）----
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
WS_QUEUE_MAXSIZE = 1000          # 每条 WS 连接的推送队列上限（原 app.py:325/397）
RESTART_DELAY_SECONDS = 5        # 看门狗重启间隔（原 start_server.bat）
RATE_LIMIT_REQUESTS = 60         # 每个 IP 在窗口内允许的取数请求数
RATE_LIMIT_WINDOW_SECONDS = 60   # 限流时间窗口（秒）

# ---- QMT（君弘君智 / 迅投 XtQuant）交易接入默认值 ----
# 项目定位由「只读」扩为「读+交易」：QMT 是唯一交易源，下单经多重护栏。
QMT_DEFAULT_SESSION_ID = 100          # XtQuantTrader 会话号（单 worker 固定即可，需唯一）
QMT_DEFAULT_MAX_NOTIONAL = 50000.0    # 单笔委托金额上限（volume×price），默认 5 万
QMT_DEFAULT_DAILY_ORDER_CAP = 50      # 当日累计下单笔数上限
# xtquant 包目录（含 cp311 原生 pyd）。中文路径在 .pth 里编码不可靠，故在 sessions.py
# 导入前用 sys.path + os.add_dll_directory 显式注入；可经 QMT_PACKAGE_DIR 覆盖。
QMT_DEFAULT_PACKAGE_DIR = r"D:\Softwares\君弘君智交易系统\bin.x64\Lib\site-packages"

# .env 路径：项目根目录（本文件位于 stocksdk/ 下，故取父目录的父目录）
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def load_dotenv(path: Path = _ENV_PATH) -> None:
    """极简 .env 加载：KEY=value 逐行，忽略空行与 # 注释。

    用 setdefault：已存在的真实环境变量优先，不被 .env 覆盖。
    文件不存在时静默跳过（容器/CI 场景靠真实环境变量注入）。
    """
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def get_api_key() -> str:
    """远程鉴权 key；留空表示不鉴权（仅本机/内网场景）。"""
    return os.environ.get("API_KEY", "").strip()


def get_cors_origins() -> list[str]:
    """CORS 允许的来源白名单，逗号分隔；留空表示默认拒绝跨域。"""
    raw = os.environ.get("CORS_ORIGINS", "").strip()
    if not raw:
        return []
    return [o.strip() for o in raw.split(",") if o.strip()]


def require_ths_credentials() -> tuple[str, str]:
    """返回 (THS_USER, THS_PWD)，缺失则抛 RuntimeError。"""
    user = os.environ.get("THS_USER")
    pwd = os.environ.get("THS_PWD")
    if not user or not pwd:
        raise RuntimeError("缺少环境变量 THS_USER / THS_PWD（检查 .env）")
    return user, pwd


# ---- QMT 配置读取（全部实时读 env，便于按请求生效与测试）----

def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return default
    return raw in ("1", "true", "yes", "on")


def is_qmt_trading_enabled() -> bool:
    """交易总开关：默认关。关时 /qmt/order、/qmt/cancel 等写操作返回 503。"""
    return _env_flag("QMT_TRADING_ENABLED", False)


def is_qmt_offhours_allowed() -> bool:
    """是否允许非交易时段下单（默认否）。测试/调试可置 true。"""
    return _env_flag("QMT_ALLOW_OFFHOURS", False)


def get_qmt_userdata_path() -> str:
    """miniQMT 的 userdata_mini 完整路径，缺失抛 RuntimeError。"""
    path = os.environ.get("QMT_USERDATA_PATH", "").strip()
    if not path:
        raise RuntimeError("缺少环境变量 QMT_USERDATA_PATH（miniQMT userdata_mini 路径）")
    return path


def get_qmt_account() -> tuple[str, str]:
    """返回 (资金账号, 账号类型)。类型默认 STOCK；缺账号抛 RuntimeError。"""
    account_id = os.environ.get("QMT_ACCOUNT_ID", "").strip()
    if not account_id:
        raise RuntimeError("缺少环境变量 QMT_ACCOUNT_ID（资金账号）")
    account_type = os.environ.get("QMT_ACCOUNT_TYPE", "STOCK").strip() or "STOCK"
    return account_id, account_type


def get_qmt_session_id() -> int:
    """XtQuantTrader 会话号。"""
    raw = os.environ.get("QMT_SESSION_ID", "").strip()
    return int(raw) if raw else QMT_DEFAULT_SESSION_ID


def get_qmt_package_dir() -> str:
    """xtquant 包所在目录（site-packages）。"""
    return os.environ.get("QMT_PACKAGE_DIR", QMT_DEFAULT_PACKAGE_DIR).strip()


def get_qmt_max_notional() -> float:
    """单笔委托金额上限（元）。"""
    raw = os.environ.get("QMT_MAX_NOTIONAL", "").strip()
    return float(raw) if raw else QMT_DEFAULT_MAX_NOTIONAL


def get_qmt_daily_order_cap() -> int:
    """当日累计下单笔数上限。"""
    raw = os.environ.get("QMT_DAILY_ORDER_CAP", "").strip()
    return int(raw) if raw else QMT_DEFAULT_DAILY_ORDER_CAP


def get_qmt_code_whitelist() -> list[str]:
    """标的白名单（逗号分隔）。留空表示不限制。"""
    raw = os.environ.get("QMT_CODE_WHITELIST", "").strip()
    if not raw:
        return []
    return [c.strip() for c in raw.split(",") if c.strip()]
