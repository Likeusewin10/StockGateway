# MCP 聚合网关 —— 本机中转，远程鉴权调用

把多厂商上游 MCP 聚合成**本机一个** streamable-http 网关，让其他机器的标准 MCP 客户端
（Claude Code / Cursor 等）经公网 + API Key 远程调用。上游厂商凭据**只存本机**，绝不下发。

```
远端 MCP 客户端 ──X-API-Key──> ngrok ──> 本机网关:8765 ──厂商凭据──> 各厂商上游 MCP
   (只持 API Key)                         (验 Key/限流)   (JWT 仅在本机)
```

当前已挂载三家上游厂商（工具前缀 `<name>_<server>_<tool>`）：

| 厂商 | `name` | 上游 server | 工具数 | 鉴权方式 |
|---|---|---|---|---|
| 同花顺 iFinD | `ifind` | 7 个（stock/fund/edb/news/bond/global-stock/index） | 32 | `Authorization` 头（裸 JWE） |
| 妙想（东方财富） | `mx` | 1 个（mx-ds-mcp） | 11 | `em_api_key` 头（裸 key） |
| Tushare | `tushare` | 1 个（tushare-mcp） | 上游 258 → **网关聚合成 14**（`tushare_cat_*`） | 🔴 **URL 查询串** `?token=`（非 header） |

加上本机自有的 11 个 `agent_*` 工具，网关对外暴露 **68 个工具**（聚合前为 305）。

> **Tushare 为何要聚合？** 上游是 tool-per-API 设计（`daily`/`stock_basic`/`adj_factor`… 各一个工具，共 258 个），
> 直接透传会撑爆客户端上下文（业界实测工具选择准确率在 30~50 个后显著下降）。
> 网关层用 `ToolAggregationMiddleware`（`mcp_gateway/aggregation.py`）把 258 个收成 14 个**分类分发工具**：
> `on_list_tools` 把 `tushare_ds_*` 从列表隐藏、替换成 `tushare_cat_<分类>`（`api_name` enum + `params` 透传）；
> `on_call_tool` 把 `tushare_cat_stock_quote(api_name="daily", params={...})` 改写回 `tushare_ds_daily` 走原 proxy。
> 分类运行时从上游工具 description 的官方路径 `/数据接口/<L1>/<L2>/...` 解析（上游加接口自动落桶，解析不出进 `misc` 兜底）。
> 14 桶：stock_quote(58)/stock_ref(52)/stock_fin(10)/index(20)/alt(20)/macro(19)/fund(18)/bond(17)/hk(12)/futures(11)/us(9)/option(4)/fx_spot(4)/misc(4)。
> 代价：丢失 per-API 参数 schema（与 REST 侧 `/tdx/call/{method}` 同一权衡），各 api 参数见分类工具 description 与 Tushare 官方文档。
> 开关：`providers.py` 里该厂商 `aggregate=True`；改回 False 即恢复 258 个原样透传。
> **已真机验证（2026-07-02）**：14 桶各实调 1 个代表 API，12/14 取数成功；`us_daily`/`news` 失败是
> Tushare 官方 40203（**账号积分不够、无该接口权限**，错误原样透传），非聚合层问题——换桶内有权限的
> API（如 `us_basic`/`cctv_news`）或升级积分即可。跨桶调用（经 stock_quote 调 income）会被网关拒绝。

---

## 一、本机启动（提供方）

### 1. 准备 `.env`
从 `.env.example` 复制，填：
- `API_KEY`：你签发给远端的鉴权 key（随机串）。
- `IFIND_MCP_JWT`：iFinD 上游 JWT（从 `~/.claude.json` 里任一 iFinD server 的 `Authorization` 整串复制）。
- `MIAO_XIANG_MCP_KEY`：妙想（东方财富）上游 API key。
- `TUSHARE_MCP_TOKEN`：Tushare 上游 token（网关拼进上游 URL 查询串 `?token=`，凭据不进 header/日志）。
- `MCP_GATEWAY_PORT`：默认 8765，可不改。

缺某厂商凭据时，该厂商启动时被跳过并告警，不影响其它厂商。

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

示例（凭据走 URL 查询串的厂商，如 Tushare —— token 放 `?token=`，不是 header）：
```python
TUSHARE = Provider(
    name="tushare",
    base_url="https://api.tushare.pro/mcp/",   # base_url 本身即完整端点
    servers=(ProviderServer("tushare-mcp", "ds"),),
    auth_env="TUSHARE_MCP_TOKEN",
    auth_query="token",       # 🔴 凭据经查询串注入、不进 header（upstream 收口拼 URL）
    url_template="{base_url}",
)
PROVIDERS = (IFIND, MX, TUSHARE)
```
`auth_query` 非空时，`upstream._server_url` 把 `TUSHARE_MCP_TOKEN` 拼进上游 URL 查询串、请求头留空；
缺 token 与 header 路径一样跳过该厂商并告警。工具前缀 `tushare_ds_*`。

---

## 四、运维要点

- **凭据过期**：iFinD JWT 是加密 JWE，有效期未知。过期表现为上游返回鉴权错误 / `list_tools` 拿不到工具。
  更新：重新从桌面客户端或官方渠道取新 JWT，改 `.env` 的 `IFIND_MCP_JWT`，重启网关。
- **鉴权**：未配 `API_KEY` 且监听 `0.0.0.0` 时，启动日志会告警「不鉴权，勿暴露公网」。公网必配。
- **限流**：按客户端 IP 滑动窗口（默认 60s 内 60 次），超限返回 429。复用 `stocksdk/ratelimit.py`。
- **健康自检**：`curl -X POST http://127.0.0.1:8765/mcp` 无 key 应返回 401；带正确 key 的 MCP `initialize` 应返回 200。
- **🔴 TLS 信任（重启后全上游 `list_tools` 失败必查）**：若日志刷 `[SSL: CERTIFICATE_VERIFY_FAILED]
  unable to get local issuer certificate`、**所有厂商**都列不出工具（只剩 4 个 `agent_*`），根因是本机上游
  证书链到的根证书只在 **Windows 信任库**、不在 Python httpx 默认的 certifi bundle（典型是企业代理/杀软的
  TLS 检测根证书）。判据：`curl` 打同一 URL 成功（用 OS 库），Python 失败。修法：`.venv-mcp` 装 `truststore`
  （已列入 `requirements-mcp.txt`），`server.py` 启动时 `truststore.inject_into_ssl()` 让 Python 改走 OS 信任库
  （与 curl 一致）。此非 Tushare 专属，影响全部 https 上游。
- **重启网关**：看门狗 `start_mcp_gateway.bat` 里 uvicorn 退出后 5s 自动重启。手动重启：
  `netstat -ano | findstr :8765`（LISTENING 行取 PID）→ `taskkill /PID <pid> /F` → 约 13s 后重新监听。

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

除转发上游厂商 MCP 外，网关还自带 **14 个本机工具**（命名空间 `agent`），让远端 Agent 在服务器上异步启动
一个 `claude` / `codex` 子进程干活，结果回传。核心三件套：

| 工具 | 入参 | 返回 | 作用 |
|---|---|---|---|
| `agent_agent_run` | `engine`(claude/codex), `prompt` | `{task_id, status}` | 异步起子进程，立即返 task_id |
| `agent_agent_status` | `task_id` | `{task_id, status[, error]}` | 轮询状态：running/done/failed/timeout/unknown |
| `agent_agent_result` | `task_id` | `{status, output, error, returncode, ...}` | 取完整输出 |

其余：`agent_sessions`（扫盘列历史会话，仿 `/resume`）、`agent_events`/`agent_send`/`agent_close`
（流式事件与常驻 live 会话交互）、`agent_memory_set/get/list/delete`（服务器端跨任务记忆 KV）、
`fs_put`/`fs_get`/`fs_stat`（主机文件传输，见下）。

### 文件传输（fs_put / fs_get / fs_stat）

让大模型在网关之间搬文件：写/读的都是**工具执行所在主机**的磁盘 —— hub 上调 `agent_fs_put`
写 hub 本机，调 `peer_pc2_fs_put` 写对等机 pc2（peer 路由与 `agent_run` 完全一致，零额外配置）。
实现在 `mcp_gateway/fs_tools.py`，全程二进制安全（`wb`/`rb`，无编码/换行转换）。

| 工具 | 入参 | 返回 | 作用 |
|---|---|---|---|
| `fs_put` | `path`, `data_b64`[, `mode`=write/append, `mkdirs`=true, `expected_size`=-1] | `{ok, path, bytes_written, size, sha256}` | base64 → 磁盘二进制写；sha256 仅 write 模式（整文件哈希），append 为 null |
| `fs_get` | `path`[, `offset`=0, `max_bytes`=0] | `{ok, path, size, offset, bytes_read, eof, sha256, data_b64}` | 磁盘 → base64 读；sha256 为**本块**哈希 |
| `fs_stat` | `path` | `{ok, path, size, sha256}` | 整文件流式哈希，分块传输后终验 |

- **路径**：须绝对路径；Windows 下 `C:\Users\...` 与 MSYS `/c/Users/...` 均接受（自动归一）。
- **单次上限**：put 解码后 / get 返回各 8MB（`FS_PUT_MAX_BYTES` / `FS_GET_MAX_BYTES` 可 env 覆盖）。
- **大文件分块协议**：上传 = 首块 `mode:"write"` + 后续块 `mode:"append"`（append 不整文件重哈希，
  避免 O(n²)）；下载 = 循环 `fs_get(offset=…)` 直到 `eof:true`；传完调一次 `fs_stat`，与本地
  sha256 比对 = 字节级保证。
- **重试幂等**：append 时传 `expected_size`（=追加前应有的文件大小）；网络超时重试若该块已落盘，
  服务端按 size 不匹配拒绝并回报当前 size，防同一块被重复追加。
- **失败**：一律 `{ok:false, error}`（非法 base64 / 相对路径 / 权限 / 文件不存在），不抛协议错误。
- **安全**：与 `agent_run` 同信任模型（后者本就可在服务器执行任意命令），不设路径白名单，
  靠 X-API-Key 兜底；写操作记 info 日志（路径+字节数，不记内容）。

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

## 七、多机 Agent 协同（hub + 对等机）

把另外 N 台机器上的 Agent 能力聚合进本机网关：**对等机跑 agent-only 网关，hub 把它们
当上游 MCP 挂载**，客户端仍只连 hub 一个入口、一把 key。

```
客户端 ── hub 网关 :8765 (MCP_GATEWAY_MODE=full，默认)
           ├── agent_*                  本机 agent 工具
           ├── peer_pc2_agent_run …    对等机 pc2（https://mcp-pc2.jiantx.net/mcp）
           └── peer_mac1_agent_run …   对等机 mac1（https://mcp-mac1.jiantx.net/mcp）
（域名由香港节点 Caddy 终结 HTTPS → frps 内部口 187xx → 对等机 frpc；
  frps 明文口被 nftables 封，公网裸 IP:端口连不通，MCP_PEERS 必须填域名 HTTPS。）
对等机 ── 同一仓库，MCP_GATEWAY_MODE=agent-only：只暴露裸名 agent_run 等，
          不挂任何厂商上游（不需要股票凭据）。
```

- **hub 配置**：`.env` 填 `MCP_PEERS=name=url,…` + 每机一把 `PEER_<NAME大写>_API_KEY`
  （= 对等机自己的 API_KEY）。解析在 `mcp_gateway/peers.py`，复用 Provider/upstream
  全套机制：缺 key / 条目畸形只 warning 跳过；凭据经 `X-API-Key` 头注入，不进日志。
- **对等机部署**：全流程见 [`docs/部署-对等机AgentMCP.md`](部署-对等机AgentMCP.md)
  （可直接丢给对等机上的 Claude Code 自动执行）。
- **容错**：peer 的 connect 超时固定 5s（`peers.py`），对等机宕机不拖死 hub；长期关机的
  peer 建议从 `MCP_PEERS` 摘除。
- **边界**：session_id 不跨机（会话历史存各机本地）；agent_memory 也是各机独立存储；
  🔴 别把 hub 自己的地址写进 hub 的 MCP_PEERS（环形自代理）。
- **自检**：`scripts/check_mcp_gateway.py`（CHECK_API_KEY + 可选 URL 参数）对本机/对等机
  做握手 + tools/list。

> 对等机同时支持 **Windows 与 macOS**：网关/agent 代码本身跨平台（agent_runner 用
> `shutil.which` 解析引擎路径，两平台通吃）；差异只在运维壳——Windows 走计划任务 +
> 看门狗 bat，macOS 走 launchd（`KeepAlive` 自带自愈），frp token 分别放
> `frpc.secret.bat` / `frpc.secret.sh`（均 gitignore）。系统分支详见部署手册。
