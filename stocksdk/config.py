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
