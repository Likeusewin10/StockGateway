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
from mcp_gateway.config import MCP_PATH, get_api_key, load_dotenv
from mcp_gateway.providers import PROVIDERS
from mcp_gateway.upstream import iter_upstreams

load_dotenv()

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
    # 本机自有工具：服务器端 Agent（agent_run/agent_status/agent_result/agent_sessions），命名空间 agent。
    gateway.mount(agent_tools, namespace="agent")
    logger.info("已挂载本机工具 -> 前缀 agent（agent_run/agent_status/agent_result/agent_sessions）")
    logger.info("网关挂载完成：%d 个上游 server", mounted)
    if mounted == 0:
        logger.warning("没有任何上游被挂载：请检查各厂商凭据环境变量（如 IFIND_MCP_JWT）")
    return gateway


def build_app():
    """构造对外 ASGI 应用（带鉴权/限流中间件）。"""
    if not get_api_key():
        logger.warning("未配置 API_KEY：网关当前不鉴权，请勿暴露到公网")
    gateway = build_gateway()
    return gateway.http_app(
        path=MCP_PATH,
        middleware=[Middleware(ApiKeyAuthMiddleware)],
    )


http_app = build_app()
