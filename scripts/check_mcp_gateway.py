"""MCP 网关连通性自检：握手 + tools/list，打印工具名清单。

用法（在 .venv-mcp 下）：
    .venv-mcp\\Scripts\\python scripts\\check_mcp_gateway.py [URL]

    URL 缺省 http://127.0.0.1:8765/mcp；API Key 从环境变量 CHECK_API_KEY 读，
    留空则不带鉴权头（仅网关未配 API_KEY 时可用）。

    示例（对等机本机自验）：
        set CHECK_API_KEY=<该机 API_KEY>
        .venv-mcp\\Scripts\\python scripts\\check_mcp_gateway.py

    示例（hub 验证对等机公网可达）：
        set CHECK_API_KEY=<对等机 API_KEY>
        .venv-mcp\\Scripts\\python scripts\\check_mcp_gateway.py http://47.76.104.225:18766/mcp

退出码：0=成功列出工具；1=连接/鉴权/协议失败（stderr 有原因）。
"""
import asyncio
import os
import sys

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport


async def main() -> int:
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765/mcp"
    key = os.environ.get("CHECK_API_KEY", "").strip()
    headers = {"X-API-Key": key} if key else {}
    transport = StreamableHttpTransport(url=url, headers=headers)
    try:
        async with Client(transport) as client:
            tools = await client.list_tools()
    except Exception as exc:  # noqa: BLE001  自检脚本：任何失败都归结为退出码 1
        print(f"[FAIL] {url} -> {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    names = sorted(t.name for t in tools)
    print(f"[OK] {url} -> {len(names)} tools")
    for name in names:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
