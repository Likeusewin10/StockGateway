"""把本机（hub）最新的 peer_service.py 推给全部对等机自更新（svc_update 通道）。

新架构下对等机的业务逻辑全在 hub，日常无需同步代码。**唯一**需要动对等机的场景 =
改了 peer_service.py 本体（哑服务的原语）。这时经 hub 网关的 peer_<name>_svc_update
把新源码推过去，对等机 py_compile 自检通过后原子替换 + 延迟重启 —— 确定性、不经
git、不经 LLM 抄写。

    .venv-mcp\\Scripts\\python scripts\\push_peer_service.py            # 推给全部 peer
    .venv-mcp\\Scripts\\python scripts\\push_peer_service.py --peer pc2  # 只推一台

鉴权用 .env 的 API_KEY（hub 自己的 key）；peer 侧 key 由 hub 网关注入,本脚本不接触。
peer_service.py 约十几 KB,单次 svc_update 即可(base64 后仍远低于请求上限)。
"""
import argparse
import asyncio
import base64
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stocksdk.config import load_dotenv  # noqa: E402

load_dotenv()

from fastmcp import Client  # noqa: E402
from fastmcp.client.transports import StreamableHttpTransport  # noqa: E402

GATEWAY_URL = os.environ.get("HUB_GATEWAY_URL", "http://127.0.0.1:8765/mcp")


def peer_names() -> list[str]:
    raw = os.environ.get("MCP_PEERS", "")
    return [e.split("=")[0].strip().lower().replace("-", "_")
            for e in raw.split(",") if e.strip() and "=" in e]


def _payload(res) -> dict:
    data = getattr(res, "data", None)
    if isinstance(data, dict):
        return data
    for block in getattr(res, "content", []) or []:
        text = getattr(block, "text", None)
        if text:
            try:
                return json.loads(text)
            except (ValueError, TypeError):
                return {"raw": text}
    return {}


def _client() -> Client:
    key = os.environ.get("API_KEY", "").strip()
    return Client(StreamableHttpTransport(GATEWAY_URL, headers={"x-api-key": key}))


async def push(peers: list[str]) -> None:
    source_b64 = base64.b64encode(
        (ROOT / "peer_service.py").read_bytes()).decode("ascii")
    print(f"peer_service.py -> {len(source_b64)} b64 chars, peers {peers}", flush=True)
    async with _client() as client:
        for p in peers:
            res = _payload(await client.call_tool(
                f"peer_{p}_svc_update", {"source_b64": source_b64}))
            ok = res.get("ok")
            print(f"[{p}] {'OK' if ok else 'FAIL'}: {json.dumps(res, ensure_ascii=False)[:300]}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--peer", help="只推指定 peer（默认全部）")
    args = parser.parse_args()
    peers = peer_names()
    if args.peer:
        target = args.peer.strip().lower().replace("-", "_")
        if target not in peers:
            sys.exit(f"peer {target!r} 不在 MCP_PEERS 中：{peers}")
        peers = [target]
    if not peers:
        sys.exit("MCP_PEERS 为空，无 peer 可推")
    asyncio.run(push(peers))


if __name__ == "__main__":
    main()
