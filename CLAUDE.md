# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

把两个 Windows-only、单会话的桌面股票数据 SDK（东方财富 **EMQuantAPI** 与同花顺 **iFinD**）包成可远程取数的服务，并把多厂商上游 MCP 聚合成本机一个网关。三件独立产物：

1. **REST + WebSocket 取数服务**（`app.py` + `stocksdk/`，端口 8000）—— 别的项目用 `ip:端口 + 参数` 取数，不写 SDK 代码。当前接**四源**（EM、iFinD、Wind、TDX）：EM/iFinD 真机已用；**第三源 Wind（WindPy）`/wind/*` 路由已实现并桩测全绿，真机环境已打通**（实现与登录踩坑见 [`.claude/plans/wind-windpy-integration.plan.md`](.claude/plans/wind-windpy-integration.plan.md)）；**第四源 TDX（通达信 TQ/TdxQuant）`/tdx/*` 路由已实现、桩测全绿、真机端到端已验证**（见架构要点「通达信 TDX 接口」）。
2. **MCP 聚合网关**（`mcp_gateway/`，端口 8765）—— 把上游厂商 MCP 中转给远程标准 MCP 客户端，上游凭据只存本机。
3. **生产压测工具**（`loadtest/`）—— 验证崩溃自愈、并发承载、WS 长稳。

公网暴露通过 ngrok（一个 agent 同时暴露 8000 + 8765）。文档在 `docs/`（含 MCP 中转网关、iFinD 字段字典等）。

### 🔴 定位边界（别搞混两个仓库）

**本仓库以「数据提供方」为主：EM/iFinD/Wind 三源只读取数、不下单、不交易。** 消费方曾是**另一个仓库 STS-codex**（交易系统，本机不存在）。

> ⚠ **定位更新（2026-06-26）**：经用户决策，**新增本机交易能力**——君弘君智（迅投 QMT/XtQuant）`/qmt/*` 路由直接做进本服务（详见架构要点「QMT 交易接口」）。交易**默认关**（`QMT_TRADING_ENABLED=false`）、下单**默认 dry-run**、过四道护栏、写审计；EM/iFinD/Wind 仍维持只读，Wind 的 `torder` 等仍 403 硬拦截。「下单只走 STS-codex / signal-submit」的旧红线在交易腿并入本仓库后已被此决策覆盖。

`docs/数据激活.md`（数据源激活手册）里的 `trading-system` CLI、SQLite、source-priority resolver **全部属于 STS-codex，不在本仓库实现**。本仓库对它只负责两件事：① 把数据取出来；② 用 [`docs/数据源对照-StockSDK提供.md`](docs/数据源对照-StockSDK提供.md) 说明「哪个字段走哪个端点」。看到要在本仓库实现 resolver / Choice provider 的需求，先回到这条边界确认。

## 多 venv 结构（关键，别搞混）

每个产物用独立的 Python 3.11.4 x64 venv，**互不共享 site-packages**：

| venv | 用途 | 依赖文件 |
|---|---|---|
| `.venv-em` | EM SDK（通过 `.pth` 引用 `D:\dev\Project\EMQuantAPI_Python\python3`，不复制进库） | `requirements-em.txt` |
| `.venv-ths` | iFinD SDK | `requirements-ths.txt` |
| `.venv-wind` | Wind SDK（WindPy，通过 `.pth` 引用 `C:\Wind\Wind.NET.Client\WindNET\x64`，不复制进库） | `requirements-wind.txt`（注释注册步骤，WindPy 不走 pip） |
| `.venv-api` | HTTP/WS 服务 + pytest + 压测 | `requirements-api.txt` |
| `.venv-mcp` | MCP 网关 | `requirements-mcp.txt` |

运行命令时**一律用 venv 内的 `Scripts\python.exe` / `pytest.exe` / `uvicorn.exe`**，不要用系统 Python。EM SDK 还需本机装 Microsoft Visual C++ 2010 可再发行组件包（x64）。

### Wind（WindPy）环境与登录（已实测打通；`/wind/*` 路由已实现，见 [`stocksdk/routes_wind.py`](stocksdk/routes_wind.py) 与 [`.claude/plans/wind-windpy-integration.plan.md`](.claude/plans/wind-windpy-integration.plan.md)）

Wind 是第三个**单会话/单点登录**桌面 SDK，接入方式与 EM/iFinD 同构（全局锁串行化 + 会话自愈三件套 `ensure_wind`/`wind_exec`/`_wind_session_dead`，会话失效码集 `{-2, -103, -40520004}`）。路由层 `/wind/*`：固定端点 `GET /wind/wsd`（日序列）、`GET /wind/wss`（日截面，均默认 `usedf=True`），透传 `POST /wind/call/{method}`、`GET /wind/methods`。**仅读取数、不做交易**——交易/写操作类（`tlogon/tlogout/torder/tcancel/tquery/wupf`）在 `routes_wind.py:_WIND_TRADING` 中**硬拦截 403**，遵循定位边界。`wsq` 实时为异步回调，HTTP 同步端点不暴露（`/wind/methods` 标注，实时推送后续仿 `routes_ws.py`）。

- **注册（一次性）**：装好 Wind 金融终端后，用官方脚本写 `.pth`（机制同 EM）：
  ```bat
  .venv-wind\Scripts\python.exe "C:\Wind\Wind.NET.Client\WindNET\bin\installWindPy.py" "C:\Wind\Wind.NET.Client\WindNET"
  ```
  之后 `from WindPy import w` 即可用。仅此一步不足以让 `w.start()` 连上终端（见下）。
- **🔴 登录踩坑链（冷启动必看，否则 `w.start()` 失败）**：
  1. `import` 成功但 `w.start()` 返回 **`-2 'Start Error!'`** → 终端侧 API 接口没修复。
     需在终端 **发现→API插件→修复Python接口**，【添加路径】指向 `.venv-wind\Scripts\python.exe`，
     **终端须管理员运行**（写注册表），且**修复时关掉所有 python 进程**（否则提示"python 正在使用中"）。
  2. 修复后 `w.start()` 返回 **`-40520004 'Login Failed!'`** → Wind 进程脏状态/多实例锁冲突。
     **管理员任务管理器杀光全部 Wind 进程**（`WBox.exe`/`WIM.exe`/`wimbrowser.exe`/`WindUpdate.RUN` 等，
     真正持锁的是 `WBox.exe`/`WIM.exe`，`wmain.exe` 只是前台窗口）→ **重开终端登录** → `w.start()` 出 `0 ['OK!']`。
  3. 同 EM/iFinD：服务用的 Wind 账号**别同时在别处登录/跑 WindPy**，单点会冲突。
- **返回结构（写 `serialize` 用）**：`wsd/wss` 返回 `WindData`（`.ErrorCode/.Codes/.Fields/.Times/.Data`，
  **`.Data` 字段优先**：`Data[i]`=第 i 个 Field 跨所有 Times 的序列，转 records 需转置）；
  **`usedf=True` 返回 `(ErrorCode, DataFrame)` 元组**（最省事路径）。**坏代码返回 `ErrorCode=0` + `Data=[[None,...]]`**，
  故失败判定**只看 `ErrorCode!=0`**。会话失效码集：`{-2, -103, -40520004}`。

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

### 通达信 TDX 接口（routes_tdx.py + sessions.py 的 ensure_tdx）

通达信 TQ（TdxQuant，官方 Python 量化框架）是**第四个数据源**，`/tdx/*` 与 `/em /ths /wind` 并列，**只读取数、不交易**（交易类硬拦 403，QMT 仍是唯一交易源）。接入要点：

- **运行时引入**：`tqcenter` 模块在通达信终端安装目录 `PYPlugins\sys` 下（默认 `config.TDX_DEFAULT_PYPLUGINS_DIR`，`TDX_PYPLUGINS_DIR` 可覆盖），依赖同目录 `TPyth*.dll`/`tdxrpc*.dll`。`sessions.py:_bootstrap_tdx_path()` 在 `from tqcenter import tq as tdx` 前用 `sys.path` + `os.add_dll_directory` 注入（机制同 QMT）。`tq` 是**类**，方法直接 `tdx.xxx()`。
- **会话模型**：同 EM/iFinD/Wind 的单会话取数 + 复用全局 `lock` 串行化。自愈三件套 `ensure_tdx`/`tdx_exec`/`_tdx_session_dead`：`ensure_tdx()` 调 `tdx.initialize(路径)`（终端未开/未登录抛 502）；失效判定 = 返回 `None` 或 dict `ErrorId!=0` 且消息含登录关键词；`tdx_exec` 还兜底 `except`（终端断连时 initialize 抛异常）重连重试一次。前提：本机通达信金融终端（64位）已开启登录、且已在「发现→API插件」修复 Python 接口。
- **端点**：固定只读端点 `GET /tdx/bars`（K线，dict-of-DataFrame）、`/tdx/snapshot`（五档快照）、`/tdx/stock_info`（基础财务）、`/tdx/financial`（专业财务 Fn 字段）、`/tdx/sector`（板块成分）、`/tdx/stock_list`（按市场取码）、`/tdx/trading_dates`（交易日历）；透传 `POST /tdx/call/{method}` + `GET /tdx/methods`。透传**硬拦三类 403**：交易类（`order_stock`/`cancel_order_stock`/`query_*`/`stock_account`）、写客户端类（`send_*`/板块增删改/`download_file`）、会话类（`initialize`/`close`）。`subscribe_hq` 异步推送 HTTP 不暴露（后续可仿 `routes_ws`）。
- **返回归一化**：`serialize.tdx_result`——dict 含 DataFrame 值（get_market_data）→每个转 records；扁平 dict（snapshot/stock_info）直返；`ErrorId!=0`→502；list 直返。**代码须标准格式（`600519.SH`），日期 `YYYYMMDD`**（与前三源 `YYYY-MM-DD` 不同）。🔴 下单常量与 QMT 不同（TQ `tqconst.STOCK_BUY=0/SELL=1`、`PRICE_MY=0`；QMT 是 23/24/11），但本源不交易，仅记录备忘。
- **官方文档**：`docs/catalog/tdx/_raw/TdxQuant接口说明文档.pdf`（231页）+ 抽出的 `tdxquant_doc.txt`，所有端点字段口径/签名据此实现。

### QMT 交易接口（routes_qmt.py + sessions.py 的 ensure_qmt）

君弘君智（迅投 QMT/XtQuant）是本服务**唯一交易源**，`/qmt/*` 与 `/em /ths /wind` 并列。接入要点：

- **运行时引入**：xtquant 原生 pyd 含 cp311，在 `.venv-api` 直接用。中文安装路径在 `.pth` 里按本地编码读不可靠，故 `sessions.py:_bootstrap_xtquant_path()` 在导入前用 `sys.path` + `os.add_dll_directory(bin.x64)` 注入（默认路径见 `config.QMT_DEFAULT_PACKAGE_DIR`，`QMT_PACKAGE_DIR` 可覆盖）。
- **会话模型**：不同于三源的无状态取数，QMT 是长连接 trader + 异步回调。`ensure_qmt()` 建单例 `XtQuantTrader` 并 `start/connect/subscribe`，复用全局 `lock` 串行下单；回调（`_QmtCallback`）只把委托/成交/错误**入队** `_qmt_events`，**回调线程内绝不调 `query_*`**（否则后续回调卡死）。前提：本机 `XtMiniQmt.exe` 已登录（极简/独立模式），`connect()!=0` → 502。
- **端点**：读 `GET /qmt/asset|positions|orders|trades|events|health`；写 `POST /qmt/order|/qmt/cancel`；透传 `POST /qmt/call/{method}` + `GET /qmt/methods`。透传**硬拦交易类**（`order_stock*`/`cancel_*` 必须走带护栏端点）与会话/底层类（`start/stop/connect` 等会断服务连接）。**行情**另有 `/qmt/data/*`（xtdata：`kline/tick/sector/trading_dates/instrument/download/call/methods`），与交易独立、不受交易开关限制；但行情与三源（EM/iFinD/Wind）重复，仅在需要 QMT 专有 tick/L2 时用。
- **三层安全**（服务经 ngrok 公网，交易端点也公网）：① 交易总开关 `QMT_TRADING_ENABLED` 默认 **false**，写操作 503；② `/qmt/order` 默认 **dry-run** 只回显，`confirm=true` 才真发；③ `guards.py` 四道护栏（单笔金额上限/标的白名单/当日笔数/交易时段）+ 全量审计 `audit/*.jsonl`（gitignore）。买卖/价位走 `xtconstant`（`STOCK_BUY=23`/`STOCK_SELL=24`、`FIX_PRICE=11`、`LATEST_PRICE=5` 配 `price=-1`）。
- **返回归一化**：`serialize.qmt_asset/qmt_position/qmt_order/qmt_trade`（字段对照 `xtquant/xttype.py`）；`order_stock` 返回 `-1`→502，`cancel_order_stock` 返回 `-3`未登录等负值→409。

### 安全（security.py / ratelimit.py）

服务经 ngrok 公网暴露，鉴权/限流为必需。`X-API-Key` 常量时间比较（`secrets.compare_digest`）；按 IP 滑动窗口限流（默认 `60 次/60s`，见 `config.py` 常量）。框架无关原语在 `ratelimit.py`，供网关复用同一份逻辑避免漂移；`security.py` 只做 FastAPI 适配。未配 `API_KEY` 时不鉴权（仅本机/内网），启动时 warning。

### 字段字典抓取（scripts/catalog/ + docs/catalog/，与运行时服务无关）

给消费方做产品/接口设计用的**全量指标字段字典**（≠ 运行时取数）。两家 SDK 都**无全量字典枚举接口**（实测：`THS_DataPool/ReportQuery/EDBQuery` 都是「给代码取数」，字典在加密的 `excel.xml`），唯一可行路径是**各家官网「命令生成器」的后台 JSON 接口**：

- **EM**：`quantapi.eastmoney.com`，已抓 18512 字段（css 11823 + csd 570 + ctr 6119）→ `docs/catalog/em/*.csv` + `东方财富EM指标字段手册.md`。
- **iFinD**：`quantapi.51ifind.com`，已抓 22940 指标 / 13 品种 → `docs/catalog/ths/{品种}_indicators.csv` + `同花顺iFinD指标字段手册.md`。
- **🔴 iFinD 抓取的两个反直觉坑**（踩过，别重走）：① **不是 IP 封**——同 IP 用 curl 打登录端点正常,只有**自动化浏览器(CDP)被反爬拦**;普通浏览器正常。② **session 绑登录浏览器**——cookie 搬到服务器 curl 报 `-1010 已登出`,故抓取**必须在用户已登录的普通浏览器 Console 就地 fetch**。
- **工具链**：`ifind_crawl.js`（浏览器爬虫,递归 `list_by_seq?seq=&type=` 指标树）→ `parse_ifind.py`（JSON→CSV 去重）→ `gen_md_ifind.py`（CSV→手册）。70MB 原始 JSON 在 `docs/catalog/_raw/`（已 gitignore）。说明见 `docs/字段清单说明.md`，记忆见 `ifind-catalog-webapi-breakthrough`。
- **未完成**：Wind 字段字典仍空白（本机可做、不卡 IP，待 spike）。

> **Wind 更新（2026-06-30）**：Wind 与前两家不同，**无公网命令生成器**，且**有三套字段口径别混用**。全量字典加密锁在本地终端，五条路实测全堵（公网帮助中心 `wx.wind.com.cn` 只放函数手册、本机终端不开 TCP 端口、SPA 不含树、CDP 调试端口被屏蔽、`Indicator.xml`/`wind_IndicatorTree.dat` 加密仅 DLL 可解、`w.menu()` 回调是 GUI 接口 headless 推 0 条）。**取数突破口=Excel 插件 `DataBrowse/XLA/*.xla`**（OLE2）：`WindFunc.xla`(7.4MB,9698 码) + `WindFunc_s.xla`(22MB,7887 码;需修 OLE2 DIFAT 截断 bug 才完整解出),并集 **10069 个 Excel 插件口径字段**（脚本 `extract_wind_xla2.py`,产出 `xla_fields*.csv` + `Wind指标字段手册.md`)。⚠ **三套口径**：① **WindPy 实测可用 5359 个**（`close`/`pe_ttm`/`roe`，**可直接喂 `/wind/wsd|wss`**）= `docs/catalog/WindPy字段手册.md`（`windpy_fields.csv`，脚本 `wind_verify_xla_fields.py`+`gen_md_windpy.py`）；② **Excel 插件 xla 并集 10069 个**（`s_dq_close`，**仅查中文名/找指标，不能直接喂 wss**）；③ 探测子集 130（已并入①）。**5359 = 并集 10069 码生「原码+渐进去前缀」变体（28327 个）批量喂 wss、按 `-40522006`（纯名级校验，与品种无关）二分定位得到,已饱和（候选 9698→10069 仅 +58）**——`wsd`/`wss` 共用同一字段字典,WindPy 字段就 ~5350 量级,非"少一个数量级"（EM 1.85万含专题报表 ctr、iFinD 2.29万跨 13 品种重复计;Wind 是去重统一名空间）。死路与坑见记忆 `wind-catalog-probe-approach`。

## 约定

- **凭据一律从 `.env` / 环境变量读**，无硬编码。`config.load_dotenv` 用 `setdefault`（真实环境变量优先）。`.env` / `userInfo` / `*.log` 已 gitignore。配置模板见 `.env.example`。
- `stocksdk/config.py` 只依赖标准库，各 venv 都能导入；魔法数字（端口、队列上限、限流阈值、重启间隔）集中在此，**不要散落硬编码**。
- `app.py` 仅负责装配（CORS / 路由挂载 / lifespan）；逻辑在 `stocksdk/` 各子模块。
- 测试用桩替换 SDK（见 `tests/conftest.py`），不触发真实登录/网络；当前覆盖率约 88%。

## 多机 / 多 Agent 协同（本阶段：Git + 本页 + handoff 文件，无 SSH/Agent-RPC）

- **本地 Agent 指挥服务器侧 Agent** = 往 `ops/handoff/inbox/` 写任务文件并 commit；服务器侧 Agent `pull` 后认领、做完移到 `ops/handoff/done/` 回写结论。协议见 [`ops/handoff/README.md`](ops/handoff/README.md)。
- **项目看板 / 进度** 在 `ops/board/`（纳入仓库，Obsidian 把 vault 指向同目录即可多机可见）。`.obsidian/` 本机 UI 配置不入库。
- **服务器侧 Agent 用 `git worktree`** 开独立工作区，避免与主工作区互相干扰。
- **中心仓库 remote 尚未选定**；确定后 `git remote add origin <地址>` 即接入。**任何 push 前先过零密钥检查**（diff 里无 token / 账号 / 内网 URL）。
- 运维全流程（启停 / 探活 / 自愈 / 冷启动 / 回滚 / 压测约束）见 [`docs/运维手册.md`](docs/运维手册.md)。

## 精简实盘版 v3 (2026-06-26 Coco经MCP同步)

- **① 项目定位收敛**：从「大而全数据平台」转向**精简实盘版**。主流程 5 支柱串行：**S1 资金异动挖掘 → S2 业务实质验证 → S3 精研关注池 → S4 盘中 14:30 信号 → S5 卖出**。旧版（大而全）以 `v1-full-system` 备份留存，不删。
- **② 我 Cody 的职责 = 轨 B 数据地基主力**：
  - 补**牛市段历史数据**（起点 **2024-09-14**）的日线 + 财务；
  - 跑通 **iFinD 原始接口**（生产主路径，量级 **6 亿/月**）；
  - **数据核验**；
  - **接口挂了实时修**（数据地基稳定性由我兜底）。
- **③ 多 Agent 协同分工**：
  - **业务实质验证（S2）**：Abby（Gemini 3.1 Pro）+ Dex + Coco **并行**产出，最后由 **Coco 汇总去重**。
  - **建模 / 回测**：Abby（Opus 4.6 Thinking）+ Dex + Coco **共同**产出，由 **Coco 整合**。
- **④ 数据铁律（来源优先级与取数约定）**：
  - 来源优先级：**iFinD > Choice > Tushare > AKShare > 网页端**。
  - **北向资金日度 2024-08 已停发** → 改用**南向 / 两融 / 持股变动**替代口径。
  - **iwencai（问财）查询必带明确日期**，否则自然语言解析失败。
  - **主营构成**：`get_stock_financials` 仅返回 **Top5**；要**全量**走 **EM 的 `MBSALESCONS`**。主题须**挂在真实业务收入占比**上，**单股各主题占比之和 = 100%**。
- **⑤ 红线（不可逾越）**：
  - **`API_KEY` 走 env**，不入库、不打印；
  - ~~不碰本地交易核心~~ / ~~以只读取数为主~~ / ~~唯一下单路径 = `signal-submit`，不自动下单~~ —— **已于 2026-06-26 经用户决策放宽**：交易腿（君弘君智 QMT `/qmt/*`）并入本仓库，见上「QMT 交易接口」。替代约束：**交易默认关（`QMT_TRADING_ENABLED=false`）、下单默认 dry-run、必过四道护栏、全量审计**，公网放开交易前需显式确认。
