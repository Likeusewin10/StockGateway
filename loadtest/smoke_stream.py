"""Smoke test: the streaming agent_events feature against the local gateway.

Does not go through the public network; connects directly to 127.0.0.1:8765.
Requires the gateway running with AGENT_STREAM_JSON enabled so that agent_run
tasks buffer stream-json events that agent_events can poll incrementally.
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


async def main():
    headers = {"X-API-Key": _read_api_key()} if _read_api_key() else {}
    transport = StreamableHttpTransport(url=URL, headers=headers)
    async with Client(transport) as client:
        print("--- agent run ---")
        r = _payload(await client.call_tool(
            "agent_agent_run",
            {"engine": "claude", "prompt": "Just print the single word hello"}))
        task_id = r.get("task_id")
        print(f"  [ok] task_id={task_id}")

        print("--- poll agent_events ---")
        events = []
        cursor = 0
        status = ""
        for _ in range(40):
            r = _payload(await client.call_tool(
                "agent_agent_events", {"task_id": task_id, "cursor": cursor}))
            events.extend(r.get("events", []))
            cursor = r.get("next_cursor", cursor)
            status = r.get("status", "")
            if status in ("done", "failed", "timeout"):
                break
            await asyncio.sleep(3)

        assert len(events) >= 1, f"expected at least one event, got {len(events)}"
        print(f"  [ok] collected {len(events)} events")
        assert status == "done", f"expected status=done, got {status!r}"
        print("  [ok] status=done")
        assert cursor > 0, f"expected cursor>0, got {cursor}"
        print(f"  [ok] cursor={cursor}")

        print("\nAll stream smoke checks passed.")


if __name__ == "__main__":
    asyncio.run(main())
