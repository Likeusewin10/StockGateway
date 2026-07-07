"""对等机（peer）Agent 网关注册 —— 多机协同的 hub 侧接入点。

拓扑：本机（hub）网关把另外 N 台机器上的 agent-only 网关当作上游 MCP 挂载，
工具前缀 peer_<机器名>_*（如 peer_pc2_agent_run），客户端只连 hub 一个入口。

配置全部走环境变量（每台机器的 peers 不同，不硬编码进 providers.py）：

    MCP_PEERS=pc2=http://47.76.104.225:18766/mcp,pc3=http://47.76.104.225:18767/mcp
    PEER_PC2_API_KEY=<pc2 网关的 API_KEY>
    PEER_PC3_API_KEY=<pc3 网关的 API_KEY>

复用 providers.Provider / upstream.iter_upstreams 全套机制：缺 key 的 peer 被跳过
（warning）不拖垮网关；凭据经 X-API-Key 头注入、绝不入日志。

🔴 connect_timeout 必须短（对等机随时可能关机）：否则一台 peer 宕机会拖慢
hub 的 tools/list 乃至整个网关初始化。

⚠ 不要把 hub 自己的地址写进 MCP_PEERS —— 会造成网关自我代理（环形）。
"""
import logging
import os
import re

from mcp_gateway.providers import Provider, ProviderServer

logger = logging.getLogger("mcp_gateway.peers")

# peer 名规范化后必须匹配（作为工具前缀的一部分，只允许小写字母数字下划线且字母开头）
_PEER_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")

# 对等机连接/读超时（秒）。connect 必须短：peer 宕机不能拖死 hub。
# read 只需覆盖 MCP 单次工具调用（agent_run 立即返 task_id，不等子进程跑完）。
PEER_CONNECT_TIMEOUT_SECONDS = 5
PEER_READ_TIMEOUT_SECONDS = 60


def _normalize_peer_name(raw: str) -> str | None:
    """规范化 peer 名（小写、连字符转下划线）；不合法返回 None。"""
    name = raw.strip().lower().replace("-", "_")
    if not _PEER_NAME_RE.match(name):
        return None
    return name


def peer_key_env(name: str) -> str:
    """该 peer 的 API Key 环境变量名，如 pc2 -> PEER_PC2_API_KEY。"""
    return f"PEER_{name.upper()}_API_KEY"


def load_peers(raw: str | None = None) -> tuple[Provider, ...]:
    """解析 MCP_PEERS 生成 Provider 元组；畸形条目跳过并告警，不抛异常。

    每个 peer 一个独立 Provider（name 统一为 "peer"、server short_name 为机器名，
    最终前缀 peer_<机器名>）；auth_env 各自独立（一机一 key，泄露不殃及全网）。
    """
    if raw is None:
        raw = os.environ.get("MCP_PEERS", "")
    providers: list[Provider] = []
    seen: set[str] = set()
    for entry in raw.split(","):
        entry = entry.strip()
        if not entry:
            continue
        name_part, sep, url = entry.partition("=")
        url = url.strip()
        if not sep or not url:
            logger.warning("MCP_PEERS 条目缺 '=url'，已跳过：%r", entry)
            continue
        name = _normalize_peer_name(name_part)
        if name is None:
            logger.warning("MCP_PEERS 条目 peer 名不合法（需小写字母数字下划线且字母开头），已跳过：%r", entry)
            continue
        if not url.lower().startswith(("http://", "https://")):
            logger.warning("MCP_PEERS 条目 URL 非 http(s)，已跳过：%r", entry)
            continue
        if name in seen:
            logger.warning("MCP_PEERS 出现重复 peer 名 %s，后者已跳过", name)
            continue
        seen.add(name)
        providers.append(Provider(
            name="peer",
            base_url=url,
            servers=(ProviderServer(name=name, short_name=name),),
            auth_env=peer_key_env(name),
            auth_header="X-API-Key",
            auth_scheme="",
            url_template="{base_url}",
            connect_timeout=PEER_CONNECT_TIMEOUT_SECONDS,
            read_timeout=PEER_READ_TIMEOUT_SECONDS,
        ))
    return tuple(providers)
