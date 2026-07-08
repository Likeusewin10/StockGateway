"""对等机（peer）接入 —— 多机 Agent 协同的 hub 侧接入点（HTTP 哑服务版）。

架构切分（用户拍板）：对等机只跑一个永不需维护的 HTTP 哑执行服务（peer_service.py），
所有会演进的业务逻辑留在 hub。故 hub 不再把对等机当 MCP 上游代理挂载，而是在网关上
**注册一组 hub 原生工具**（peer_<机器名>_agent_run/_status/_result/fs_put/fs_get/fs_stat/
svc_health/svc_update），这些工具内部经 PeerClient 调对等机的 HTTP 原语。

好处：改进 agent_run 命令模板、加新工具、改 fs 分块编排 —— 全在 hub 侧改代码，对等机零感知。

配置仍走环境变量（与旧版兼容，URL 末尾的 /mcp 会被 PeerClient 自动剥掉）：

    MCP_PEERS=pc2=https://mcp-pc2.jiantx.net,mac1=https://mcp-mac1.jiantx.net
    PEER_PC2_API_KEY=<pc2 小服务的 API_KEY>
    PEER_MAC1_API_KEY=<mac1 小服务的 API_KEY>

缺 key 的 peer 被跳过（warning），不拖垮网关。凭据经 X-API-Key 注入、绝不入日志。
⚠ 不要把 hub 自己的地址写进 MCP_PEERS（环形自代理）。
"""
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from fastmcp import FastMCP

from mcp_gateway.agent_runner import build_agent_argv
from mcp_gateway.peer_client import PeerClient

logger = logging.getLogger("mcp_gateway.peers")

# peer 名规范化后必须匹配（作为工具前缀的一部分，只允许小写字母数字下划线且字母开头）。
_PEER_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def _normalize_peer_name(raw: str) -> Optional[str]:
    name = raw.strip().lower().replace("-", "_")
    return name if _PEER_NAME_RE.match(name) else None


def peer_key_env(name: str) -> str:
    """该 peer 的 API Key 环境变量名，如 pc2 -> PEER_PC2_API_KEY。"""
    return f"PEER_{name.upper()}_API_KEY"


def load_peer_clients(raw: Optional[str] = None) -> List[PeerClient]:
    """解析 MCP_PEERS 生成 PeerClient 列表；畸形/缺 key 条目跳过并告警，不抛异常。"""
    if raw is None:
        raw = os.environ.get("MCP_PEERS", "")
    clients: List[PeerClient] = []
    seen: set = set()
    for entry in raw.split(","):
        entry = entry.strip()
        if not entry:
            continue
        name_part, sep, url = entry.partition("=")
        url = url.strip()
        if not sep or not url:
            logger.warning("MCP_PEERS 条目缺 '=url'，已跳过：%r", entry)
            continue
        name = _normalize_peer_name(name_part)
        if name is None:
            logger.warning("MCP_PEERS 条目 peer 名不合法，已跳过：%r", entry)
            continue
        if not url.lower().startswith(("http://", "https://")):
            logger.warning("MCP_PEERS 条目 URL 非 http(s)，已跳过：%r", entry)
            continue
        if name in seen:
            logger.warning("MCP_PEERS 出现重复 peer 名 %s，后者已跳过", name)
            continue
        api_key = os.environ.get(peer_key_env(name), "").strip()
        if not api_key:
            logger.warning("对等机 %s 缺 %s，已跳过", name, peer_key_env(name))
            continue
        seen.add(name)
        clients.append(PeerClient(name=name, base_url=url, api_key=api_key))
    return clients


def peer_agent_run(client: PeerClient, engine: str, prompt: str,
                   session_id: str = "") -> Dict[str, Any]:
    """在对等机异步起 Agent 子进程。命令 argv 在 hub 拼好（claude 会话 UUID 预生成），
    argv[0] 保留裸引擎名交对等机 /exec 解析。返回 {task_id,status[,session_id]} 或 failed。"""
    argv, resolved_sid, err = build_agent_argv(engine, prompt, session_id or None)
    if err:
        return {"status": "failed", "error": err}
    res = client.exec(argv)
    if res.get("ok") is False:
        return {"status": "failed", "error": res.get("error", "peer exec 失败")}
    out: Dict[str, Any] = {"task_id": res.get("task_id"),
                           "status": res.get("status", "running"), "engine": engine}
    if resolved_sid:
        out["session_id"] = resolved_sid
    return out


def build_peer_mcp(client: PeerClient) -> FastMCP:
    """为一台对等机构造一个 FastMCP，含全部 hub 原生 peer 工具（裸名，挂载时加前缀）。

    工具全部为同步函数（PeerClient 走同步 httpx），薄薄转发到模块级 helper / PeerClient 方法，
    便于直接单测。
    """
    mcp = FastMCP(name=f"peer_{client.name}")

    @mcp.tool
    def agent_run(engine: str, prompt: str, session_id: str = "") -> Dict[str, Any]:
        """在该对等机上异步启动一个 Agent 子进程，立即返回 {task_id, status[, session_id]}。

        engine 限 claude/codex；session_id 留空=新会话（claude 会回传预生成 id 供续接）。
        用法：本工具拿 task_id → 轮询 <peer>_agent_status(task_id) 至终态 → _agent_result 取输出。
        """
        return peer_agent_run(client, engine, prompt, session_id)

    @mcp.tool
    def agent_status(task_id: str) -> Dict[str, Any]:
        """查该对等机上任务的状态（轻量）。返回 {task_id, status[, error]}。"""
        return client.task_status(task_id)

    @mcp.tool
    def agent_result(task_id: str) -> Dict[str, Any]:
        """取该对等机上任务的完整结果 {task_id, status, output, error, returncode}。

        建议先 agent_status 确认终态（done/failed/timeout）再取。claude 的 output 为
        --output-format json 的 JSON 信封（原样透传）。
        """
        return client.task_result(task_id)

    @mcp.tool
    def fs_put(path: str, data_b64: str, mode: str = "write",
               mkdirs: bool = True, expected_size: int = -1) -> Dict[str, Any]:
        """把 base64 字节写到该对等机磁盘（绝对路径；write 覆盖 / append 分块）。返回 {ok,...}。"""
        return client.file_put(path, data_b64, mode=mode, mkdirs=mkdirs, expected_size=expected_size)

    @mcp.tool
    def fs_get(path: str, offset: int = 0, max_bytes: int = 0) -> Dict[str, Any]:
        """从该对等机磁盘读字节返回 base64（offset 分块下载）。返回 {ok, ..., eof, data_b64}。"""
        return client.file_get(path, offset=offset, max_bytes=max_bytes)

    @mcp.tool
    def fs_stat(path: str) -> Dict[str, Any]:
        """取该对等机上文件的 {ok, path, size, sha256}（分块传输完成后做整文件终验）。"""
        return client.file_stat(path)

    @mcp.tool
    def svc_health() -> Dict[str, Any]:
        """查该对等机小服务的存活/版本/平台/引擎可用性（fleet 版本审计用）。"""
        return client.health()

    @mcp.tool
    def svc_update(source_b64: str, restart_delay: int = 8) -> Dict[str, Any]:
        """把新版 peer_service.py 源码推给该对等机自更新（py_compile 自检 + 原子替换 + 延迟重启）。

        用于极少数需要改小服务本体时的确定性推送（不经 git、不经 LLM）。返回 {ok,...}。
        """
        return client.admin_update(source_b64, restart_delay=restart_delay)

    return mcp


def load_peer_mcps(raw: Optional[str] = None) -> List[Tuple[str, FastMCP]]:
    """便捷入口：解析 MCP_PEERS 并为每台可用对等机构造 (name, FastMCP)。"""
    return [(c.name, build_peer_mcp(c)) for c in load_peer_clients(raw)]
