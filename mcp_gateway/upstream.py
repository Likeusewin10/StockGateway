"""上游 MCP client 构造 + 凭据收口。

凭据读取唯一入口在 _auth_headers：按 provider.auth_env 读环境变量，按 auth_scheme/auth_header
注入。凭据绝不写入日志、repr 或对外响应。缺凭据的 provider 跳过并 warning，不拖垮整个网关。
"""
import logging
import os

import httpx
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from mcp.shared._httpx_utils import create_mcp_http_client

from mcp_gateway.providers import Provider, ProviderServer

logger = logging.getLogger("mcp_gateway.upstream")


def _timeout_factory(provider: Provider):
    """按 provider 超时配置生成 httpx_client_factory；未配超时返回 None(走上游默认)。

    FastMCP 3.x 的 StreamableHttpTransport 不直接接受请求级 timeout，只能经
    httpx_client_factory 注入 httpx.Timeout。工厂内不记录 headers(含凭据)。
    """
    if provider.connect_timeout is None and provider.read_timeout is None:
        return None

    timeout_cfg = httpx.Timeout(
        connect=provider.connect_timeout,
        read=provider.read_timeout,
        write=provider.read_timeout,
        pool=provider.connect_timeout,
    )

    def factory(headers=None, timeout=None, auth=None, **kwargs):  # noqa: ARG001
        # fastmcp 调用时会多传 follow_redirects 等 kwargs(见其 http.py)，用 **kwargs 吞掉；
        # 传入的 timeout 被忽略，强制用本 provider 配置的 timeout。
        # create_mcp_http_client 自身已 follow_redirects=True，无需再传。
        return create_mcp_http_client(headers=headers, timeout=timeout_cfg, auth=auth)

    return factory


def _auth_headers(provider: Provider) -> dict[str, str] | None:
    """按 provider 配置生成鉴权 header；凭据缺失返回 None 并告警。"""
    if not provider.auth_env:
        return {}  # 该厂商无需鉴权
    token = os.environ.get(provider.auth_env, "").strip()
    if not token:
        logger.warning(
            "厂商 %s 缺少凭据环境变量 %s，已跳过该厂商", provider.name, provider.auth_env
        )
        return None
    return {provider.auth_header: f"{provider.auth_scheme}{token}"}


def make_server_client(provider: Provider, server: ProviderServer, headers: dict[str, str]) -> Client:
    """为单个上游 server 构造 streamable-http client。"""
    factory = _timeout_factory(provider)
    kwargs: dict = {"url": provider.server_url(server), "headers": headers}
    if factory is not None:
        kwargs["httpx_client_factory"] = factory
    transport = StreamableHttpTransport(**kwargs)
    return Client(transport, name=provider.prefix(server))


def iter_upstreams(provider: Provider):
    """产出 (server, client) —— 凭据缺失时不产出任何项（跳过整个 provider）。"""
    headers = _auth_headers(provider)
    if headers is None:
        return
    for server in provider.servers:
        yield server, make_server_client(provider, server, headers)
