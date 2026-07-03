"""Provider 注册表 + 凭据注入单测。"""
import logging

import pytest

from mcp_gateway.providers import IFIND, MX, PROVIDERS, Provider, ProviderServer, TUSHARE


class TestRegistry:
    def test_ifind_has_seven_servers(self):
        assert len(IFIND.servers) == 7

    def test_ifind_is_registered(self):
        assert IFIND in PROVIDERS

    def test_server_url_concatenation(self):
        stock = next(s for s in IFIND.servers if s.short_name == "stock")
        # Arrange/Act
        url = IFIND.server_url(stock)
        # Assert
        assert url == (
            "https://api-mcp.51ifind.com:8643/ds-mcp-servers/hexin-ifind-ds-stock-mcp"
        )

    def test_prefix_namespacing(self):
        stock = next(s for s in IFIND.servers if s.short_name == "stock")
        assert IFIND.prefix(stock) == "ifind_stock"

    def test_hyphen_in_short_name_becomes_underscore(self):
        gstock = next(s for s in IFIND.servers if "global" in s.short_name)
        assert gstock.short_name == "global_stock"
        assert IFIND.prefix(gstock) == "ifind_global_stock"

    def test_provider_names_unique(self):
        names = [p.name for p in PROVIDERS]
        assert len(names) == len(set(names))


class TestMxProvider:
    """妙想（东方财富 MX）：URL 结构与鉴权头都与 iFinD 不同，单独固化。"""

    def test_mx_is_registered(self):
        assert MX in PROVIDERS

    def test_mx_has_single_server(self):
        assert len(MX.servers) == 1

    def test_server_url_is_single_endpoint(self):
        # 妙想上游是单一完整地址，base_url 本身即终点，不追加 /{server}
        url = MX.server_url(MX.servers[0])
        assert url == "https://mxapi.eastmoney.com/mxds/mcp"

    def test_prefix_namespacing(self):
        assert MX.prefix(MX.servers[0]) == "mx_ds"

    def test_mx_has_timeouts(self):
        assert MX.connect_timeout == 10
        assert MX.read_timeout == 120

    def test_auth_uses_em_api_key_header(self, monkeypatch):
        from mcp_gateway.upstream import _auth_headers

        monkeypatch.setenv("MIAO_XIANG_MCP_KEY", "mx-key-123")
        headers = _auth_headers(MX)
        # 裸 key 注入到 em_api_key 头，而非 Authorization；读的是 MIAO_XIANG_MCP_KEY
        assert headers == {"em_api_key": "mx-key-123"}


class TestTushareProvider:
    """Tushare：凭据走 URL 查询串（?token=），不是 header。单独固化这条差异。"""

    def test_tushare_is_registered(self):
        assert TUSHARE in PROVIDERS

    def test_tushare_has_single_server(self):
        assert len(TUSHARE.servers) == 1

    def test_server_url_is_single_endpoint(self):
        # base_url 本身即完整端点（含结尾 /），不追加 /{server}
        url = TUSHARE.server_url(TUSHARE.servers[0])
        assert url == "https://api.tushare.pro/mcp/"

    def test_prefix_namespacing(self):
        assert TUSHARE.prefix(TUSHARE.servers[0]) == "tushare_ds"

    def test_auth_query_field_set(self):
        assert TUSHARE.auth_query == "token"

    def test_auth_headers_empty_for_query_auth(self, monkeypatch):
        # query 鉴权厂商：凭据不进 header，_auth_headers 返回 {}
        from mcp_gateway.upstream import _auth_headers

        monkeypatch.setenv("TUSHARE_MCP_TOKEN", "tok-abc")
        assert _auth_headers(TUSHARE) == {}

    def test_auth_headers_none_when_token_missing(self, monkeypatch, caplog):
        # 缺 token 仍走跳过逻辑（返回 None + warning），与 header 路径对称
        from mcp_gateway.upstream import _auth_headers

        monkeypatch.delenv("TUSHARE_MCP_TOKEN", raising=False)
        with caplog.at_level(logging.WARNING):
            assert _auth_headers(TUSHARE) is None
        assert any("TUSHARE_MCP_TOKEN" in r.message for r in caplog.records)

    def test_server_url_appends_token_query(self, monkeypatch):
        from mcp_gateway.upstream import _server_url

        monkeypatch.setenv("TUSHARE_MCP_TOKEN", "tok-abc")
        url = _server_url(TUSHARE, TUSHARE.servers[0])
        assert url == "https://api.tushare.pro/mcp/?token=tok-abc"

    def test_server_url_none_when_token_missing(self, monkeypatch):
        from mcp_gateway.upstream import _server_url

        monkeypatch.delenv("TUSHARE_MCP_TOKEN", raising=False)
        assert _server_url(TUSHARE, TUSHARE.servers[0]) is None

    def test_client_url_carries_token(self, monkeypatch):
        from mcp_gateway.upstream import make_server_client

        monkeypatch.setenv("TUSHARE_MCP_TOKEN", "tok-abc")
        client = make_server_client(TUSHARE, TUSHARE.servers[0], {})
        assert "token=tok-abc" in client.transport.url

    def test_token_not_in_provider_repr(self):
        # 注册表只含环境变量名，不含 token 本身
        assert "TUSHARE_MCP_TOKEN" in repr(TUSHARE)
        assert "55e2d5be" not in repr(TUSHARE)


class TestCredentialInjection:
    def test_headers_inject_credential(self, monkeypatch):
        from mcp_gateway.upstream import _auth_headers

        monkeypatch.setenv("IFIND_MCP_JWT", "secret-token-xyz")
        headers = _auth_headers(IFIND)
        assert headers == {"Authorization": "secret-token-xyz"}

    def test_auth_scheme_prefix_applied(self, monkeypatch):
        from mcp_gateway.upstream import _auth_headers

        bearer_provider = Provider(
            name="demo",
            base_url="https://x",
            servers=(ProviderServer("demo-mcp", "demo"),),
            auth_env="DEMO_TOKEN",
            auth_scheme="Bearer ",
        )
        monkeypatch.setenv("DEMO_TOKEN", "abc")
        headers = _auth_headers(bearer_provider)
        assert headers == {"Authorization": "Bearer abc"}

    def test_missing_credential_returns_none_and_warns(self, monkeypatch, caplog):
        from mcp_gateway.upstream import _auth_headers

        monkeypatch.delenv("IFIND_MCP_JWT", raising=False)
        with caplog.at_level(logging.WARNING):
            headers = _auth_headers(IFIND)
        assert headers is None
        assert any("IFIND_MCP_JWT" in r.message for r in caplog.records)

    def test_credential_not_in_provider_repr(self):
        # 注册表里只有环境变量名，不含凭据本身
        assert "IFIND_MCP_JWT" in repr(IFIND)
        assert "secret" not in repr(IFIND).lower()


class TestTimeoutInjection:
    """超时只对配了 connect/read_timeout 的 provider 注入 httpx_client_factory。"""

    def test_ifind_has_no_timeout(self):
        # iFinD 未配超时，回归保护：字段为 None
        assert IFIND.connect_timeout is None
        assert IFIND.read_timeout is None

    def test_factory_none_when_no_timeout(self):
        from mcp_gateway.upstream import _timeout_factory

        assert _timeout_factory(IFIND) is None

    def test_factory_builds_httpx_timeout_for_mx(self):
        import httpx

        from mcp_gateway.upstream import _timeout_factory

        factory = _timeout_factory(MX)
        assert factory is not None
        client = factory(headers={"em_api_key": "k"})
        assert isinstance(client, httpx.AsyncClient)
        assert client.timeout.connect == 10
        assert client.timeout.read == 120

    def test_factory_accepts_fastmcp_extra_kwargs(self):
        # 回归：fastmcp 的 http.py 调工厂时会多传 follow_redirects（及未来可能的其它 kwargs）。
        # 工厂必须用 **kwargs 吞掉，否则上游 client 连接即抛 TypeError、列空工具。
        import httpx

        from mcp_gateway.upstream import _timeout_factory

        factory = _timeout_factory(MX)
        client = factory(
            headers={"em_api_key": "k"},
            timeout=httpx.Timeout(5),  # 传入的 timeout 应被忽略，强制用 provider 配置
            auth=None,
            follow_redirects=True,
        )
        assert isinstance(client, httpx.AsyncClient)
        assert client.timeout.connect == 10  # provider 配置生效，非传入的 5
        assert client.follow_redirects is True

    def test_mx_client_injects_factory(self, monkeypatch):
        from mcp_gateway.upstream import make_server_client

        client = make_server_client(MX, MX.servers[0], {"em_api_key": "k"})
        # transport 应带上非默认 httpx_client_factory
        factory = getattr(client.transport, "httpx_client_factory", None)
        assert factory is not None

    def test_ifind_client_no_factory_override(self):
        from mcp_gateway.upstream import make_server_client

        stock = next(s for s in IFIND.servers if s.short_name == "stock")
        client = make_server_client(IFIND, stock, {"Authorization": "t"})
        # 未配超时则不显式注入；transport 走默认工厂
        factory = getattr(client.transport, "httpx_client_factory", None)
        # 默认值为 mcp 的 create_mcp_http_client，不是我们的闭包(名为 'factory')
        assert factory is None or getattr(factory, "__name__", "") != "factory"
