"""服务器端 Agent 的 MCP 工具：agent_run / agent_status / agent_result / agent_sessions。

挂到 8765 网关的 `agent` 命名空间（最终工具名 agent_agent_run 等）。鉴权/限流由网关
ApiKeyAuthMiddleware 统一覆盖，本模块不另做第二层鉴权。

异步模型：agent_run 立即返 task_id（不等子进程跑完，避开 MCP 同步超时），
调用方轮询 agent_status 直到 done/failed/timeout，再用 agent_result 取完整输出。

上下文接力：agent_run 首轮返回 session_id；后续轮把该 session_id 传回即自动续接全部历史，
客户端只保管一个几十字节的字符串，历史永远留在服务器。也可先 agent_sessions 看会话标题
列表（仿原生 /resume）挑一条续接。
"""
from typing import Dict, List

from fastmcp import FastMCP

from mcp_gateway.agent_runner import runner
from mcp_gateway.agent_sessions import list_sessions
from mcp_gateway.config import AGENT_SESSIONS_LIST_LIMIT, get_agent_project_dir

agent = FastMCP(name="agent")


@agent.tool
def agent_run(engine: str, prompt: str, session_id: str = "") -> Dict[str, str]:
    """在服务器上异步启动一个 Agent 子进程干活，立即返回 task_id。

    - engine: 引擎，限 claude / codex。
    - prompt: 交给该引擎的自然语言指令。
    - session_id: 留空=全新会话；传入=续接该会话全部历史（须为 UUID，非法直接 failed）。
    - 子进程全自动非交互执行，cwd 锁定服务器 StockSDK 项目目录；服务器 CLAUDE.md 随 prompt 自动加载。
    - 立即返回 {task_id, status, engine[, session_id]}（status=running 表示已起；failed 表示
      引擎不可用/参数错/session_id 非法，附 error）。

    上下文接力（最优雅用法，客户端只保管 session_id 字符串）：
      第1轮  agent_run("claude", "记住数字 42")              → 返回里带 session_id S
      第2轮  agent_run("claude", "我让你记的数字是几?", session_id=S) → 自动加载历史,答 42
      第3轮  agent_run("claude", "再加 1 呢?", session_id=S)   → 继续累积
    注意：claude 首轮的 session_id 在 agent_run 返回里即可拿到；codex 首轮需轮询 agent_status/
    agent_result 至终态后才会带上解析出的 session_id。

    或先调 agent_sessions() 看历史会话标题列表，挑一条的 session_id 传进来续接。

    用法：调本工具拿 task_id → 轮询 agent_status(task_id) 至终态 → agent_result(task_id) 取输出。
    """
    return runner.submit(engine, prompt, session_id=session_id)


@agent.tool
def agent_status(task_id: str) -> Dict[str, str]:
    """查询 agent_run 任务的状态（轻量，不含完整输出）。

    返回 {task_id, status, engine[, session_id][, error]}；
    status ∈ running/done/failed/timeout/unknown。session_id 可用于后续 agent_run 续接。
    """
    return runner.status(task_id)


@agent.tool
def agent_result(task_id: str) -> Dict[str, object]:
    """取 agent_run 任务的完整结果（output / error / returncode / session_id）。

    建议先 agent_status 确认进入终态（done/failed/timeout）再取，否则 output 可能为空。
    返回 {task_id, status, engine, session_id, output, error, returncode}。
    claude 的 output 为 --output-format json 的 JSON 信封（原样透传，不解包）。
    """
    return runner.result(task_id)


@agent.tool
def agent_sessions(limit: int = 0) -> List[Dict[str, object]]:
    """列出本项目历史会话（标题列表，仿原生 /resume），供挑一条续接。

    - limit: 最多回多少条；留 0/省略用默认上限。
    - 返回按修改时间倒序的列表，每条 {session_id, engine, title, mtime, modified}。
      title 派生自该会话第一条有意义的用户消息（截断）。
    - 拿到某条的 session_id 后，直接 agent_run(engine, prompt, session_id=该id) 即续接其全部历史。

    会话历史存在 claude/codex 自己的磁盘存储，与网关任务表生命周期解耦——任务表淘汰不丢会话。
    """
    n = limit if limit and limit > 0 else AGENT_SESSIONS_LIST_LIMIT
    return list_sessions(get_agent_project_dir(), n)
