"""父网关：遍历厂商注册表，把每个上游 server 代理挂载到统一的 streamable-http 网关。

工具前缀 = f"{provider}_{server_short}"，跨厂商命名空间隔离。
缺凭据的厂商在 upstream.iter_upstreams 处被跳过（warning），不影响其它厂商。
导出 http_app（ASGI app）供 uvicorn 运行：uvicorn mcp_gateway.server:http_app
"""
import logging

from fastmcp import FastMCP
from fastmcp.server import create_proxy
from starlette.middleware import Middleware

from mcp_gateway.auth import ApiKeyAuthMiddleware
from mcp_gateway.agent_tools import agent as agent_tools
from mcp_gateway.aggregation import ToolAggregationMiddleware
from mcp_gateway.config import (
    GATEWAY_MODE_AGENT_ONLY,
    MCP_PATH,
    get_api_key,
    get_gateway_mode,
    load_dotenv,
)
from mcp_gateway.peers import load_peer_mcps
from mcp_gateway.providers import PROVIDERS
from mcp_gateway.upstream import iter_upstreams

load_dotenv()

# 让上游 TLS 走操作系统信任库（与 curl/浏览器一致），而非 certifi 自带 CA bundle。
# 某些环境（企业代理 / 杀软 TLS 检测根证书）只把根证书装进 OS 信任库，certifi 里没有，
# 会导致 httpx 报 CERTIFICATE_VERIFY_FAILED、所有上游 list_tools 失败。truststore 缺失时静默跳过。
try:
    import truststore

    truststore.inject_into_ssl()
except Exception:  # noqa: BLE001  truststore 未装或注入失败都不应拖垮网关启动
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("mcp_gateway")


def build_gateway() -> FastMCP:
    """构造父网关并挂载所有可用厂商的上游代理。"""
    gateway = FastMCP(name="mcp-gateway")
    mounted = 0
    for provider in PROVIDERS:
        for server, client in iter_upstreams(provider):
            proxy = create_proxy(client)
            gateway.mount(proxy, namespace=provider.prefix(server))
            mounted += 1
            logger.info("已挂载上游 %s -> 前缀 %s", server.name, provider.prefix(server))
        # aggregate 厂商:该厂商全部 server 的原始工具在网关层收成分类分发工具
        # (tushare_ds_* 258 个 → tushare_cat_* ~13 个,原始工具从 tools/list 隐藏但仍可被改写调用)。
        if provider.aggregate:
            for server in provider.servers:
                gateway.add_middleware(ToolAggregationMiddleware(
                    raw_prefix=f"{provider.prefix(server)}_",
                    cat_prefix=f"{provider.name}_cat_",
                ))
                logger.info("已启用工具聚合:%s_* -> %s_cat_*", provider.prefix(server), provider.name)
    # 本机自有工具：服务器端 Agent（agent_run/agent_status/agent_result/agent_sessions），命名空间 agent。
    gateway.mount(agent_tools, namespace="agent")
    logger.info("已挂载本机工具 -> 前缀 agent（agent_run/agent_status/agent_result/agent_sessions）")
    # 对等机（多机协同）：MCP_PEERS 定义，缺 key 的 peer 被跳过（warning）。
    # 对等机现跑纯 HTTP 哑执行服务（peer_service.py），hub 侧注册原生工具经 HTTP 调它，
    # 挂载后即 peer_<机器名>_agent_run/_status/_result/fs_*/svc_* 等。
    for name, peer_mcp in load_peer_mcps():
        gateway.mount(peer_mcp, namespace=f"peer_{name}")
        logger.info("已挂载对等机 %s -> 前缀 peer_%s", name, name)
    logger.info("网关挂载完成：%d 个上游 server", mounted)
    if mounted == 0:
        logger.warning("没有任何上游被挂载：请检查各厂商凭据环境变量（如 IFIND_MCP_JWT）")
    return gateway


def build_app():
    """构造对外 ASGI 应用（带鉴权/限流中间件）。

    MCP_GATEWAY_MODE=agent-only：对等机形态，只暴露本机 agent 工具（裸名
    agent_run 等，无 agent_ 前缀），不挂任何厂商上游/peers —— hub 挂载它时
    加 peer_<机器名>_ 前缀即得 peer_pc2_agent_run。鉴权中间件两种模式一致。
    """
    if not get_api_key():
        logger.warning("未配置 API_KEY：网关当前不鉴权，请勿暴露到公网")
    if get_gateway_mode() == GATEWAY_MODE_AGENT_ONLY:
        logger.info("agent-only 模式：仅暴露本机 agent 工具（供 hub 对等挂载），不挂任何厂商上游")
        return agent_tools.http_app(
            path=MCP_PATH,
            middleware=[Middleware(ApiKeyAuthMiddleware)],
        )
    gateway = build_gateway()
    return gateway.http_app(
        path=MCP_PATH,
        middleware=[Middleware(ApiKeyAuthMiddleware)],
    )


http_app = build_app()
