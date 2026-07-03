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
    auth_query: str | None = None        # 若上游把凭据放 URL 查询串（如 Tushare ?token=），填参数名；
                                         # 非 None 时凭据经查询串注入、不进 header（见 upstream.py）
    transport: str = "http"              # 当前仅 streamable-http
    adapter: str = "fastmcp_proxy"       # 预留：不兼容时切 "raw_reverse_proxy"
    url_template: str = "{base_url}/{server}"
    connect_timeout: float | None = None  # 上游 TCP 连接超时(秒)；None=沿用上游默认
    read_timeout: float | None = None     # 上游读/请求超时(秒)；None=沿用上游默认
    aggregate: bool = False               # True=该厂商工具在网关层聚合成分类分发工具
                                          # (tool-per-API 型"吵闹"厂商用,见 aggregation.py)

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
# 凭据环境变量名按官方参考用 MIAO_XIANG_MCP_KEY；超时按官方 connectTimeout:10 / timeout:120。
MX = Provider(
    name="mx",
    base_url="https://mxapi.eastmoney.com/mxds/mcp",
    servers=(ProviderServer(name="mx-ds-mcp", short_name="ds"),),
    auth_env="MIAO_XIANG_MCP_KEY",
    auth_header="em_api_key",
    auth_scheme="",          # 裸 key，不加前缀
    url_template="{base_url}",
    connect_timeout=10,      # 官方 connectTimeout
    read_timeout=120,        # 官方 timeout
)

# Tushare：单个 server，上游把 token 放 URL 查询串（?token=<TOKEN>），不是请求头。
# 故 auth_query="token"：upstream 读 TUSHARE_MCP_TOKEN 拼进查询串、请求头留空（凭据不进 header/日志）。
# base_url 本身即完整端点（含结尾 /），url_template 只用 {base_url}；工具前缀 tushare_ds_。
TUSHARE = Provider(
    name="tushare",
    base_url="https://api.tushare.pro/mcp/",
    servers=(ProviderServer(name="tushare-mcp", short_name="ds"),),
    auth_env="TUSHARE_MCP_TOKEN",
    auth_query="token",      # 凭据走 URL 查询串，而非 header
    url_template="{base_url}",
    aggregate=True,          # 上游 tool-per-API 258 个,网关层聚合成 ~13 个分类工具
)

# 以后追加厂商：PROVIDERS = (IFIND, MX, TUSHARE, WIND, CHOICE, ...)
PROVIDERS: tuple[Provider, ...] = (IFIND, MX, TUSHARE)
