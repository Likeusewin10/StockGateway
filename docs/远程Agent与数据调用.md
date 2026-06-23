# 远程调用服务器端 Agent + 股票数据 MCP

本机(如 Mac)通过 MCP 协议,经公网调用这台 Windows 服务器上的 **36 个工具**:
4 个 Agent 工具(在服务器上起 claude/codex 干活)+ 32 个 iFinD 股票数据工具。

```
本机 MCP 客户端 ──X-API-Key──> ngrok ──> 服务器:8765 网关 ┬─ agent_* :起 claude/codex 子进程
  (Claude Code/Cursor)      jtx-mcp.ngrok.app           └─ ifind_* :转发同花顺上游取数
```

> **主用 Agent = 服务器端的 Claude Code 子进程(`engine=claude`)。** 这是你日常指挥、主要沟通的对象;`codex` 仅作备选引擎。
> 子进程仍是现起、cwd 锁死服务器 StockSDK 目录、带服务器 `CLAUDE.md` 身份的一次性进程;但**现已支持上下文接力**——首轮返回 `session_id`,后续把它传回即续接全部历史(详见 §三-A 会话语义)。客户端只保管一个几十字节的 `session_id` 字符串,历史永留服务器。

---

## 一、服务器端(提供方,已配好)

三件套常驻,均看门狗自愈,**开机自启**:

| 组件 | 启动方式 | 端口/地址 | 作用 |
|---|---|---|---|
| MCP 网关 | `start_mcp_gateway.bat`(看门狗) | `:8765` | 36 个工具的本机网关 |
| ngrok 隧道 | 计划任务 `NgrokTunnel` → `start_ngrok.bat` | `jtx-mcp.ngrok.app` → 8765 | 公网暴露(同会话还带 `jtx.ngrok.app`→8000 REST) |
| (引擎) | `claude` 已登录 / `codex login` | — | agent 子进程靠它跑 |

### 凭据(都在 `.env`,gitignored)
- `API_KEY`:对外鉴权 key(32 位随机串)。**= 调用方的唯一钥匙,也 = 在服务器执行任意命令的钥匙,只发可信机器。**
- `IFIND_MCP_JWT`:iFinD 上游令牌(从 `~/.claude.json` 的 iFinD server `Authorization` 复制整串)。过期表现为 `ifind_*` 取数报鉴权错 → 重取新串改 `.env` → 重启网关。

### 起停 / 自检
```bash
# 起网关(看门狗,崩溃 5s 自重启)
start_mcp_gateway.bat

# ngrok 由计划任务管,需手动重启时:
powershell -Command "Stop-ScheduledTask -TaskName NgrokTunnel; Start-Sleep 2; Start-ScheduledTask -TaskName NgrokTunnel"

# 本机自检(无 key 应 401,带 key initialize 应 200)
curl -s -o nul -w "%{http_code}\n" -X POST http://127.0.0.1:8765/mcp
```

> ⚠ **全机只允许一个 ngrok 会话**:api+mcp 两隧道合在 `start_ngrok.bat` 一个会话里。
> 别再另起第二个 ngrok 看门狗,否则两会话抢同一域名报 `endpoint already online` 致整会话退出(历史踩坑)。
> 加隧道就改 `start_ngrok.bat` + `ngrok-gateway.yml`。

---

## 二、客户端接入(调用方,如 Mac)

需要两样东西:**网关地址** `https://jtx-mcp.ngrok.app/mcp` + **服务器 `.env` 里的 `API_KEY`**。

### 方法 A:对话式添加(最省事,推荐)

在 **Claude 桌面版 / Codex 桌面版**的对话框里,直接把下面这句发给它(把密钥替换成真实 `API_KEY`),
它会自动帮你把 MCP server 加进配置:

```
帮我添加一个 mcp 服务:
claude mcp add --transport http stocksdk-gateway https://jtx-mcp.ngrok.app/mcp --header "X-API-Key: <API_KEY>"
```

> 桌面版会代为执行 `claude mcp add`,无需手动进设置界面点选。加完通常要重启/重连一次客户端。

### 方法 B:命令行(用 Claude Code CLI 时)

```bash
claude mcp add --transport http stocksdk-gateway https://jtx-mcp.ngrok.app/mcp \
  --header "X-API-Key: <API_KEY>"
```

### 方法 C:手改配置文件

`~/.claude.json`(或对应客户端的 MCP 配置)加:
```json
{
  "mcpServers": {
    "stocksdk-gateway": {
      "type": "http",
      "url": "https://jtx-mcp.ngrok.app/mcp",
      "headers": { "X-API-Key": "<API_KEY>" }
    }
  }
}
```

### 验证 / 维护
- 连上后 `/mcp`(或客户端 MCP 面板)应显示 `stocksdk-gateway` 已连接、**36 个工具**。
- 改地址或密钥:多数客户端**无编辑功能**,需先删除该 server 再重新添加。
- 🔴 `API_KEY` 别贴进聊天截图/公开渠道——它=调用网关、并在服务器执行任意命令的钥匙。


---

## 三、用法

### A. 指挥服务器端 Agent 干活(异步三步 + 上下文接力)

工具:`agent_agent_run` / `agent_agent_status` / `agent_agent_result` / `agent_agent_sessions`。
异步模型(避开 MCP 同步超时):起任务拿 `task_id` → 轮询 status 至终态 → 取 result。

> 直接用自然语言让客户端 Claude 代劳即可,例:
> 「用 stocksdk-gateway 的 agent_agent_run,engine=claude,prompt="列出当前目录前3个文件",轮询到 done 再取结果」

- `engine`:限 `claude` / `codex`。**主用 `claude`**(服务器端 Claude Code 子进程,默认沟通对象);`codex` 备选。
- 子进程**全自动非交互**,cwd 锁死服务器 StockSDK 目录;服务器 `CLAUDE.md` 随 prompt 自动加载。
- status:`running` / `done` / `failed` / `timeout` / `unknown`。
- 🔴 全自动 = 拿到 API_KEY 即可让服务器无确认执行任意命令。**key 只发可信机器。**

#### 会话语义:支持上下文接力(session_id 回传 / 续传)

`agent_agent_run` 现在接受 `engine` + `prompt` + 可选 `session_id` 三个字段。会话历史**永远留在服务器**,客户端只需保管一个几十字节的 `session_id` 字符串:

```
第1轮  agent_run(engine=claude, prompt="记住数字 42")                  → 返回里带 session_id S
第2轮  agent_run(engine=claude, prompt="我让你记的数字是几?", session_id=S) → 自动加载历史,答 42
第3轮  agent_run(engine=claude, prompt="再加 1 呢?", session_id=S)         → 继续累积
```

- **不传 `session_id`** = 全新会话(行为同改造前,向后兼容)。
- **传入 `session_id`** = 续接该会话的全部历史(须为合法 UUID,非法直接 `failed`)。
- `task_id` 仍只是这一次任务的轮询句柄(给 status/result 用),**与 `session_id` 是两码事**——`session_id` 才是跨轮续接的钥匙。
- **两引擎拿 id 的时机不同**:
  - `claude`:服务器**预生成** session_id,**首轮 `agent_run` 即时返回里就带**,无需等终态。
  - `codex`:id 由 codex 自己生成,**须轮询到终态后**从 `agent_status`/`agent_result` 里拿。

**看历史会话标题列表(仿原生 `/resume`)**:调 `agent_agent_sessions`(可选 `limit`)列出本项目下 claude+codex 的历史会话,每条含 `session_id` + 派生标题(取该会话第一条有意义的用户消息)+ 时间,按修改时间倒序。挑一条的 `session_id` 直接喂给 `agent_run` 即续接。

> 例:「用 stocksdk-gateway 的 agent_agent_sessions 看最近 10 个会话,选标题里提到 MCP 网关那条,用它的 session_id 继续问 xxx」

> 会话历史存在 claude/codex 各自的磁盘存储,与网关任务表(`AGENT_MAX_TASKS` 淘汰)生命周期**解耦**——任务表淘汰不丢会话。续接时若服务器侧对应会话历史已被 CLI 清理,子进程会非零退出走 `failed`,据 error 重开首轮即可。

### B. 取股票数据(iFinD,32 工具)

工具前缀 `ifind_<模块>_<工具>`,模块:`stock` / `fund` / `bond` / `index` / `edb`(宏观)/ `news` / `global_stock`。
> 例:「用 stocksdk-gateway 查贵州茅台最新行情」→ 客户端会调 `ifind_stock_get_stock_summary`。

常用:`ifind_stock_get_stock_summary`(个股摘要)、`ifind_stock_stock_highfreq_quotes`(实时/高频)、
`ifind_stock_get_stock_financials`(财务)、`ifind_index_index_data`(指数)、`ifind_edb_get_edb_data`(宏观)。

---

## 四、用户安装后的基本测试

客户端(如 Mac 的 Claude Code / Cursor)按 §二 加好 `stocksdk-gateway` 后,**用自然语言**让客户端逐条照做即可,无需写代码。五步从连通到接力,全绿即可用:

**0. 连通 + 工具数**
> 「列出 stocksdk-gateway 的所有工具」
- 预期:连接成功,共 **36 个**工具(`agent_*` 4 个 + `ifind_*` 32 个)。看不到 → §五排错「连不上 / 401」。

**1. 取一条数据(验上游链路)**
> 「用 stocksdk-gateway 查贵州茅台最新行情」
- 预期:客户端调 `ifind_stock_get_stock_summary` 返回个股摘要。报鉴权错 → `IFIND_MCP_JWT` 过期(见排错)。

**2. 起一次 Agent(验异步三步)**
> 「用 stocksdk-gateway 的 agent_agent_run,engine=claude,prompt="用一句话说明你当前的工作目录,并列出前3个文件",轮询 agent_agent_status 到 done,再用 agent_agent_result 取输出」
- 预期:status 走 `running → done`,output 里是服务器 StockSDK 目录的信息。`failed` 且 error 提到登录 → 服务器侧 `claude` 未登录。

**3. 上下文接力(验新功能 session_id)**
> 「agent_agent_run,engine=claude,prompt="记住数字 42",拿到返回里的 session_id;轮询到 done 后,再 agent_agent_run,engine=claude,prompt='我刚让你记的数字是几?',把上一步的 session_id 传进去」
- 预期:第二轮 output 里出现 **42**,证明历史在服务器侧续上了。
- claude 的 session_id 在**首轮 run 即时返回里**就有;若用 `engine=codex`,需轮询到终态后再从 status/result 里取 session_id。

**4. 会话列表(验 agent_sessions,仿 /resume)**
> 「用 stocksdk-gateway 的 agent_agent_sessions 列出最近会话」
- 预期:返回一个列表,每条含 `session_id` + 标题(第3步那轮的标题应是「记住数字 42」)+ 时间,按时间倒序。挑一条 session_id 喂回 `agent_run` 即可继续那段对话。

> 想在**服务器本机**(不走公网)验证同样链路,见 §五「本机冒烟脚本」。

---

## 五、排错

| 现象 | 排查 |
|---|---|
| 客户端连不上 / `/mcp` 失败 | ① 服务器 `curl http://127.0.0.1:8765/mcp` 本机通不通(网关挂了→`start_mcp_gateway.bat`);② 公网 `curl https://jtx-mcp.ngrok.app/mcp` 通不通(ngrok 掉了→重启计划任务) |
| 401 | API_KEY 不匹配,核对客户端 header 与服务器 `.env` |
| `agent_run` 返回 failed | 看 error:引擎未登录(服务器 `claude`/`codex login`)、prompt 空、engine 不在白名单、`session_id` 非法(须为 UUID) |
| 续接没接上历史(答不出第3步的 42) | 多半传错了字段:接力靠 `session_id`,**不是** `task_id`;或服务器侧该会话历史已被 CLI 清理(走 failed),重开首轮即可 |
| `ifind_*` 取数鉴权错 | `IFIND_MCP_JWT` 过期,重取新串改 `.env` 重启网关 |
| 公网 mcp 偶发 000/404 | 隧道刚重建的瞬态,等几秒重试;持续则查 `ngrok.log` 有无 `already online`(多会话冲突) |

### 本机冒烟脚本
`loadtest/smoke_agent.py`:在服务器本机经 8765 完整跑一遍 agent_run→轮询→result,验证网关+claude 链路(不走公网)。
```bash
.venv-mcp\Scripts\python loadtest\smoke_agent.py
```
> Git-Bash 控制台显示中文乱码是终端编码问题,数据本身正确。

---

## 六、相关文件

| 文件 | 作用 |
|---|---|
| `mcp_gateway/agent_runner.py` | Agent 异步任务核心(起子进程/状态机/超时/session_id 接力) |
| `mcp_gateway/agent_sessions.py` | 扫盘列会话(仿 /resume,派生标题) |
| `mcp_gateway/agent_tools.py` | 四个 agent MCP 工具(run/status/result/sessions) |
| `mcp_gateway/providers.py` | iFinD 厂商注册表(加新厂商处) |
| `ngrok-gateway.yml` | 两条隧道定义(api + mcp) |
| `start_ngrok.bat` | ngrok 看门狗(计划任务 NgrokTunnel 拉起,带两隧道) |
| `start_mcp_gateway.bat` | 网关看门狗 |
| `loadtest/smoke_agent.py` | 本机端到端冒烟 |
| `docs/MCP中转网关.md` | 网关原理 + 加厂商 + 安全细节 |
