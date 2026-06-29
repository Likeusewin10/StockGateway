"""冒烟测试：经 MCP 协议验证 agent 命名空间下的四个记忆工具。

不走公网，直连 127.0.0.1:8765，覆盖 set / get / list / delete 完整 CRUD。
"""
import asyncio
import json
import os

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport


def _read_api_key() -> str:
    env = os.path.join(os.path.dirname(__file__), "..", ".env")
    try:
        with open(env, encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("API_KEY="):
                    return line.split("=", 1)[1].strip()
    except OSError:
        pass
    return ""


URL = "http://127.0.0.1:8765/mcp"
HOST = "smoke-test-host"


def _payload(result):
    data = getattr(result, "data", None)
    if data is not None:
        return data
    for b in getattr(result, "content", []) or []:
        txt = getattr(b, "text", None)
        if txt:
            try:
                return json.loads(txt)
            except Exception:
                return {"raw": txt}
    return {}


def _check(label: str, got: dict, **expected):
    for k, v in expected.items():
        assert got.get(k) == v, f"{label}: expected {k}={v!r}, got {got.get(k)!r}"
    print(f"  [ok] {label}")


async def main():
    headers = {"X-API-Key": _read_api_key()} if _read_api_key() else {}
    transport = StreamableHttpTransport(url=URL, headers=headers)
    async with Client(transport) as client:
        # defensively clear any leftovers from a prior partial run
        for _slug in ("lang", "theme"):
            try:
                await client.call_tool(
                    "agent_agent_memory_delete", {"host_id": HOST, "slug": _slug})
            except Exception:
                pass

        print("--- memory set ---")
        r = _payload(await client.call_tool(
            "agent_agent_memory_set",
            {"host_id": HOST, "slug": "lang", "body": "Python", "type": "project"}))
        _check("set lang=Python", r, ok=True, slug="lang", created=True)

        r = _payload(await client.call_tool(
            "agent_agent_memory_set",
            {"host_id": HOST, "slug": "theme", "body": "dark", "type": "project"}))
        _check("set theme=dark", r, ok=True, slug="theme", created=True)

        print("--- memory get ---")
        r = _payload(await client.call_tool(
            "agent_agent_memory_get", {"host_id": HOST, "slug": "lang"}))
        assert r.get("ok") is True, f"get lang: expected ok=True, got {r.get('ok')!r}"
        assert r["fact"]["body"] == "Python", \
            f"get lang: expected fact.body='Python', got {r.get('fact', {}).get('body')!r}"
        print("  [ok] get lang")

        print("--- memory list ---")
        r = _payload(await client.call_tool(
            "agent_agent_memory_list", {"host_id": HOST}))
        _check("list", r, ok=True)
        assert "lang" in r["slugs"] and "theme" in r["slugs"], \
            f"expected both slugs, got {r['slugs']}"
        print(f"  [ok] slugs={r['slugs']}")

        print("--- memory delete ---")
        r = _payload(await client.call_tool(
            "agent_agent_memory_delete", {"host_id": HOST, "slug": "theme"}))
        _check("delete theme", r, ok=True, deleted=True)

        r = _payload(await client.call_tool(
            "agent_agent_memory_list", {"host_id": HOST}))
        assert "theme" not in r["slugs"], f"theme still present after delete: {r['slugs']}"
        print("  [ok] theme removed")

        print("--- invalid host_id rejected ---")
        r = _payload(await client.call_tool(
            "agent_agent_memory_set",
            {"host_id": "../bad", "slug": "x", "body": "y", "type": "project"}))
        _check("invalid host_id", r, ok=False)

        # cleanup
        await client.call_tool("agent_agent_memory_delete", {"host_id": HOST, "slug": "lang"})
        print("\nAll memory smoke checks passed.")


asyncio.run(main())
