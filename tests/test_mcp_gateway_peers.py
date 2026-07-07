"""对等机（peer）注册 + 网关运行模式单测（多机 agent 协同）。"""
import logging

from mcp_gateway.config import (
    GATEWAY_MODE_AGENT_ONLY,
    GATEWAY_MODE_FULL,
    get_gateway_mode,
)
from mcp_gateway.peers import (
    PEER_CONNECT_TIMEOUT_SECONDS,
    PEER_READ_TIMEOUT_SECONDS,
    load_peers,
    peer_key_env,
)


class TestLoadPeers:
    def test_empty_env_returns_no_peers(self, monkeypatch):
        monkeypatch.delenv("MCP_PEERS", raising=False)
        assert load_peers() == ()

    def test_blank_string_returns_no_peers(self):
        assert load_peers("") == ()
        assert load_peers("  ,  ,") == ()

    def test_single_peer(self):
        peers = load_peers("pc2=https://mcp-pc2.jiantx.net/mcp")
        assert len(peers) == 1
        p = peers[0]
        assert p.base_url == "https://mcp-pc2.jiantx.net/mcp"
        assert p.auth_env == "PEER_PC2_API_KEY"
        assert p.auth_header == "X-API-Key"

    def test_multiple_peers(self):
        peers = load_peers("pc2=http://a/mcp, pc3=https://b/mcp")
        assert [p.servers[0].short_name for p in peers] == ["pc2", "pc3"]

    def test_prefix_is_peer_name(self):
        # hub 挂载后工具名 = peer_pc2_agent_run（对等机 agent-only 模式工具为裸名）
        p = load_peers("pc2=http://a/mcp")[0]
        assert p.prefix(p.servers[0]) == "peer_pc2"

    def test_server_url_is_base_url_verbatim(self):
        # url_template 只用 {base_url}，不追加 /{server}
        p = load_peers("pc2=http://a:18766/mcp")[0]
        assert p.server_url(p.servers[0]) == "http://a:18766/mcp"

    def test_name_normalized_lower_and_underscore(self):
        p = load_peers("Work-PC=http://a/mcp")[0]
        assert p.servers[0].short_name == "work_pc"
        assert p.auth_env == "PEER_WORK_PC_API_KEY"

    def test_malformed_entry_skipped_with_warning(self, caplog):
        with caplog.at_level(logging.WARNING):
            peers = load_peers("no-equals-sign,pc2=http://a/mcp")
        assert len(peers) == 1
        assert any("已跳过" in r.message for r in caplog.records)

    def test_non_http_url_skipped(self, caplog):
        with caplog.at_level(logging.WARNING):
            peers = load_peers("pc2=ftp://a/mcp")
        assert peers == ()

    def test_bad_peer_name_skipped(self, caplog):
        # 数字开头 / 含非法字符的 peer 名不能做工具前缀
        with caplog.at_level(logging.WARNING):
            peers = load_peers("2pc=http://a/mcp,p c=http://b/mcp")
        assert peers == ()

    def test_duplicate_peer_name_keeps_first(self, caplog):
        with caplog.at_level(logging.WARNING):
            peers = load_peers("pc2=http://first/mcp,pc2=http://second/mcp")
        assert len(peers) == 1
        assert peers[0].base_url == "http://first/mcp"

    def test_short_connect_timeout_set(self):
        # 🔴 peer 宕机不能拖死 hub 的 tools/list：connect 超时必须短
        p = load_peers("pc2=http://a/mcp")[0]
        assert p.connect_timeout == PEER_CONNECT_TIMEOUT_SECONDS == 5
        assert p.read_timeout == PEER_READ_TIMEOUT_SECONDS

    def test_reads_env_when_raw_omitted(self, monkeypatch):
        monkeypatch.setenv("MCP_PEERS", "pc9=http://x/mcp")
        peers = load_peers()
        assert len(peers) == 1
        assert peers[0].servers[0].short_name == "pc9"


class TestPeerCredentialInjection:
    """peers 复用 upstream 凭据收口：X-API-Key 注入 / 缺 key 整个 peer 跳过。"""

    def test_api_key_injected_into_x_api_key_header(self, monkeypatch):
        from mcp_gateway.upstream import _auth_headers

        monkeypatch.setenv("PEER_PC2_API_KEY", "peer-key-abc")
        p = load_peers("pc2=http://a/mcp")[0]
        assert _auth_headers(p) == {"X-API-Key": "peer-key-abc"}

    def test_missing_key_skips_peer(self, monkeypatch, caplog):
        from mcp_gateway.upstream import iter_upstreams

        monkeypatch.delenv("PEER_PC2_API_KEY", raising=False)
        p = load_peers("pc2=http://a/mcp")[0]
        with caplog.at_level(logging.WARNING):
            assert list(iter_upstreams(p)) == []
        assert any("PEER_PC2_API_KEY" in r.message for r in caplog.records)

    def test_key_env_helper(self):
        assert peer_key_env("pc2") == "PEER_PC2_API_KEY"


class TestGatewayMode:
    def test_default_is_full(self, monkeypatch):
        monkeypatch.delenv("MCP_GATEWAY_MODE", raising=False)
        assert get_gateway_mode() == GATEWAY_MODE_FULL

    def test_agent_only_variants(self, monkeypatch):
        for raw in ("agent-only", "AGENT-ONLY", "agent_only", "agentonly", " agent-only "):
            monkeypatch.setenv("MCP_GATEWAY_MODE", raw)
            assert get_gateway_mode() == GATEWAY_MODE_AGENT_ONLY

    def test_unknown_value_falls_back_to_full(self, monkeypatch):
        monkeypatch.setenv("MCP_GATEWAY_MODE", "banana")
        assert get_gateway_mode() == GATEWAY_MODE_FULL


class TestAgentOnlyApp:
    def test_build_app_agent_only_returns_asgi_app(self, monkeypatch):
        # agent-only 模式：app 可构建且不触发任何厂商上游挂载
        monkeypatch.setenv("MCP_GATEWAY_MODE", "agent-only")
        from mcp_gateway import server

        app = server.build_app()
        assert app is not None
        assert callable(app)  # ASGI 应用

    def test_build_app_full_still_works(self, monkeypatch):
        monkeypatch.setenv("MCP_GATEWAY_MODE", "full")
        monkeypatch.delenv("MCP_PEERS", raising=False)
        from mcp_gateway import server

        app = server.build_app()
        assert app is not None
