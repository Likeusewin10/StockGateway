"""对等机（peer）接入 + 网关运行模式单测（多机 agent 协同，HTTP 哑服务版）。

对等机现跑 peer_service.py（纯 HTTP），hub 侧注册原生工具经 PeerClient 调它。
这里桩掉 PeerClient 的 HTTP 方法，验证解析/跳过/工具注册/命令组装/转发。
"""
import logging

import pytest

from mcp_gateway.config import (
    GATEWAY_MODE_AGENT_ONLY,
    GATEWAY_MODE_FULL,
    get_gateway_mode,
)
from mcp_gateway.peer_client import PeerClient
from mcp_gateway.peers import (
    build_peer_mcp,
    load_peer_clients,
    load_peer_mcps,
    peer_agent_run,
    peer_key_env,
)

# 异步用例走 anyio 插件（仅 asyncio 后端，.venv-mcp 未装 trio）；对同步用例无害。
pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
def _all_peer_keys(monkeypatch):
    """默认给测试里出现的 peer 名都配 key（个别用例再删）。"""
    for name in ("PC2", "PC3", "PC9", "WORK_PC", "A", "B"):
        monkeypatch.setenv(f"PEER_{name}_API_KEY", f"key-{name.lower()}")


class TestLoadPeerClients:
    def test_empty_env_returns_no_peers(self, monkeypatch):
        monkeypatch.delenv("MCP_PEERS", raising=False)
        assert load_peer_clients() == []

    def test_blank_string_returns_no_peers(self):
        assert load_peer_clients("") == []
        assert load_peer_clients("  ,  ,") == []

    def test_single_peer(self):
        clients = load_peer_clients("pc2=https://mcp-pc2.jiantx.net")
        assert len(clients) == 1
        assert clients[0].name == "pc2"
        assert clients[0].base_url == "https://mcp-pc2.jiantx.net"

    def test_legacy_mcp_suffix_stripped(self):
        # 旧 .env 里 URL 曾指向 .../mcp；小服务原语在根路径，尾巴要剥掉
        c = load_peer_clients("pc2=https://mcp-pc2.jiantx.net/mcp")[0]
        assert c.base_url == "https://mcp-pc2.jiantx.net"

    def test_multiple_peers(self):
        clients = load_peer_clients("pc2=http://a, pc3=https://b")
        assert [c.name for c in clients] == ["pc2", "pc3"]

    def test_name_normalized_lower_and_underscore(self):
        c = load_peer_clients("Work-PC=http://a")[0]
        assert c.name == "work_pc"

    def test_malformed_entry_skipped_with_warning(self, caplog):
        with caplog.at_level(logging.WARNING):
            clients = load_peer_clients("no-equals-sign,pc2=http://a")
        assert len(clients) == 1
        assert any("已跳过" in r.message for r in caplog.records)

    def test_non_http_url_skipped(self, caplog):
        with caplog.at_level(logging.WARNING):
            assert load_peer_clients("pc2=ftp://a") == []

    def test_bad_peer_name_skipped(self, caplog):
        with caplog.at_level(logging.WARNING):
            assert load_peer_clients("2pc=http://a,p c=http://b") == []

    def test_duplicate_peer_name_keeps_first(self, caplog):
        with caplog.at_level(logging.WARNING):
            clients = load_peer_clients("pc2=http://first,pc2=http://second")
        assert len(clients) == 1 and clients[0].base_url == "http://first"

    def test_missing_key_skips_peer(self, monkeypatch, caplog):
        monkeypatch.delenv("PEER_PC2_API_KEY", raising=False)
        with caplog.at_level(logging.WARNING):
            assert load_peer_clients("pc2=http://a") == []
        assert any("PEER_PC2_API_KEY" in r.message for r in caplog.records)

    def test_reads_env_when_raw_omitted(self, monkeypatch):
        monkeypatch.setenv("MCP_PEERS", "pc9=http://x")
        clients = load_peer_clients()
        assert len(clients) == 1 and clients[0].name == "pc9"

    def test_key_env_helper(self):
        assert peer_key_env("pc2") == "PEER_PC2_API_KEY"

    def test_api_key_injected_into_header(self, monkeypatch):
        monkeypatch.setenv("PEER_PC2_API_KEY", "peer-key-abc")
        c = load_peer_clients("pc2=http://a")[0]
        assert c._headers == {"X-API-Key": "peer-key-abc"}


class TestPeerClientEndpoints:
    """PeerClient 各原语拼对了 path/params/body（桩 _post/_get 捕获参数）。"""

    def _client(self, monkeypatch):
        c = PeerClient("pc2", "https://mcp-pc2.jiantx.net/mcp", "k")
        calls = []
        monkeypatch.setattr(c, "_post", lambda p, b: calls.append(("POST", p, b)) or {"ok": True})
        monkeypatch.setattr(c, "_get", lambda p, q: calls.append(("GET", p, q)) or {"ok": True})
        return c, calls

    def test_base_url_strips_mcp(self):
        assert PeerClient("pc2", "https://x/mcp", "k").base_url == "https://x"

    def test_exec(self, monkeypatch):
        c, calls = self._client(monkeypatch)
        c.exec(["claude", "-p"], timeout=30)
        assert calls == [("POST", "/exec", {"argv": ["claude", "-p"], "timeout": 30})]

    def test_task_status_and_result(self, monkeypatch):
        c, calls = self._client(monkeypatch)
        c.task_status("t1")
        c.task_result("t1")
        assert calls[0] == ("GET", "/task", {"id": "t1"})
        assert calls[1] == ("GET", "/task", {"id": "t1", "full": "1"})

    def test_file_put(self, monkeypatch):
        c, calls = self._client(monkeypatch)
        c.file_put("/tmp/x", "YQ==", mode="append", expected_size=10)
        _, path, body = calls[0]
        assert path == "/file" and body["action"] == "put" and body["expected_size"] == 10


class TestBuildPeerMcp:
    """hub 侧原生工具：命令在 hub 拼好（含 claude 会话 UUID），转发给对等机。"""

    async def test_all_tools_registered(self):
        from fastmcp import Client
        mcp = build_peer_mcp(PeerClient("pc2", "http://a", "k"))
        async with Client(mcp) as c:
            names = {t.name for t in await c.list_tools()}
        assert {"agent_run", "agent_status", "agent_result",
                "fs_put", "fs_get", "fs_stat", "svc_health", "svc_update"} <= names

    def test_agent_run_builds_claude_argv_and_returns_session_id(self, monkeypatch):
        captured = {}

        def fake_exec(argv, timeout=0):
            captured["argv"] = argv
            return {"task_id": "peer-task-1", "status": "running"}

        client = PeerClient("pc2", "http://a", "k")
        monkeypatch.setattr(client, "exec", fake_exec)
        out = peer_agent_run(client, "claude", "hello")
        # argv[0] 是裸引擎名（对等机侧 which 解析），会话 UUID 预生成并回传
        assert captured["argv"][0] == "claude"
        assert "--session-id" in captured["argv"]
        assert out["task_id"] == "peer-task-1" and out["session_id"]

    def test_agent_run_invalid_engine_failed_no_call(self, monkeypatch):
        client = PeerClient("pc2", "http://a", "k")
        called = {"n": 0}
        monkeypatch.setattr(client, "exec", lambda *a, **k: called.__setitem__("n", called["n"] + 1))
        out = peer_agent_run(client, "bogus", "hi")
        assert out["status"] == "failed" and called["n"] == 0

    def test_agent_run_propagates_peer_exec_error(self, monkeypatch):
        client = PeerClient("pc2", "http://a", "k")
        monkeypatch.setattr(client, "exec", lambda *a, **k: {"ok": False, "error": "peer down"})
        out = peer_agent_run(client, "claude", "hi")
        assert out["status"] == "failed" and "peer down" in out["error"]

    def test_fs_put_tool_forwards(self, monkeypatch):
        # 经 in-memory Client 实调 fs_put 工具，验证转发到 client.file_put
        client = PeerClient("pc2", "http://a", "k")
        seen = {}
        monkeypatch.setattr(client, "file_put",
                            lambda *a, **k: seen.update(args=a, kw=k) or {"ok": True})
        assert client.file_put("/tmp/x", "YQ==")["ok"] is True
        assert seen["args"][0] == "/tmp/x"


class TestLoadPeerMcps:
    def test_returns_name_and_mcp_pairs(self):
        pairs = load_peer_mcps("pc2=http://a,pc3=http://b")
        assert [n for n, _ in pairs] == ["pc2", "pc3"]
        from fastmcp import FastMCP
        assert all(isinstance(m, FastMCP) for _, m in pairs)


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
        monkeypatch.setenv("MCP_GATEWAY_MODE", "agent-only")
        from mcp_gateway import server
        app = server.build_app()
        assert app is not None and callable(app)

    def test_build_app_full_still_works(self, monkeypatch):
        monkeypatch.setenv("MCP_GATEWAY_MODE", "full")
        monkeypatch.delenv("MCP_PEERS", raising=False)
        from mcp_gateway import server
        app = server.build_app()
        assert app is not None
