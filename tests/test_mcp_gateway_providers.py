"""Provider 注册表 + 凭据注入单测。"""
import logging

import pytest

from mcp_gateway.providers import IFIND, PROVIDERS, Provider, ProviderServer


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
