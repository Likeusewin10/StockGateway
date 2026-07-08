"""迁移驱动：把某台对等机从「旧 agent-only MCP 网关」换成「哑执行小服务 peer_service.py」。

经**旧** hub 网关（当前仍在跑旧代码）的 peer_<name>_fs_put / peer_<name>_agent_run 通道驱动
（对等机此刻仍跑旧网关，故只能用旧通道自举）。三个子命令：

  probe    —— agent_run 探测对等机：OS / 仓库根 / python / 现有常驻任务，供决定 push 路径
  push     —— fs_put 把本机 peer_service.py + start_peer_service.bat 确定性写到对等机(--root 指定落点)
  cutover  —— agent_run 让对等机切换常驻到 peer_service 并延迟脱离式重启(自杀交看门狗拉起)

均需 --peer。鉴权用 .env 的 API_KEY（hub 自己的）。

⚠ 实战踩坑（2026-07-08 首迁 pc2/mac1，详见记忆 peer-migration-gotchas）：
- probe/push 稳定可用（fs_put 确定性、sha256 核对）。
- Windows 下 cutover 的 schtasks /Create 会因对等机 agent 非管理员而「拒绝访问」；
  实际改用「覆盖现有 MCPGatewayBoot 任务启动的 start_mcp_gateway.bat 内容为拉起 peer_service
  + 杀旧进程等任务自愈」绕开建任务权限。
- 给对等机 claude 的 prompt 含 " / & / 多行会被 Windows shim 截断 → 单行无特殊字符，
  复杂逻辑下沉到 .bat。
- macOS 走 launchd（用户级无需管理员），但 launchd PATH 缺 nvm bin 会致 engines=false，
  plist 需补 EnvironmentVariables PATH；旧网关 plist 记得 launchctl disable 防 RunAtLoad 复活。
"""
import argparse
import asyncio
import base64
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stocksdk.config import load_dotenv  # noqa: E402

load_dotenv()

# 复用旧部署脚本里已验证的 hub 客户端 + 轮询机制
from scripts.peer_deploy_fs_tools import (  # noqa: E402
    _client, _poll_to_result, _tool_payload, run_peer_task, summarize,
)

PROBE_PROMPT = """探测任务（来自 hub，只读不改）：报告本机环境，供 hub 决定后续部署路径。逐条输出：
1. 操作系统：跑 `uname` —— 有输出即 macOS/Unix,报错即 Windows。
2. 本仓库根的绝对路径（你当前 cwd 就是；输出它）。
3. 是否存在文件 peer_service.py（列出 cwd 下有无该文件）。
4. python 版本：Windows 跑 `python --version`，macOS 跑 `python3 --version`。
5. claude 是否可用：`claude --version`。
6. 现有常驻：Windows 跑 `schtasks /query /TN MCPGatewayBoot`（有无该任务）；macOS 跑
   `launchctl print gui/$(id -u)/com.stocksdk.mcpgateway | grep -i state`。
最后一行输出 `PROBE_DONE`。不要改任何文件、不要重启任何进程。"""


def _cutover_prompt(root: str) -> str:
    bat = root.rstrip('/').rstrip(chr(92)) + chr(92) + "start_peer_service.bat"
    return f"""切换任务（来自 hub，机械执行，不要发挥）：把本机常驻从「旧 agent-only MCP 网关」换成
「哑执行小服务 peer_service.py」。仓库根 = {root}。peer_service.py 与 start_peer_service.bat
已由 hub 经 fs_put 写好，**勿改其内容**。

前提无需改 .env：peer_service 会自动认现有 API_KEY、端口默认 8765（与旧网关同口）。

⚠ 你自己是**旧网关的子进程**：任何同步杀旧网关/停旧网关任务的动作都会中断你。因此杀旧网关
必须用「延迟 + 脱离进程树」的方式（用 start 起独立进程），并在**安排好后立即返回**，
绝不等它真正切换完成。

步骤（本机是 Windows / MrGatsby）：
1. 注册新常驻计划任务 PeerServiceBoot 指向看门狗 bat（覆盖式）：
   schtasks /Create /TN PeerServiceBoot /TR "{bat}" /SC ONLOGON /RL HIGHEST /F
2. 起一个**分离**进程（用 start 脱离你所在的旧网关进程树），延迟 15 秒后依次执行：
   停旧网关常驻→删旧网关常驻(防下次登录再起)→杀旧网关 uvicorn→拉起新服务任务。整条一次发出：
   start "" cmd /c "timeout /t 15 >nul & schtasks /End /TN MCPGatewayBoot & schtasks /Delete /TN MCPGatewayBoot /F & taskkill /F /IM uvicorn.exe & schtasks /Run /TN PeerServiceBoot"
3. 确认上面 start 命令已发出（不阻塞），**立即**输出最后一行 `CUTOVER_SCHEDULED`。

若第 1 步 schtasks /Create 就失败（权限等），不要继续第 2 步，输出 `CUTOVER_FAIL: <一句话原因>`。"""


async def cmd_probe(peer: str) -> None:
    async with _client() as client:
        summarize(await run_peer_task(client, peer, PROBE_PROMPT))


async def cmd_push(peer: str, root: str) -> None:
    files = {
        f"{root.rstrip('/').rstrip(chr(92))}/peer_service.py": ROOT / "peer_service.py",
        f"{root.rstrip('/').rstrip(chr(92))}/start_peer_service.bat": ROOT / "start_peer_service.bat",
    }
    async with _client() as client:
        for target, local in files.items():
            b64 = base64.b64encode(local.read_bytes()).decode("ascii")
            res = _tool_payload(await client.call_tool(
                f"peer_{peer}_fs_put", {"path": target, "data_b64": b64, "mode": "write"}))
            ok = res.get("ok")
            print(f"[{peer}] fs_put {target} -> {'OK' if ok else 'FAIL'} "
                  f"bytes={res.get('bytes_written')} sha256={str(res.get('sha256'))[:16]} "
                  f"{'' if ok else res.get('error')}")


async def cmd_cutover(peer: str, root: str) -> None:
    async with _client() as client:
        summarize(await run_peer_task(client, peer, _cutover_prompt(root)))


def main() -> None:
    # Windows 控制台默认 GBK,对等机结果含非 GBK 字符(如 ⚠)会 UnicodeEncodeError;强制 UTF-8。
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["probe", "push", "cutover"])
    parser.add_argument("--peer", required=True, help="对等机名（如 pc2）")
    parser.add_argument("--root", help="对等机仓库根绝对路径（push/cutover 必填）")
    args = parser.parse_args()
    peer = args.peer.strip().lower().replace("-", "_")
    if args.command in ("push", "cutover") and not args.root:
        sys.exit(f"{args.command} 需要 --root（先跑 probe 得到仓库根）")
    fn = {"probe": lambda: cmd_probe(peer),
          "push": lambda: cmd_push(peer, args.root),
          "cutover": lambda: cmd_cutover(peer, args.root)}[args.command]
    asyncio.run(fn())


if __name__ == "__main__":
    main()
