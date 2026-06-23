"""服务器本机冒烟:经 MCP 协议调 agent_run claude → 轮询 → 取结果。

不走公网,直连 127.0.0.1:8765,验证「网关 + claude 子进程」整条链路。
"""
import asyncio
import json
import os
import time

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

def _read_api_key() -> str:
    """从 .env 读 API_KEY(避免依赖临时文件/shell 路径差异)。"""
    with open(os.path.join(os.path.dirname(__file__), "..", ".env"), encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


API_KEY = _read_api_key()
URL = "http://127.0.0.1:8765/mcp"
PROMPT = "用一句话说明你现在所在的工作目录是什么,并列出该目录下的前3个文件名。"


def _payload(result):
    """从 CallToolResult 取出工具返回的 dict(结构化输出优先,回退文本 JSON)。"""
    data = getattr(result, "data", None)
    if data is not None:
        return data
    sc = getattr(result, "structured_content", None)
    if sc:
        return sc
    blocks = getattr(result, "content", []) or []
    for b in blocks:
        txt = getattr(b, "text", None)
        if txt:
            try:
                return json.loads(txt)
            except Exception:
                return {"raw": txt}
    return {}


async def main():
    transport = StreamableHttpTransport(url=URL, headers={"X-API-Key": API_KEY})
    async with Client(transport) as client:
        tools = await client.list_tools()
        names = [t.name for t in tools]
        print("可见工具:", names)

        print("\n--- agent_run claude ---")
        run = await client.call_tool("agent_agent_run", {"engine": "claude", "prompt": PROMPT})
        run_data = _payload(run)
        print("run 返回:", run_data)
        task_id = run_data.get("task_id")
        assert task_id, "没拿到 task_id"

        print("\n--- 轮询 agent_status ---")
        deadline = time.time() + 180
        status = "running"
        while time.time() < deadline:
            st = _payload(await client.call_tool("agent_agent_status", {"task_id": task_id}))
            status = st.get("status")
            print(f"  [{int(time.time()%1000):>3}s] status={status}", st.get("error", ""))
            if status in ("done", "failed", "timeout", "unknown"):
                break
            await asyncio.sleep(3)

        print("\n--- agent_result ---")
        res = _payload(await client.call_tool("agent_agent_result", {"task_id": task_id}))
        print("status   :", res.get("status"))
        print("returncode:", res.get("returncode"))
        print("error    :", (res.get("error") or "")[:300])
        print("output   :\n", (res.get("output") or "")[:2000])


asyncio.run(main())
