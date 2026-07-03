"""MCP 聚合网关 —— 网关全局配置（端口、API Key、.env 加载）。

凭据读取分两类：
- 网关对外鉴权用的 API_KEY、网关端口 —— 在此读取。
- 各厂商上游凭据 —— 不在此，按 provider 的 auth_env 在 upstream.py 读取并收口。

复用根项目 stocksdk 的 .env 加载，避免两套 .env 解析逻辑漂移。
"""
import logging
import os
import re
import sys
from pathlib import Path

# 让网关能复用 stocksdk.config.load_dotenv（同一份 .env 解析）。
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from stocksdk.config import load_dotenv  # noqa: E402  复用唯一的 .env 加载器

logger = logging.getLogger("mcp_gateway.config")

# ---- 常量 ----
DEFAULT_GATEWAY_HOST = "0.0.0.0"
DEFAULT_GATEWAY_PORT = 8765       # 与现有 REST 服务 8000 隔离，二者可并存
MCP_PATH = "/mcp"                 # streamable-http 挂载路径

# ---- 网关限流（不同于 REST 的 60/60s）----
# MCP streamable-http 客户端行为与取数完全不同：一次会话会密集调几十个工具，
# 且 SSE 长流断线每 1000ms 重连；经 ngrok 后所有客户端的 request.client.host
# 折叠成同一隧道 IP。若沿用 REST 的 60/60s 按 IP，单个正常客户端秒级打满限流，
# 表现为 initialize 过、紧接的 tools/list 被拦（客户端报 tools fetch failed）。
# 故网关：① 限流键优先用 mcp-session-id（每会话独立预算，非折叠 IP）；
# ② 阈值放宽到 600/60s；③ SSE 的 GET 与会话拆除 DELETE 属传输控制、不计限流。
GATEWAY_RATE_LIMIT_REQUESTS = 600
GATEWAY_RATE_LIMIT_WINDOW_SECONDS = 60

# ---- 服务器端 Agent 工具（agent_run/agent_status/agent_result）----
# 子进程执行目录：锁死本仓库根，防止任意路径读写。可用 AGENT_PROJECT_DIR 覆盖。
AGENT_PROJECT_DIR_DEFAULT = str(_ROOT)

# 引擎命令模板：每引擎拆「首轮(fresh)」「续轮(resume)」两套 argv。
#   {prompt}     处替换为用户 prompt；
#   {session_id} 处替换为会话 id（claude 由服务器预生成并经 --session-id 注入；
#                codex 首轮不带、终态从 --json 输出解析，续轮经 resume 子命令带回）。
# 两个引擎均全自动、非交互。
# 🔴 安全：--dangerously-* flag = 拿到 X-API-Key 即可让服务器 Agent 无确认执行任意命令。
#    配套防线：① API_KEY 强随机且只发可信机器；② cwd 锁死 AGENT_PROJECT_DIR。
# 所有引擎自身 flag 放在 `--` 之前，{prompt} 放最后：`--` 结束选项解析，
# 防止以 `-` 开头的 prompt 被 CLI 当成 flag（argument injection）。
# claude 加 --output-format json：让输出为结构化 JSON 信封（output 原样透传，不解包）。
AGENT_ENGINES: dict[str, dict[str, list[str]]] = {
    "claude": {
        # 首轮：服务器预生成 UUID 经 --session-id 注入，id 在 submit 那一刻即确定。
        "fresh": [
            "claude", "-p", "--output-format", "json",
            "--session-id", "{session_id}",
            "--dangerously-skip-permissions", "--", "{prompt}",
        ],
        # 续轮：--resume <uuid> 自动加载该会话全部历史。
        "resume": [
            "claude", "-p", "--output-format", "json",
            "--resume", "{session_id}",
            "--dangerously-skip-permissions", "--", "{prompt}",
        ],
    },
    "codex": {
        # 首轮：codex 自己生成 id，不可指定；--json 输出 JSONL 供终态解析 id。
        "fresh": [
            "codex", "exec", "--json",
            "--dangerously-bypass-approvals-and-sandbox", "--", "{prompt}",
        ],
        # 续轮：codex exec resume <uuid> 续接。
        "resume": [
            "codex", "exec", "resume", "{session_id}", "--json",
            "--dangerously-bypass-approvals-and-sandbox", "--", "{prompt}",
        ],
    },
}

# Streaming variant used when AGENT_STREAM_JSON is on (claude only).
AGENT_ENGINES_STREAM: dict[str, dict[str, list[str]]] = {
    "claude": {
        "fresh": [
            "claude", "-p", "--output-format", "stream-json", "--verbose",
            "--session-id", "{session_id}",
            "--dangerously-skip-permissions", "--", "{prompt}",
        ],
        "resume": [
            "claude", "-p", "--output-format", "stream-json", "--verbose",
            "--resume", "{session_id}",
            "--dangerously-skip-permissions", "--", "{prompt}",
        ],
    },
}

# Live persistent-stdin session variant: prompt is sent over stdin, not argv.
AGENT_ENGINES_LIVE: dict[str, dict[str, list[str]]] = {
    "claude": {
        "fresh": [
            "claude", "-p", "--input-format", "stream-json",
            "--output-format", "stream-json", "--verbose",
            "--dangerously-skip-permissions",
            "--session-id", "{session_id}",
        ],
        "resume": [
            "claude", "-p", "--input-format", "stream-json",
            "--output-format", "stream-json", "--verbose",
            "--dangerously-skip-permissions",
            "--resume", "{session_id}",
        ],
    },
}

# codex --json(JSONL) 首轮输出里 session id 的候选字段名，按序探测（容版本字段名差异）。
CODEX_SESSION_ID_KEYS: tuple[str, ...] = ("session_id", "conversation_id", "thread_id", "id")

AGENT_TASK_TIMEOUT_SECONDS = 600   # 单任务上限,超时 kill,防僵进程占满服务器
AGENT_MAX_TASKS = 100              # 内存中保留的最近任务数,超出按完成顺序清理最旧

# Stream agent subprocess output as JSON events; off by default.
AGENT_STREAM_JSON = os.environ.get("AGENT_STREAM_JSON", "1").strip().lower() in {"1", "true", "yes", "on"}
# Max number of streamed events buffered in memory per task.
AGENT_EVENT_BUFFER_MAX = int(os.environ.get("AGENT_EVENT_BUFFER_MAX", "2000"))
# Idle seconds before a live persistent session is reaped.
AGENT_SESSION_IDLE_SECONDS = int(os.environ.get("AGENT_SESSION_IDLE_SECONDS", "300"))
# Max number of concurrent live persistent sessions kept alive.
AGENT_MAX_LIVE_SESSIONS = int(os.environ.get("AGENT_MAX_LIVE_SESSIONS", "8"))

# ---- 会话列表（agent_sessions 工具，仿原生 /resume）----
# CLI 本身不暴露 list 子命令；两个引擎都把会话存成可扫描的 JSONL：
#   claude: ~/.claude/projects/<编码cwd>/<uuid>.jsonl     （文件名即 session_id）
#   codex:  ~/.codex/sessions/YYYY/MM/DD/rollout-*-<uuid>.jsonl （首行 session_meta.payload.id）
# 两个根经 get_claude_projects_dir / get_codex_sessions_dir 动态读取（可被 env 覆盖，便于测试）。
AGENT_SESSIONS_LIST_LIMIT = 30     # agent_sessions 默认/最多回多少条会话
AGENT_SESSION_TITLE_MAXLEN = 80    # 派生标题截断长度,防外泄过长用户原文


def get_claude_projects_dir() -> Path:
    """claude 会话存储根；CLAUDE_PROJECTS_DIR 留空则用 ~/.claude/projects。

    动态读取（而非 import 时定值），便于测试用 env 指向 tmp 目录。
    """
    raw = os.environ.get("CLAUDE_PROJECTS_DIR", "").strip()
    return Path(raw) if raw else (Path.home() / ".claude" / "projects")


def get_codex_sessions_dir() -> Path:
    """codex 会话存储根；CODEX_SESSIONS_DIR 留空则用 ~/.codex/sessions。

    动态读取（而非 import 时定值），便于测试用 env 指向 tmp 目录。
    """
    raw = os.environ.get("CODEX_SESSIONS_DIR", "").strip()
    return Path(raw) if raw else (Path.home() / ".codex" / "sessions")



def encode_claude_project_dir(cwd: str) -> str:
    """把 cwd 路径转成 claude 的 projects 子目录编码。

    规则由真实样本反推（已对拍多个样本）：把 `:` `\\` `/` 各替换成 `-`。
    例：`D:\\dev\\Project\\StockSDK` → `D--dev-Project-StockSDK`
       （`D:` 的冒号 → `-`，紧跟的 `\\dev` 的反斜杠 → `-`，故出现连续 `--`）。
    """
    return re.sub(r"[:\\/]", "-", cwd)



def get_gateway_port() -> int:
    """网关监听端口；MCP_GATEWAY_PORT 留空则用默认 8765。"""
    raw = os.environ.get("MCP_GATEWAY_PORT", "").strip()
    return int(raw) if raw else DEFAULT_GATEWAY_PORT


def get_api_key() -> str:
    """网关对外鉴权 key；留空表示不鉴权（仅本机/内网场景）。"""
    return os.environ.get("API_KEY", "").strip()


def get_agent_project_dir() -> str:
    """Agent 子进程执行目录；AGENT_PROJECT_DIR 留空则锁死本仓库根。

    安全：覆盖值必须仍在本仓库根内（防 env 被改后把 cwd 指向任意路径，绕过目录锁）。
    越界则告警并回退默认根。
    """
    raw = os.environ.get("AGENT_PROJECT_DIR", "").strip()
    if not raw:
        return AGENT_PROJECT_DIR_DEFAULT
    resolved = Path(raw).resolve()
    root = Path(AGENT_PROJECT_DIR_DEFAULT).resolve()
    if resolved != root and root not in resolved.parents:
        logger.warning("AGENT_PROJECT_DIR %r 在项目根之外，已回退默认根", raw)
        return AGENT_PROJECT_DIR_DEFAULT
    return str(resolved)
