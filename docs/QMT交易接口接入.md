# 君弘君智（QMT / XtQuant）交易接口接入

> 本文档记录把**国泰海通 君弘君智（迅投 QMT）**的下单/查询能力并入 StockSDK（端口 8000）的全过程、配置与现状。
> 接入日期：2026-06-26。代码已交付并桩测全绿；真机待券商开通「独立交易」权限后即可用。

## 1. 背景与定位变更

- StockSDK 原定位「只读取数」（EM/iFinD/Wind 三源）。经用户决策，**新增本机交易能力**：
  君弘君智（= 迅投 QMT，各券商换皮，国君叫「君弘君智」）的 `xtquant` Python 库本机已装，
  直接做进本服务，暴露 `/qmt/*`，与 `/em /ths /wind` 并列。
- **EM/iFinD/Wind 仍只读**；Wind 的 `torder` 等交易函数仍 403 硬拦截。QMT 是**唯一交易源**。
- 详细方案见 [`.claude/plans/guotai-qmt-execution.plan.md`](../.claude/plans/guotai-qmt-execution.plan.md)。

## 2. 为什么是 QMT 而不是普通君弘 / PTrade

- **普通君弘 App / 客户端（D:\Softwares\GTJAJH）**：纯图形界面手动下单，**无个人 API**，不可程序化。
- **PTrade（恒生）**：另一套券商量化平台，**本机未安装**；且运行在券商机房内网、默认无外网，喂信号要走文件上传，
  对「本地算信号→本地下单」的现有架构不如 QMT 顺手。
- **君弘君智（QMT/XtQuant，D:\Softwares\君弘君智交易系统）**：**本地运行 + 可联网 + 自带 Python 库**，本机已装，故选它。

## 3. 本机安装事实（已核实）

| 项 | 值 |
|---|---|
| QMT 安装根 | `D:\Softwares\君弘君智交易系统` |
| xtquant 包目录 | `D:\Softwares\君弘君智交易系统\bin.x64\Lib\site-packages\xtquant` |
| 原生 pyd 版本 | cp36/37/38/39/310/**311** 全编（故可在 `.venv-api` 的 Python 3.11 直接 import） |
| userdata_mini | `D:\Softwares\君弘君智交易系统\userdata_mini`（账号子目录登录后才生成） |
| miniQMT 本体 | `bin.x64\XtMiniQmt.exe`、`bin.x64\XtItClient.exe` |
| 自带 Python | `bin.x64\python.exe`（3.6.8，本接入未用，走 .venv-api 3.11） |

## 4. 代码改动（全部在 stocksdk/，并入现有服务）

| 文件 | 说明 |
|---|---|
| `stocksdk/routes_qmt.py`（新） | `/qmt/*` 路由：health/asset/positions/orders/trades/events/order/cancel/call/methods |
| `stocksdk/guards.py`（新） | 下单四道护栏：单笔金额上限 / 标的白名单 / 当日笔数 / 交易时段 |
| `stocksdk/sessions.py` | `_bootstrap_xtquant_path()` 注入路径 + `ensure_qmt()` 单例 trader + `_QmtCallback` 回调入队 + 复用全局 `lock` |
| `stocksdk/serialize.py` | `qmt_asset/qmt_position/qmt_order/qmt_trade` + 错误码→HTTP（下单 `-1`→502；撤单 `-3` 等负值→409） |
| `stocksdk/config.py` | QMT 配置读取（全部走 `.env`，实时读便于按请求生效） |
| `app.py` | `include_router(routes_qmt.router)` |
| `tests/conftest.py` + `tests/test_routes_qmt.py` | XtQuant 桩 + 21 用例 |
| `.env.example` / `CLAUDE.md` / `.gitignore` | 配置模板、定位说明、`audit/` 忽略 |

### 4.1 xtquant 引入方式（关键踩坑）

- 不能靠 `.pth`：包目录是**中文路径**（君弘君智），`site.py` 按本地编码读 `.pth` 不可靠，导致 `ModuleNotFoundError`。
- 改为在 `sessions.py` 导入 xtquant **之前**显式注入：
  ```python
  sys.path.append(包目录)
  os.add_dll_directory(bin.x64)   # cp311 pyd 依赖 bin.x64 下的 DLL
  ```
  默认路径见 `config.QMT_DEFAULT_PACKAGE_DIR`，可用 `QMT_PACKAGE_DIR` 覆盖。已实测真机 `import app` 成功。

### 4.2 会话模型（与三源不同）

- EM/iFinD/Wind 是无状态取数；QMT 是**长连接 trader + 异步回调**。
- `ensure_qmt()` 建单例 `XtQuantTrader(userdata, session_id)` → `start/connect/subscribe`，复用全局 `lock` 串行下单。
- `connect()!=0` → 502（终端未登录）。回调 `_QmtCallback` 只把委托/成交/错误**入队** `_qmt_events`，
  **回调线程内绝不调 `query_*`**（否则后续回调卡死）；查询端点直接走 `query_stock_*`（权威值）。

## 5. 配置（.env）

| 变量 | 必填 | 说明 |
|---|---|---|
| `QMT_TRADING_ENABLED` | — | 交易总开关，默认 `false`（关时写操作 503） |
| `QMT_ACCOUNT_ID` | ✅ | 资金账号（君弘客户端/登录框可见；登录后 userdata_mini 下生成同名目录） |
| `QMT_USERDATA_PATH` | ✅ | `D:\Softwares\君弘君智交易系统\userdata_mini` |
| `QMT_ACCOUNT_TYPE` | — | 默认 `STOCK`；两融填 `CREDIT` |
| `QMT_SESSION_ID` | — | 默认 100（单 worker 固定即可） |
| `QMT_PACKAGE_DIR` | — | 默认指向本机安装路径，换机改这里 |
| `QMT_MAX_NOTIONAL` | — | 单笔金额上限，默认 50000 |
| `QMT_DAILY_ORDER_CAP` | — | 当日笔数上限，默认 50 |
| `QMT_CODE_WHITELIST` | — | 标的白名单（逗号分隔），空=不限 |
| `QMT_ALLOW_OFFHOURS` | — | 非交易时段是否放行，默认 false |

## 6. 端点与调用（带 `X-API-Key`，与现有接口同构）

```
GET  /qmt/health                  连接状态 {connected, account}
GET  /qmt/asset                   资金 {cash,frozen_cash,market_value,total_asset}
GET  /qmt/positions               持仓列表
GET  /qmt/orders?cancelable=0|1   委托列表
GET  /qmt/trades                  成交列表
GET  /qmt/events                  最近交易回调 + 当日下单计数
POST /qmt/order                   下单（默认 dry-run，confirm=true 才真发）
POST /qmt/cancel                  撤单（默认 dry-run）
POST /qmt/call/{method}           透传只读类方法（交易/会话类硬拦 403）
GET  /qmt/methods                 方法清单 + 标注
```

下单请求体：
```json
{"side":"buy|sell","stock_code":"600000.SH","volume":100,
 "price_type":"limit|latest","price":10.5,"strategy":"sts","remark":"","confirm":false}
```
curl 样例：
```bash
curl -H "X-API-Key: <key>" http://127.0.0.1:8000/qmt/health
curl -H "X-API-Key: <key>" http://127.0.0.1:8000/qmt/asset
curl -X POST -H "X-API-Key: <key>" -H "Content-Type: application/json" \
  -d '{"side":"buy","stock_code":"600000.SH","volume":100,"price_type":"limit","price":10.5}' \
  http://127.0.0.1:8000/qmt/order        # 默认 dry_run 只回显
```

### 6.1 行情数据端点（xtdata，/qmt/data/*）

QMT 行情模块 `xtdata` 也已包入（与交易独立、**不受 `QMT_TRADING_ENABLED` 限制**）：

```
GET  /qmt/data/kline?codes=600000.SH&fields=close&period=1d&start=&end=&count=-1&dividend=none
GET  /qmt/data/tick?codes=600000.SH,000001.SZ          盘口最新 tick
GET  /qmt/data/sector?name=沪深A股                      板块成分股
GET  /qmt/data/trading_dates?market=SH                  交易日(毫秒戳)
GET  /qmt/data/instrument?code=600000.SH                合约详情
POST /qmt/data/download {code,period,start,end}         下载历史到本地缓存
POST /qmt/data/call/{method}                            透传 xtdata 只读方法(订阅/连接类 403)
GET  /qmt/data/methods                                  xtdata 方法清单
```
- 返回的 DataFrame/ndarray 经 `_jsonify_market` 转 JSON（`orient=split`，NaN→null）。
- ⚠ 注意：**行情数据已有 EM/iFinD/Wind 三源**，QMT 行情属补充（如需 QMT 的 tick/Level-2 等）。
- 🔑 **行情可能不需「独立交易」权限**：xtdata 连的是本机 QMT 数据服务，只要 **君弘君智正常登录在跑**就可能取到（数据权限 ≠ 交易权限）。值得先试 `curl /qmt/data/tick`——若通，则行情无需等独立交易权限，仅交易腿需要。

## 7. 三层安全（服务经 ngrok 公网，交易端点也公网）

1. `QMT_TRADING_ENABLED=false` 默认关 → `/qmt/order`、`/qmt/cancel` 返回 503。
2. `/qmt/order` 默认 **dry-run** 只回显 `would_send`，`confirm=true` 才真发单。
3. `guards.py` 四道护栏 + 全量审计 `audit/qmt-YYYYMMDD.jsonl`（已 gitignore）。
- 建议上线前再给 `/qmt/*` 写类加独立 key 或 IP 白名单；公网放开交易需显式确认。

## 8. 运行前提与真机现状（2026-06-26）

- **前提**：本机 miniQMT 以「独立交易 / 极简模式」登录（普通君弘界面登录**不会**起 XtQuant 服务）。
- **🔴 当前卡点：账号无 QMT 独立交易权限。** 实测勾「独立交易」登录提示「没有权限」、双击 `XtMiniQmt.exe` 也提示没权限。
  → 需联系**国泰海通客户经理**申请「君弘君智 QMT 独立交易 / XtQuant API 交易权限」
  （常见要求：普通柜台资金 ≥30 万、签《量化交易风险协议》、C4 风测、程序化交易报告）。
- **数据源现状**：EM ✅ / iFinD ✅ / Wind ✅，`/health/deep` 实测取数正常，均不受 QMT 权限影响。
- **QMT 现状**：`/qmt/health` 返回 `connected:false (connect()=-1)`；账户读（asset/positions/orders/trades）与下单**均需**权限开通后才能用。

## 9. 权限开通后的验证顺序

1. `.env` 确认 `QMT_ACCOUNT_ID` / `QMT_USERDATA_PATH`，重启服务。
2. 启动 miniQMT，以「独立交易/极简模式」登录该资金账号。
3. `curl /qmt/health` → 应为 `{"connected":true,"account":"..."}`。
4. `curl /qmt/asset`、`/qmt/positions` 验账户数据。
5. 设 `QMT_TRADING_ENABLED=true`，用 **1 手最小额限价单** 走通 `order`(confirm) → `/qmt/orders` → `/qmt/cancel`。
