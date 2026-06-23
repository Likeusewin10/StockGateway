# StockSDK 部署说明

两个股票数据 SDK 各自用独立的 Python venv（均为 Python 3.11.4 x64）。

## SDK 2：同花顺 iFinD（已跑通）

```bat
py -3.11 -m venv .venv-ths
.venv-ths\Scripts\activate
pip install -r requirements-ths.txt
python verify_ths.py
```

- 凭据来自 `.env`（`THS_USER` / `THS_PWD`），不入库、不硬编码。
- 注意：同花顺单点登录，勿在多处同时登录同一账号。

## SDK 1：东方财富 EMQuantAPI

SDK 文件位于 `D:\dev\Project\EMQuantAPI_Python\python3`（不复制进本项目，venv 通过 `.pth` 引用）。

```bat
py -3.11 -m venv .venv-em
.venv-em\Scripts\activate
:: 注册接口（在 venv 激活态下运行）
cd /d D:\dev\Project\EMQuantAPI_Python\python3
python installEmQuantAPI.py
cd /d D:\dev\Project\StockSDK
```

运行依赖：Microsoft Visual C++ 2010 可再发行组件包（x64，本机已装）。

### 激活（生成 userInfo 令牌，需绑定手机号的 Choice 账号）

运行图形激活工具，输入绑定手机号、获取验证码：

```
D:\dev\Project\EMQuantAPI_Python\python3\libs\windows\LoginActivator.exe
```

激活成功后生成 `userInfo` 令牌文件。然后：

```bat
.venv-em\Scripts\python verify_em.py
```

- 默认用 userInfo 令牌登录。
- 若想用账密登录（不生成令牌），在 `.env` 增加 `EM_USER` / `EM_PWD` 后再运行。

## 安全

- `.env`、`userInfo`、`docs/quantapi/相关信息.txt` 已被 `.gitignore` 排除，不入版本库。
- 代码一律从环境变量 / `.env` 读取凭据，无硬编码。
- HTTP 服务（经 ngrok 公网暴露）已加：`X-API-Key` 常量时间鉴权、按 IP 限流、默认拒绝跨域（`CORS_ORIGINS` 白名单显式放开）。

## HTTP 服务结构与测试

服务实现拆分在 `stocksdk/` 包：`config`（配置/`.env` 加载）、`sessions`（SDK 单会话+全局锁）、
`serialize`（返回值归一化）、`security`（鉴权/限流）、`routes_em` / `routes_ths` / `routes_ws`（路由）。
`app.py` 仅负责装配。

### 会话自愈与单点登录

SDK 单会话会被悄悄踢掉（同账号在别处登录挤掉、iFinD 单点登录冲突、令牌超时）。
服务通过 `sessions.em_exec`/`ths_exec` 在取数返回会话/登录失效码时**自动强制重登并重试一次**，
远程调用不再因此报"未登录/已登出"，无需手动重启。

为减少被挤：服务用的账号**不要**同时在桌面客户端或其他脚本登录同一账号；
iFinD 重登前会先 `Logout` 再 `Login` 抢回会话，EM 用 `ForceLogin=1` 抢登。

```bat
.venv-api\Scripts\python -m pytest --cov=stocksdk
```

测试用桩替换两个 SDK，不触发真实登录/网络（当前覆盖率 88%）。

## MCP 聚合网关（远程调用 iFinD MCP）

把多厂商上游 MCP 聚合为**本机一个** streamable-http 网关，让其他机器的标准 MCP 客户端
（Claude Code / Cursor）经 ngrok + `X-API-Key` 远程调用。上游厂商凭据（如 iFinD JWT）**只存本机，绝不下发**。

- 实现：`mcp_gateway/` 包 —— `providers`（多厂商注册表，加新厂商只改这里 + `.env`）、
  `upstream`（凭据收口）、`server`（mount 代理 + `http_app`）、`auth`（复用 `stocksdk/ratelimit` 的 Key 鉴权/限流）。
- 端口 8765，与 8000 的 REST 服务并存。`.venv-mcp` 独立依赖（`requirements-mcp.txt`）。
- 启动：`start_mcp_gateway.bat`；公网：`start_ngrok_gateway.bat`（一个 ngrok agent 同时暴露 8000+8765）。
- 远端只需在 `mcpServers` 加**一条**指向网关的配置，原 7 条 iFinD 直连收敛为 1 条。

详见 [`docs/MCP中转网关.md`](docs/MCP中转网关.md)（含远端配置样例、加新厂商三步、运维）。

```bat
.venv-mcp\Scripts\python -m pytest tests\test_mcp_gateway_auth.py tests\test_mcp_gateway_providers.py
```
