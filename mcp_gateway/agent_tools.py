"""服务器端 Agent 的 MCP 工具：agent_run / agent_status / agent_result / agent_sessions。

挂到 8765 网关的 `agent` 命名空间（最终工具名 agent_agent_run 等）。鉴权/限流由网关
ApiKeyAuthMiddleware 统一覆盖，本模块不另做第二层鉴权。

异步模型：agent_run 立即返 task_id（不等子进程跑完，避开 MCP 同步超时），
调用方轮询 agent_status 直到 done/failed/timeout，再用 agent_result 取完整输出。

上下文接力：agent_run 首轮返回 session_id；后续轮把该 session_id 传回即自动续接全部历史，
客户端只保管一个几十字节的字符串，历史永远留在服务器。也可先 agent_sessions 看会话标题
列表（仿原生 /resume）挑一条续接。
"""
from typing import Any, Dict, List

from fastmcp import FastMCP

from mcp_gateway.agent_runner import runner
from mcp_gateway.agent_sessions import list_sessions
from mcp_gateway.config import AGENT_SESSIONS_LIST_LIMIT, get_agent_project_dir
from mcp_gateway.host_memory import mem_delete, mem_get, mem_list, mem_set, recall_for_prompt

agent = FastMCP(name="agent")


@agent.tool
def agent_run(engine: str, prompt: str, session_id: str = "", host_id: str = "",
              live: bool = False) -> Dict[str, str]:
    """在服务器上异步启动一个 Agent 子进程干活，立即返回 task_id。

    - engine: 引擎，限 claude / codex。
    - prompt: 交给该引擎的自然语言指令。
    - session_id: 留空=全新会话；传入=续接该会话全部历史（须为 UUID，非法直接 failed）。
    - host_id: 留空=不注入记忆；传入=自动把该 host 的全部记忆前置注入 prompt（记忆通过
      agent_memory_set 写入，让每轮 Agent 调用都能感知长期上下文）。
    - 子进程全自动非交互执行，cwd 锁定服务器 StockSDK 项目目录；服务器 CLAUDE.md 随 prompt 自动加载。
    - 立即返回 {task_id, status, engine[, session_id]}（status=running 表示已起；failed 表示
      引擎不可用/参数错/session_id 非法，附 error）。

    用法：调本工具拿 task_id → 轮询 agent_status(task_id) 至终态 → agent_result(task_id) 取输出。
    """
    return runner.submit(engine, recall_for_prompt(host_id, prompt, query=prompt),
                         session_id=session_id, live=live)


@agent.tool
def agent_send(task_id: str, message: str, priority: int = 0) -> Dict[str, object]:
    """Inject a user message into a running live session.

    The message is consumed at the next turn boundary; a higher priority is
    served first. Returns {ok, task_id[, queued|error|status]}.
    """
    return runner.send(task_id, message, priority)


@agent.tool
def agent_close(task_id: str) -> Dict[str, object]:
    """Request closing a live session so its stdin is closed and the process winds down.

    Returns {ok, task_id[, status]}.
    """
    return runner.close(task_id)


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
def agent_events(task_id: str, cursor: int = 0) -> Dict[str, object]:
    """拉取 agent_run 任务中 seq 大于 cursor 的流式事件（增量轮询）。

    返回 {task_id, status, events, next_cursor, dropped}。
    每次轮询把上次返回的 next_cursor 作为本次 cursor 传回，即可只取新增事件。
    dropped 统计内存缓冲溢出时被逐出的最旧事件数。
    """
    return runner.events(task_id, cursor)


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


@agent.tool
def agent_memory_set(host_id: str, slug: str, body: str,
                     description: str = "", type: str = "project") -> Dict[str, Any]:
    """为指定 host 持久化一条结构化事实（覆盖已有同名 slug）。

    - slug: 唯一键（字母数字及 - _ .）。
    - body: 完整事实内容。
    - description: 一句话摘要，用于召回排序。
    - type: 事实类型，取值 user/project/feedback/reference。
    """
    return mem_set(host_id, slug, body, type=type, description=description)


@agent.tool
def agent_memory_get(host_id: str, slug: str) -> Dict[str, Any]:
    """读取指定 host 的一条记忆（slug 不存在时 ok=false）。"""
    return mem_get(host_id, slug)


@agent.tool
def agent_memory_delete(host_id: str, slug: str) -> Dict[str, Any]:
    """删除指定 host 的一条记忆（slug 不存在时也返回 ok=true，deleted=false）。"""
    return mem_delete(host_id, slug)


@agent.tool
def agent_memory_list(host_id: str) -> Dict[str, Any]:
    """列出指定 host 所有已存储的 slug 及元数据。返回 {ok, host_id, slugs, facts, count}。"""
    return mem_list(host_id)
