# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

把两个 Windows-only、单会话的桌面股票数据 SDK（东方财富 **EMQuantAPI** 与同花顺 **iFinD**）包成可远程取数的服务，并把多厂商上游 MCP 聚合成本机一个网关。三件独立产物：

1. **REST + WebSocket 取数服务**（`app.py` + `stocksdk/`，端口 8000）—— 别的项目用 `ip:端口 + 参数` 取数，不写 SDK 代码。
2. **MCP 聚合网关**（`mcp_gateway/`，端口 8765）—— 把上游厂商 MCP 中转给远程标准 MCP 客户端，上游凭据只存本机。
3. **生产压测工具**（`loadtest/`）—— 验证崩溃自愈、并发承载、WS 长稳。

公网暴露通过 ngrok（一个 agent 同时暴露 8000 + 8765）。文档在 `docs/`（含 MCP 中转网关、iFinD 字段字典等）。

### 🔴 定位边界（别搞混两个仓库）

**本仓库只是「数据提供方」，只读取数、不下单、不交易。** 消费方是**另一个仓库 STS-codex**（交易系统，本机不存在）。

`docs/数据激活.md`（数据源激活手册）里的 `trading-system` CLI、SQLite、source-priority resolver **全部属于 STS-codex，不在本仓库实现**。本仓库对它只负责两件事：① 把数据取出来；② 用 [`docs/数据源对照-StockSDK提供.md`](docs/数据源对照-StockSDK提供.md) 说明「哪个字段走哪个端点」。看到要在本仓库实现 resolver / Choice provider 的需求，先回到这条边界确认。

## 多 venv 结构（关键，别搞混）

每个产物用独立的 Python 3.11.4 x64 venv，**互不共享 site-packages**：

| venv | 用途 | 依赖文件 |
|---|---|---|
| `.venv-em` | EM SDK（通过 `.pth` 引用 `D:\dev\Project\EMQuantAPI_Python\python3`，不复制进库） | `requirements-em.txt` |
| `.venv-ths` | iFinD SDK | `requirements-ths.txt` |
| `.venv-api` | HTTP/WS 服务 + pytest + 压测 | `requirements-api.txt` |
| `.venv-mcp` | MCP 网关 | `requirements-mcp.txt` |

运行命令时**一律用 venv 内的 `Scripts\python.exe` / `pytest.exe` / `uvicorn.exe`**，不要用系统 Python。EM SDK 还需本机装 Microsoft Visual C++ 2010 可再发行组件包（x64）。

## 常用命令

```bat
:: 测试（在 .venv-api 下；测试用桩替换两个 SDK，不触发真实登录/网络）
.venv-api\Scripts\python -m pytest --cov=stocksdk
.venv-api\Scripts\python -m pytest tests\test_routes.py            :: 单文件
.venv-api\Scripts\python -m pytest tests\test_routes.py::test_xxx  :: 单用例

:: MCP 网关测试（在 .venv-mcp 下）
.venv-mcp\Scripts\python -m pytest tests\test_mcp_gateway_auth.py tests\test_mcp_gateway_providers.py

:: 启动 REST 服务（看门狗模式，崩溃 5s 自动重启）—— 必须单 worker
start_server.bat
:: 或手动：.venv-api\Scripts\uvicorn app:app --host 0.0.0.0 --port 8000

:: 启动 MCP 网关（看门狗）
start_mcp_gateway.bat

:: 公网暴露（一个 ngrok agent 同时暴露 8000+8765）
start_ngrok_gateway.bat

:: 交互式 API 文档
:: http://<ip>:8000/docs

:: 健康自测（浅 = 进程存活；深 = 实测两源取数 + 时延）
curl -s http://127.0.0.1:8000/health
curl -s -H "X-API-Key: <key>" http://127.0.0.1:8000/health/deep
```

压测见 `loadtest/README.md`。⚠ 压测脚本**别用 Git-Bash 直接跑**：它会把 `--target /health` 转义成 Windows 路径致全部请求失败；用 `cmd` 或设 `MSYS_NO_PATHCONV=1`。

## 架构要点（多文件交叉、需先理解）

### 单会话 + 全局锁串行化（最重要的约束）

两个 SDK 都是**单会话、单点登录**。`stocksdk/sessions.py` 持一把进程全局 `threading.Lock`，**所有取数串行化**。后果遍布全栈：

- **必须单 worker 部署**，不能加 `--workers`，不能起多进程——会话会互相挤掉。
- 取数端点吞吐不随并发翻倍、延迟随并发线性上升，是**设计预期，不是缺陷**。
- 服务用的账号不要同时在桌面客户端或其它脚本登录同一账号。

### 会话自愈（sessions.py）

底层会话会被悄悄踢掉（同账号别处登录、iFinD 单点冲突、令牌超时）。`em_exec` / `ths_exec` 包裹取数 thunk：取数返回会话/登录失效码（`_EM_SESSION_CODES` / `_THS_SESSION_CODES`，外加文本关键词兜底）时**强制重登并重试一次**。EM 用 `ForceLogin=1` 抢登；iFinD 先 `Logout` 再 `Login`。`ensure_em(force=True)` / `ensure_ths(force=True)` 是强制重登入口。**调用方须已持有全局 `lock`**（这两个函数不自己加锁）。

### 通用透传（routes_em.py / routes_ths.py）

除固定端点（EM 的 `/em/csd`、`/em/css`；iFinD 类似）外，`/em/call/{method}` 用 `getattr` 动态分发，**SDK 全部方法均可调用**。`/em/methods` 仅做**提示性标注**（异步/交易/会话管理类），不再拦截。仅拦截下划线开头的私有方法。透传调用经 `serialize.merge_pandas_option` 智能补 `Ispandas=1`（仅当末参看起来像 options 串）。

### 返回值归一化（serialize.py）

EM / iFinD 返回类型各异（DataFrame / 自定义对象 / dict），统一成 JSON 友好结构。SDK 错误码翻译成 **HTTP 502**；参数不匹配 → 400；重登失败的 502 直接透传。

### WebSocket 真订阅推送（routes_ws.py）

SDK 回调在后台线程触发 → `loop.call_soon_threadsafe` 塞进 `asyncio.Queue`（每连接上限 `WS_QUEUE_MAXSIZE`）→ pump 协程发给 WS。注册/退订在 executor 线程里**持全局锁**执行，推送本身不碰锁。断开自动退订全部订阅，避免 SDK 侧泄漏。WS 鉴权走 query 参数 `?key=`（WS 不便带请求头）。注意：EM 账号常无 `csq` 行情权限会返回 error 事件，iFinD 可推送。

### MCP 网关（mcp_gateway/）

FastMCP `create_proxy` + `gateway.mount`，把每个上游 server 以 `f"{provider}_{server_short}"` 前缀挂载（命名空间隔离）。**加新厂商 = 往 `providers.py` 的 `PROVIDERS` 追加一个 `Provider` 条目 + 在 `.env` 填该厂商凭据变量**，不改任何执行代码。凭据读取在 `upstream.py` 收口（注册表只存环境变量**名**，绝不存凭据本身）。缺凭据的厂商被跳过（warning），不影响其它厂商。

### 服务器端 Agent 工具（mcp_gateway/agent_runner.py + agent_tools.py）

网关自带三个本机工具（命名空间 `agent`，工具名 `agent_agent_run`/`_status`/`_result`），让远端 Agent 在服务器上**异步**起一次性 `claude -p` / `codex exec` 子进程干活、轮询取结果，实现「本地 Agent 指挥服务器 Agent」。异步模型（立即返 `task_id` + 后台线程跑 + 轮询）避开 MCP 同步超时；状态机 `running→done|failed|timeout`。🔴 子进程全自动非交互（`--dangerously-*`），靠两道防线：① 复用网关 X-API-Key（强随机、只发可信机器）；② **cwd 锁死 `AGENT_PROJECT_DIR`**（`config.get_agent_project_dir` 校验覆盖值仍在仓库根内）。引擎限 `claude`/`codex` 白名单 + `shutil.which` 探活，未装/未登录返回 `failed` 不崩。命令模板里 `--` 在 `{prompt}` 前，防 `-` 开头 prompt 被当 flag。第一步不做常驻会话/跨任务上下文（服务器 `CLAUDE.md` 随 prompt 自动加载弥补）。详见 [`docs/MCP中转网关.md`](docs/MCP中转网关.md) 第六节。

### 安全（security.py / ratelimit.py）

服务经 ngrok 公网暴露，鉴权/限流为必需。`X-API-Key` 常量时间比较（`secrets.compare_digest`）；按 IP 滑动窗口限流（默认 `60 次/60s`，见 `config.py` 常量）。框架无关原语在 `ratelimit.py`，供网关复用同一份逻辑避免漂移；`security.py` 只做 FastAPI 适配。未配 `API_KEY` 时不鉴权（仅本机/内网），启动时 warning。

## 约定

- **凭据一律从 `.env` / 环境变量读**，无硬编码。`config.load_dotenv` 用 `setdefault`（真实环境变量优先）。`.env` / `userInfo` / `*.log` 已 gitignore。配置模板见 `.env.example`。
- `stocksdk/config.py` 只依赖标准库，三个 venv 都能导入；魔法数字（端口、队列上限、限流阈值、重启间隔）集中在此，**不要散落硬编码**。
- `app.py` 仅负责装配（CORS / 路由挂载 / lifespan）；逻辑在 `stocksdk/` 各子模块。
- 测试用桩替换 SDK（见 `tests/conftest.py`），不触发真实登录/网络；当前覆盖率约 88%。

## 多机 / 多 Agent 协同（本阶段：Git + 本页 + handoff 文件，无 SSH/Agent-RPC）

- **本地 Agent 指挥服务器侧 Agent** = 往 `ops/handoff/inbox/` 写任务文件并 commit；服务器侧 Agent `pull` 后认领、做完移到 `ops/handoff/done/` 回写结论。协议见 [`ops/handoff/README.md`](ops/handoff/README.md)。
- **项目看板 / 进度** 在 `ops/board/`（纳入仓库，Obsidian 把 vault 指向同目录即可多机可见）。`.obsidian/` 本机 UI 配置不入库。
- **服务器侧 Agent 用 `git worktree`** 开独立工作区，避免与主工作区互相干扰。
- **中心仓库 remote 尚未选定**；确定后 `git remote add origin <地址>` 即接入。**任何 push 前先过零密钥检查**（diff 里无 token / 账号 / 内网 URL）。
- 运维全流程（启停 / 探活 / 自愈 / 冷启动 / 回滚 / 压测约束）见 [`docs/运维手册.md`](docs/运维手册.md)。
