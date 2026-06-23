# MCP 聚合网关 —— 本机中转，远程鉴权调用

把多厂商上游 MCP 聚合成**本机一个** streamable-http 网关，让其他机器的标准 MCP 客户端
（Claude Code / Cursor 等）经公网 + API Key 远程调用。上游厂商凭据**只存本机**，绝不下发。

```
远端 MCP 客户端 ──X-API-Key──> ngrok ──> 本机网关:8765 ──厂商凭据──> 各厂商上游 MCP
   (只持 API Key)                         (验 Key/限流)   (JWT 仅在本机)
```

首个厂商是 iFinD（同花顺）的 7 个 MCP server（stock/fund/edb/news/bond/global-stock/index，
共 32 个工具），在网关里以 `ifind_<server>_<tool>` 前缀暴露。

---

## 一、本机启动（提供方）

### 1. 准备 `.env`
从 `.env.example` 复制，填三项：
- `API_KEY`：你签发给远端的鉴权 key（随机串）。
- `IFIND_MCP_JWT`：iFinD 上游 JWT（从 `~/.claude.json` 里任一 iFinD server 的 `Authorization` 整串复制）。
- `MCP_GATEWAY_PORT`：默认 8765，可不改。

### 2. 起网关（看门狗自重启）
```bat
start_mcp_gateway.bat
```
监听 `0.0.0.0:8765`，日志写 `mcp_gateway.log`。与 8000 的 REST 服务互不影响，可并存。

### 3. 公网暴露（ngrok）
> ngrok 免费版同一 authtoken 只允许 **1 个 agent 会话**，而 8000 已占用。
> 故用一个 agent 同时起两个 tunnel（api + mcp），见 `ngrok-gateway.yml` / `start_ngrok_gateway.bat`：
```bat
start_ngrok_gateway.bat
```
mcp tunnel 若无第二个固定域名，会分配随机域名（看 `ngrok.log` 或 ngrok 后台）。
付费版可直接两个 agent 各跑各的，无需合并。

---

## 二、远端接入（调用方）

在远端机器的 `~/.claude.json`（或 Cursor 的 MCP 配置）里，**只加一条**：

```json
{
  "mcpServers": {
    "mcp-gateway": {
      "type": "http",
      "url": "https://<你的ngrok域名>/mcp",
      "headers": { "X-API-Key": "<你签发的API_KEY>" }
    }
  }
}
```

- 原来 7 条 iFinD 直连配置 → 现在**收敛成 1 条网关配置**。
- 上游 JWT 不出现在远端任何地方，远端只持有 `API_KEY`。
- 工具名带前缀（如 `ifind_stock_get_stock_summary`），与原直连工具一一对应。

> 客户端若不便设 `X-API-Key`，也可用 `"Authorization": "Bearer <API_KEY>"`，网关两者都认。

---

## 三、加新厂商（三步，零网关代码改动）

1. **注册**：在 `mcp_gateway/providers.py` 的 `PROVIDERS` 追加一个 `Provider(...)`，
   填 `name`（全局唯一）、`base_url`、`servers`、`auth_env`（凭据环境变量名）、`auth_scheme`。
2. **填凭据**：在 `.env` 增加与 `auth_env` 同名的变量。
3. **重启网关**。新厂商工具自动以 `<name>_*` 前缀出现，**远端配置无需改动**。

缺凭据的厂商在启动时被跳过并告警，不影响其它厂商。

示例（带 Bearer 前缀的厂商）：
```python
DEMO = Provider(
    name="demo",
    base_url="https://demo.example.com/mcp-servers",
    servers=(ProviderServer("demo-quote-mcp", "quote"),),
    auth_env="DEMO_MCP_TOKEN",
    auth_scheme="Bearer ",
)
PROVIDERS = (IFIND, DEMO)
```

---

## 四、运维要点

- **凭据过期**：iFinD JWT 是加密 JWE，有效期未知。过期表现为上游返回鉴权错误 / `list_tools` 拿不到工具。
  更新：重新从桌面客户端或官方渠道取新 JWT，改 `.env` 的 `IFIND_MCP_JWT`，重启网关。
- **鉴权**：未配 `API_KEY` 且监听 `0.0.0.0` 时，启动日志会告警「不鉴权，勿暴露公网」。公网必配。
- **限流**：按客户端 IP 滑动窗口（默认 60s 内 60 次），超限返回 429。复用 `stocksdk/ratelimit.py`。
- **健康自检**：`curl -X POST http://127.0.0.1:8765/mcp` 无 key 应返回 401；带正确 key 的 MCP `initialize` 应返回 200。

## 五、本机连通自测

```bash
# 无 key → 401
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:8765/mcp
# 正确 key + MCP initialize → 200
curl -s -o /dev/null -w '%{http_code}\n' -X POST \
  -H "X-API-Key: <你的API_KEY>" -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}' \
  http://127.0.0.1:8765/mcp
```

---

## 六、服务器端 Agent 工具（本地指挥服务器干活）

除转发上游厂商 MCP 外，网关还自带三个**本机工具**，让远端 Agent 在服务器上异步启动
一个 `claude` / `codex` 子进程干活，结果回传。命名空间 `agent`，工具名：

| 工具 | 入参 | 返回 | 作用 |
|---|---|---|---|
| `agent_agent_run` | `engine`(claude/codex), `prompt` | `{task_id, status}` | 异步起子进程，立即返 task_id |
| `agent_agent_status` | `task_id` | `{task_id, status[, error]}` | 轮询状态：running/done/failed/timeout/unknown |
| `agent_agent_result` | `task_id` | `{status, output, error, returncode, ...}` | 取完整输出 |

### 异步轮询流程

MCP 同步调用有超时，长任务不能在一次调用里等完。因此：

```
agent_agent_run(engine="claude", prompt="列出当前目录并解释结构")
  → {task_id: "ab12…", status: "running"}
# 轮询直到终态
agent_agent_status("ab12…")  → status: "running" … 直到 "done"/"failed"/"timeout"
agent_agent_result("ab12…")  → {status:"done", output:"...", returncode:0}
```

> 第一步不做常驻会话 / 跨任务上下文。服务器的 `CLAUDE.md`（本仓库根）每次随 prompt 自动加载，
> 弥补无常驻会话的上下文缺口。常驻（session 复用）是验证后的第二步。

### 🔴 安全说明（务必知晓）

子进程以**全自动、非交互**方式执行：

```
claude:  claude -p "<prompt>" --dangerously-skip-permissions
codex:   codex exec "<prompt>" --dangerously-bypass-approvals-and-sandbox
```

这两个 flag = **任何拿到 X-API-Key 的人都能让服务器 Agent 无需确认、绕过沙箱、执行任意命令**
（读写删文件 / 跑 shell / 联网）。全自动是异步任务的必要选择（否则卡在审批提示），但配套两道
防线绝不能省：

1. **X-API-Key 必须强随机，且只发可信本地机器**——这是唯一的访问门槛。
2. **cwd 锁死 `AGENT_PROJECT_DIR`**（默认本仓库根），子进程只能在项目目录内操作。

引擎前置：服务器侧需已登录（`claude` 登录态 / `codex login`），否则非交互启动即失败，
`agent_run` 返回 `status=failed` 并附脱敏 reason。`codex` 未装时 `engine=codex` 返回
`failed`（unavailable），不影响 `claude`。

相关配置（`.env`，均可选）：`AGENT_PROJECT_DIR` 覆盖执行目录；超时/任务上限在
`mcp_gateway/config.py`（`AGENT_TASK_TIMEOUT_SECONDS` / `AGENT_MAX_TASKS`）。
