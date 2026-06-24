"""多厂商 MCP 上游注册表（纯数据，无副作用）。

设计目标：加新厂商 = 往 PROVIDERS 追加一个 Provider 条目 + 在 .env 填该厂商凭据环境变量，
不改网关任何执行代码。

命名空间：每个上游 server 最终以 f"{provider.name}_{server.short_name}" 作为 mount 前缀，
provider.name 全局唯一，天然隔离不同厂商的同名 server / 工具。

安全：凭据本身不在此（此处只放“环境变量名” auth_env），真正读取在 upstream.py 收口，
绝不把凭据写进注册表、日志或对外响应。
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProviderServer:
    """上游一个 MCP server。"""

    name: str               # 上游 server 名，用于拼 URL，如 "hexin-ifind-ds-stock-mcp"
    short_name: str         # 前缀用短名，如 "stock" -> 工具前缀 ifind_stock_


@dataclass(frozen=True)
class Provider:
    """一个上游厂商：一组同源 MCP server + 统一鉴权方式。"""

    name: str                            # 厂商命名空间，全局唯一，如 "ifind"
    base_url: str                        # 上游公共前缀
    servers: tuple[ProviderServer, ...]
    auth_env: str | None = None          # 该厂商凭据的环境变量名，如 "IFIND_MCP_JWT"
    auth_header: str = "Authorization"   # 凭据注入到哪个 header
    auth_scheme: str = ""                # 头部前缀，如 "Bearer "；裸 token 留空
    transport: str = "http"              # 当前仅 streamable-http
    adapter: str = "fastmcp_proxy"       # 预留：不兼容时切 "raw_reverse_proxy"
    url_template: str = "{base_url}/{server}"

    def server_url(self, server: ProviderServer) -> str:
        """拼接某 server 的完整上游 URL。"""
        return self.url_template.format(base_url=self.base_url, server=server.name)

    def prefix(self, server: ProviderServer) -> str:
        """该 server 在网关里的 mount 前缀（命名空间隔离）。"""
        return f"{self.name}_{server.short_name}"


# ---- 厂商注册表 ----------------------------------------------------------
# iFinD（同花顺）：7 个 server 共用一个上游 JWT（裸 JWE，直接整串放 Authorization）。
_IFIND_SERVERS = tuple(
    ProviderServer(name=f"hexin-ifind-ds-{s}-mcp", short_name=s.replace("-", "_"))
    for s in ("stock", "fund", "edb", "news", "bond", "global-stock", "index")
)

IFIND = Provider(
    name="ifind",
    base_url="https://api-mcp.51ifind.com:8643/ds-mcp-servers",
    servers=_IFIND_SERVERS,
    auth_env="IFIND_MCP_JWT",
    auth_header="Authorization",
    auth_scheme="",          # iFinD 当前是裸 JWE，不加 "Bearer " 前缀
)

# 妙想（东方财富 MX）：单个 server，鉴权头是 em_api_key（裸 key，无 scheme 前缀）。
# 上游 URL 是单一完整地址（base_url 本身即终点，无 /{server} 子路径），故 url_template
# 只用 {base_url}；short_name 决定工具前缀 mx_ds_。
MX = Provider(
    name="mx",
    base_url="https://mxapi.eastmoney.com/mxds/mcp",
    servers=(ProviderServer(name="mx-ds-mcp", short_name="ds"),),
    auth_env="EM_API_KEY",
    auth_header="em_api_key",
    auth_scheme="",          # 裸 key，不加前缀
    url_template="{base_url}",
)

# 以后追加厂商：PROVIDERS = (IFIND, MX, WIND, CHOICE, ...)
PROVIDERS: tuple[Provider, ...] = (IFIND, MX)
