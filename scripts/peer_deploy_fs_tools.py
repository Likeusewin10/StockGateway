"""[已废弃 / 历史留存] 一次性运维脚本：把 fs_tools 经 LLM 抄写推送到对等机。

⚠ 2026-07 多机架构重构后本脚本已被取代，勿再用于日常：对等机改跑「哑服务」
`peer_service.py`，业务逻辑全在 hub，加/改工具无需再往对等机推代码。需要更新哑服务
本体时用 `scripts/push_peer_service.py`（经 svc_update 确定性推送）。本文件仅作历史留存。

（原说明）经 hub 网关的 peer_<name>_agent_run 把「文件完整内容 + 落地指令」作为 prompt
丢给对等机上的 Claude 执行，轮询 peer_<name>_agent_status 至终态后取 result。

分三步（restart 拆开是因为对等机 Agent 是网关子进程，任务里直接杀网关会
丢掉自己的任务表，apply 结果就取不回来了）：

  .venv-mcp\\Scripts\\python scripts\\peer_deploy_fs_tools.py apply           # 落文件+自检(不重启)
  .venv-mcp\\Scripts\\python scripts\\peer_deploy_fs_tools.py restart         # 触发网关重启(fire&forget)
  .venv-mcp\\Scripts\\python scripts\\peer_deploy_fs_tools.py verify          # hub 侧确认 peer_*_fs_put 出现

均支持 --peer <name> 只操作某台。鉴权用 .env 的 API_KEY（hub 自己的 key，
peer 侧 key 由 hub 网关注入，本脚本不接触）。
"""
import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stocksdk.config import load_dotenv  # noqa: E402

load_dotenv()

from fastmcp import Client  # noqa: E402
from fastmcp.client.transports import StreamableHttpTransport  # noqa: E402

GATEWAY_URL = os.environ.get("HUB_GATEWAY_URL", "http://127.0.0.1:8765/mcp")
POLL_INTERVAL_SECONDS = 3
POLL_TIMEOUT_SECONDS = 420

CONFIG_BLOCK = '''# ---- 文件传输工具（fs_put/fs_get/fs_stat，见 fs_tools.py）----
# 单次 put 解码后字节上限 / 单次 get 返回字节上限。base64 膨胀 4/3，8MB 二进制
# 对应 ~10.7MB MCP 消息体；更大文件走分块（put mode=append / get offset）。
FS_PUT_MAX_BYTES = int(os.environ.get("FS_PUT_MAX_BYTES", str(8 * 1024 * 1024)))
FS_GET_MAX_BYTES = int(os.environ.get("FS_GET_MAX_BYTES", str(8 * 1024 * 1024)))'''


def peer_names() -> list[str]:
    raw = os.environ.get("MCP_PEERS", "")
    return [e.split("=")[0].strip().lower().replace("-", "_")
            for e in raw.split(",") if e.strip() and "=" in e]


def build_apply_prompt() -> str:
    fs_tools_src = (ROOT / "mcp_gateway" / "fs_tools.py").read_text(encoding="utf-8")
    agent_tools_src = (ROOT / "mcp_gateway" / "agent_tools.py").read_text(encoding="utf-8")
    lines = [
        "部署任务（来自 hub，机械执行，不要发挥）：给本机 MCP 网关（agent-only 对等机）",
        "新增文件传输工具 fs_put/fs_get/fs_stat。只改文件并自检，",
        "完成后【绝对不要重启/杀网关进程】——你自己是网关的子进程，重启由 hub 另行触发。",
        "",
        "步骤：",
        "1. git status 查看 mcp_gateway/agent_tools.py 与 mcp_gateway/config.py 有无未提交本地改动，结论写进输出。",
        "2. 用本消息底部【文件一】的完整内容覆盖写入 mcp_gateway/fs_tools.py（新文件）。",
        "3. 用底部【文件二】的完整内容覆盖写入 mcp_gateway/agent_tools.py；",
        "   ⚠ 若第 1 步发现该文件有本地未提交改动，则不要整体覆盖，改为合并增量：",
        "   加 import 行 `from mcp_gateway.fs_tools import fs_get_impl, fs_put_impl, fs_stat_impl`，",
        "   并把【文件二】末尾的 fs_put/fs_get/fs_stat 三个 @agent.tool 函数原样追加到文件末尾。",
        "4. mcp_gateway/config.py：紧跟 `AGENT_SESSION_TITLE_MAXLEN = 80` 那行之后插入以下块",
        "  （若文件里已有 FS_PUT_MAX_BYTES 则跳过此步）：",
        "```python",
        CONFIG_BLOCK,
        "```",
        "5. 自检（用本机网关 venv 的 python：Windows 是 .venv-mcp\\Scripts\\python.exe，",
        "   macOS 是 .venv-mcp/bin/python；没有 .venv-mcp 就用网关实际在用的解释器）：",
        "   a) 导入检查：python -c \"from mcp_gateway.fs_tools import fs_put_impl; print('import ok')\"",
        "   b) 工具注册检查：进程内用 fastmcp Client 连 mcp_gateway.agent_tools 的 agent 实例，",
        "      list_tools 须包含裸名 fs_get、fs_put、fs_stat 三个工具。",
        "6. 输出的最后一行必须是机器可读结论：全部成功输出 `DEPLOY_OK`，",
        "   任一步失败输出 `DEPLOY_FAIL: <一句话原因>`。",
        "",
        "=== 文件一 mcp_gateway/fs_tools.py 完整内容（含此行下方到『文件一结束』之间的全部）===",
        fs_tools_src,
        "=== 文件一结束 ===",
        "",
        "=== 文件二 mcp_gateway/agent_tools.py 完整内容 ===",
        agent_tools_src,
        "=== 文件二结束 ===",
    ]
    return "\n".join(lines)


RESTART_PROMPT = """运维任务（来自 hub）：重启本机 MCP 网关（agent-only）进程，使刚部署的 fs_put/fs_get/fs_stat 工具生效。

⚠ 你自己是网关的子进程，直接同步杀网关会中断你所在的任务。请用「延迟 + 脱离」方式：
- Windows：起一个分离进程延迟约 10 秒后杀网关（例如 `start "" cmd /c "timeout /t 10 & taskkill /F /IM uvicorn.exe"`，
  或按本机实际进程名/PID 杀跑着 mcp_gateway 的 python），看门狗 bat / 计划任务会自动拉起；
  若网关由计划任务管理，也可延迟后 schtasks /End + /Run 对应任务。
- macOS：网关由 launchd 管理且带 KeepAlive，延迟后 kill 网关进程或
  `launchctl kickstart -k gui/$(id -u)/<网关label>` 即自动拉起。
先安排好延迟重启（确认命令已发出、不阻塞），然后立即输出最后一行 `RESTART_SCHEDULED`，不要等待网关真正重启。"""

# git 拉取部署（首选通道：短 prompt，绕开 Windows cmd 8191 字符命令行上限）
PULL_PROMPT = """部署任务（来自 hub，机械执行）：仓库远端已推送文件传输工具提交（mcp_gateway/fs_tools.py 等）。请更新本机代码并自检，完成后【绝对不要重启/杀网关进程】（你是网关子进程，重启由 hub 另行触发）。

1. git status。若存在未跟踪的 mcp_gateway/fs_tools.py 或 mcp_gateway/agent_tools.py、mcp_gateway/config.py 有本地改动——那是此前经 Agent 手工落的同内容临时改动——先丢弃：删掉未跟踪的 mcp_gateway/fs_tools.py，`git checkout -- mcp_gateway/agent_tools.py mcp_gateway/config.py`。⚠ 其他文件的本地改动一律不动。
2. `git pull --ff-only origin main`（预期快进包含提交 bdb1ee5「feat(mcp-gateway): 文件传输工具」）。失败不要 merge/rebase，直接报告。
3. 自检（网关 venv 的 python：Windows .venv-mcp\\Scripts\\python.exe / macOS .venv-mcp/bin/python）：
   a) `python -c "from mcp_gateway.fs_tools import fs_put_impl; print('import ok')"`
   b) 进程内 fastmcp Client 连 mcp_gateway.agent_tools 的 agent 实例，list_tools 须含裸名 fs_get、fs_put、fs_stat。
4. 最后一行输出机器可读结论：`DEPLOY_OK` 或 `DEPLOY_FAIL: <一句话原因>`。"""


def _tool_payload(res) -> dict:
    """CallToolResult → dict（优先 structured data，退回解析 text）。"""
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
    transport = StreamableHttpTransport(GATEWAY_URL, headers={"x-api-key": key})
    return Client(transport)


async def _poll_to_result(client: Client, peer: str, task_id: str) -> dict:
    """轮询单个任务到终态并取结果；瞬时网络/502 错误重试而非放弃。"""
    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
        try:
            st = _tool_payload(await client.call_tool(
                f"peer_{peer}_agent_status", {"task_id": task_id}))
        except Exception as exc:  # noqa: BLE001  隧道瞬时 502/超时不放弃任务
            print(f"[{peer}] poll transient error, retrying: "
                  f"{str(exc)[:120]}", flush=True)
            continue
        if st.get("status") in ("done", "failed", "timeout"):
            result = _tool_payload(await client.call_tool(
                f"peer_{peer}_agent_result", {"task_id": task_id}))
            return {"peer": peer, "task_id": task_id, **result}
    return {"peer": peer, "task_id": task_id, "status": "poll_timeout"}


async def run_peer_task(client: Client, peer: str, prompt: str,
                        wait: bool = True) -> dict:
    """对单个 peer 起 agent_run 并（可选）轮询到终态，返回汇总 dict。"""
    submitted = _tool_payload(await client.call_tool(
        f"peer_{peer}_agent_run", {"engine": "claude", "prompt": prompt}))
    task_id = submitted.get("task_id", "")
    status = submitted.get("status", "")
    print(f"[{peer}] submitted task_id={task_id} status={status}", flush=True)
    if status == "failed" or not task_id:
        return {"peer": peer, "status": "failed", "error": submitted.get("error", submitted)}
    if not wait:
        return {"peer": peer, "status": status, "task_id": task_id}
    return await _poll_to_result(client, peer, task_id)


def summarize(res: dict) -> None:
    peer = res.get("peer")
    status = res.get("status")
    output = str(res.get("output", ""))
    # claude 的 output 是 JSON 信封，取 result 字段更可读
    try:
        envelope = json.loads(output)
        if isinstance(envelope, dict) and "result" in envelope:
            output = str(envelope["result"])
    except (ValueError, TypeError):
        pass
    tail = output[-1500:] if output else ""
    print(f"\n===== [{peer}] status={status} =====")
    if res.get("error"):
        print(f"error: {str(res['error'])[:800]}")
    if tail:
        print(tail)
    verdict = ("DEPLOY_OK" in output and "DEPLOY_FAIL" not in output) or \
              ("RESTART_SCHEDULED" in output)
    print(f"----- [{peer}] verdict: {'PASS' if verdict else 'CHECK MANUALLY'} -----", flush=True)


async def cmd_apply(peers: list[str]) -> None:
    prompt = build_apply_prompt()
    print(f"apply prompt: {len(prompt)} chars -> peers {peers}", flush=True)
    async with _client() as client:
        results = await asyncio.gather(
            *(run_peer_task(client, p, prompt) for p in peers))
    for res in results:
        summarize(res)


async def cmd_restart(peers: list[str]) -> None:
    # fire-and-forget：重启会杀掉 agent 自己所在的网关，任务表随之清空，
    # 无法轮询到终态。只提交、确认已受理（返回 task_id / RESTART_SCHEDULED），不等待。
    async with _client() as client:
        for p in peers:
            res = await run_peer_task(client, p, RESTART_PROMPT, wait=False)
            print(f"[{p}] restart submitted: {res.get('status')} "
                  f"task_id={res.get('task_id', '')}", flush=True)


async def cmd_pull(peers: list[str]) -> None:
    print(f"pull prompt: {len(PULL_PROMPT)} chars -> peers {peers}", flush=True)
    async with _client() as client:
        results = await asyncio.gather(
            *(run_peer_task(client, p, PULL_PROMPT) for p in peers))
    for res in results:
        summarize(res)


async def cmd_verify(peers: list[str]) -> None:
    async with _client() as client:
        tools = {t.name for t in await client.list_tools()}
    for p in peers:
        expect = [f"peer_{p}_fs_put", f"peer_{p}_fs_get", f"peer_{p}_fs_stat"]
        present = [n for n in expect if n in tools]
        missing = [n for n in expect if n not in tools]
        mark = "OK" if not missing else f"MISSING {missing}"
        print(f"[{p}] {mark} (present: {present})")


async def cmd_poll(peers: list[str], task_id: str) -> None:
    """续接轮询一个已提交的任务（apply 中断后恢复用），--peer 必填。"""
    if len(peers) != 1:
        sys.exit("poll 需要 --peer 指定单台")
    async with _client() as client:
        summarize(await _poll_to_result(client, peers[0], task_id))


async def cmd_run(peers: list[str], prompt_file: str) -> None:
    """把任意 prompt 文件发给 peer 执行并轮询到终态（通用运维通道）。"""
    prompt = Path(prompt_file).read_text(encoding="utf-8")
    print(f"run prompt: {len(prompt)} chars -> peers {peers}", flush=True)
    async with _client() as client:
        results = await asyncio.gather(
            *(run_peer_task(client, p, prompt) for p in peers))
    for res in results:
        summarize(res)


# ---- chunkpush：Windows peer 专用推送协议 ----
# 背景（pc2 实测踩坑）：Windows 上 claude 是 .CMD shim，agent_run 的 prompt 经
# cmd.exe 解析 —— ① 命令行总长 8191 字符上限；② prompt 在第一个换行处被截断。
# 故所有消息必须「单行 + 短」。文件内容 base64 后按 ~5500 字符分块逐条追加到
# peer 的 deploy_tmp/*.b64，最后一条消息给出各文件解码后的 sha256 让 peer 侧
# 校验后落盘（字节级保证），再自检工具注册。
_CHUNK_B64_CHARS = 5500


def _oneline(s: str) -> str:
    return " ".join(s.split())


async def cmd_chunkpush(peers: list[str]) -> None:
    import base64
    import hashlib
    payloads: dict[str, bytes] = {
        "fs_tools.b64": (ROOT / "mcp_gateway" / "fs_tools.py").read_bytes(),
        "agent_tools.b64": (ROOT / "mcp_gateway" / "agent_tools.py").read_bytes(),
        "config_block.b64": CONFIG_BLOCK.encode("utf-8"),
    }
    shas = {n: hashlib.sha256(raw).hexdigest() for n, raw in payloads.items()}
    async with _client() as client:
        for peer in peers:
            print(f"\n### chunkpush -> {peer}", flush=True)
            init = _oneline("""部署准备（来自 hub，机械执行，本条及后续消息均为单行）：
                在仓库根创建目录 deploy_tmp（已存在则清空其中 *.b64）。
                后续多条消息会发 base64 分块让你追加成文件。完成本步后最后一行输出 READY""")
            res = await run_peer_task(client, peer, init)
            if "READY" not in str(res.get("output", "")):
                summarize(res)
                print(f"[{peer}] init 未确认 READY，中止该 peer", flush=True)
                continue
            ok = True
            for name, raw in payloads.items():
                b64 = base64.b64encode(raw).decode("ascii")
                chunks = [b64[i:i + _CHUNK_B64_CHARS]
                          for i in range(0, len(b64), _CHUNK_B64_CHARS)]
                for idx, chunk in enumerate(chunks, 1):
                    prompt = _oneline(f"""机械执行勿发挥：把本消息末尾反引号内的 base64
                        片段原样追加到仓库根 deploy_tmp/{name} 文件末尾（文件不存在则创建），
                        不得添加任何换行或空白，建议用 python 的 open(path,'a') 直接 write。
                        完成后最后一行输出 APPENDED {name} {idx}/{len(chunks)}。""") + f" `{chunk}`"
                    res = await run_peer_task(client, peer, prompt)
                    out = str(res.get("output", ""))
                    if f"APPENDED {name} {idx}/{len(chunks)}" not in out:
                        summarize(res)
                        print(f"[{peer}] {name} 第 {idx} 块未确认，中止该 peer", flush=True)
                        ok = False
                        break
                    print(f"[{peer}] {name} {idx}/{len(chunks)} ok", flush=True)
                if not ok:
                    break
            if not ok:
                continue
            finalize = _oneline(f"""最终落地（机械执行）：仓库根 deploy_tmp 下有三个单行
                base64 文件。逐个 base64 解码为字节并校验 sha256：
                fs_tools.b64 解码后 sha256 须为 {shas['fs_tools.b64']}，二进制写入（覆盖）mcp_gateway/fs_tools.py；
                agent_tools.b64 解码后 sha256 须为 {shas['agent_tools.b64']}，二进制写入（覆盖）mcp_gateway/agent_tools.py；
                config_block.b64 解码后 sha256 须为 {shas['config_block.b64']}，解码内容是一段 python 常量文本：
                若 mcp_gateway/config.py 中没有 FS_PUT_MAX_BYTES，就把这段文本（前后各留一个空行）插入到
                「AGENT_SESSION_TITLE_MAXLEN = 80」那一行之后，已有则跳过。
                任一 sha256 不匹配立即停止并输出 DEPLOY_FAIL: sha256 mismatch <文件名>。
                全部落盘后自检：.venv-mcp 的 python 执行 from mcp_gateway.fs_tools import fs_put_impl，
                并进程内用 fastmcp Client 连 mcp_gateway.agent_tools 的 agent 实例确认 list_tools
                含裸名 fs_get、fs_put、fs_stat；然后删除 deploy_tmp 目录。
                绝对不要重启或杀网关进程。最后一行输出 DEPLOY_OK 或 DEPLOY_FAIL: 原因""")
            summarize(await run_peer_task(client, peer, finalize))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",
                        choices=["apply", "pull", "restart", "verify", "poll", "run",
                                 "chunkpush"])
    parser.add_argument("--peer", help="只操作指定 peer（默认全部）")
    parser.add_argument("--task-id", help="poll 用：要续接轮询的 task_id")
    parser.add_argument("--prompt-file", help="run 用：要发给 peer 的 prompt 文件路径")
    args = parser.parse_args()
    peers = peer_names()
    if args.peer:
        target = args.peer.strip().lower().replace("-", "_")
        if target not in peers:
            sys.exit(f"peer {target!r} 不在 MCP_PEERS 中：{peers}")
        peers = [target]
    if not peers:
        sys.exit("MCP_PEERS 为空，无 peer 可操作")
    if args.command == "poll":
        if not args.task_id:
            sys.exit("poll 需要 --task-id")
        asyncio.run(cmd_poll(peers, args.task_id))
        return
    if args.command == "run":
        if not args.prompt_file:
            sys.exit("run 需要 --prompt-file")
        asyncio.run(cmd_run(peers, args.prompt_file))
        return
    asyncio.run({"apply": cmd_apply, "pull": cmd_pull, "restart": cmd_restart,
                 "verify": cmd_verify, "chunkpush": cmd_chunkpush}[args.command](peers))


if __name__ == "__main__":
    main()
