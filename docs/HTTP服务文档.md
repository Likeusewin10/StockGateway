# 股票数据 HTTP 服务

把 EM（东方财富）和 iFinD（同花顺）两个 SDK 包成一个 HTTP 服务。
**其他项目无需写任何 SDK 代码，只要往 `http://本机IP:端口/...` 发请求 + 带参数，即可取数。**

## 启动

### 常驻服务（推荐，开机/登录后自动运行）

双击运行 `install_service.bat`，注册为计划任务 `StockDataService`：
- **登录后自动启动**（你登录 Windows 桌面后服务自动起来）。
- **崩溃自动重启**：`start_server.bat` 是看门狗循环，服务进程退出后 5 秒内自动重启。
- 停用/卸载：运行 `uninstall_service.bat`。
- 手动立即启动：`schtasks /Run /TN StockDataService`；查看状态：`Get-ScheduledTask -TaskName StockDataService`。

> 注意：用的是"登录后启动"。开机停在锁屏、尚未登录时服务不跑；登录进桌面即自动启动。
> 这样服务以你自己的账户运行，EM 的 userInfo 令牌可正常使用。

### 临时手动启动（调试用）

```bat
.venv-api\Scripts\python -m uvicorn app:app --host 127.0.0.1 --port 8000
```
- 两个 SDK 装在同一个 venv（`.venv-api`），一个服务、一个端口同时提供两家数据。
- **必须单 worker**（SDK 单会话，服务内部用全局锁串行化请求）。不要加 `--workers`。

## 访问

- 仅本机：`http://127.0.0.1:8000`（服务绑定 127.0.0.1，同网段其他设备访问不到）
- **交互式文档（可直接点着试）**：`http://127.0.0.1:8000/docs`

## 鉴权（API Key）

`.env` 里设了 `API_KEY` 后，**所有取数接口都要求请求头 `X-API-Key` 匹配**，否则返回 401。
`/health` 不需要 key（方便探活）。`.env` 里 `API_KEY` 留空则不鉴权（纯本机时）。

```bash
# 无 key → 401；带正确 key → 200
curl -H "X-API-Key: 你的KEY" "http://127.0.0.1:8000/em/csd?codes=300059.SZ&indicators=CLOSE&startdate=2024-01-02&enddate=2024-01-03"
```
```python
import requests
requests.get("http://127.0.0.1:8000/em/csd",
             headers={"X-API-Key": "你的KEY"},
             params={"codes":"300059.SZ","indicators":"CLOSE",
                     "startdate":"2024-01-02","enddate":"2024-01-03"})
```

## 远程调用（本机无公网 IP，用 Tailscale）

本机在路由器 NAT 后面、没有公网 IP，**不能直接被外网访问**。
对"固定一个人、跨网络"的场景，用 **Tailscale**（VPN）最合适：不暴露公网、不依赖公网 IP、CGNAT 也能用、一个人免费。

步骤：
1. 这台机器和远程设备都安装 Tailscale（https://tailscale.com/download），用同一账号登录，加入同一 tailnet。
2. 在这台机器上执行 `tailscale ip -4` 查到它的虚拟内网地址（形如 `100.x.x.x`，固定不变）。
3. 让服务监听 Tailscale 网卡。两种做法：
   - 简单：把 `start_server.bat` 里的 `--host 127.0.0.1` 改成 `--host 0.0.0.0`（监听所有网卡，含 Tailscale）。此时**务必已设 `API_KEY`**，因为同局域网也能访问到。
   - 收紧：`--host 100.x.x.x`（只监听 Tailscale 地址），但该地址变动时要改。推荐前者 + API Key。
4. 远程设备访问 `http://100.x.x.x:8000/...`，请求头带 `X-API-Key`。

> 安全要点：远程开放后**必须有 API Key**（已内置）。Tailscale 只让你 tailnet 内的设备可达，双重保险。
> 备选方案（不展开）：内网穿透 frp/ngrok（数据过第三方中转，慎用）、云服务器反向代理（要花钱、最稳定）。

## 接口一览

所有接口都是 GET，参数走查询字符串，返回 JSON。

| 接口 | 说明 | 必填参数 |
|---|---|---|
| `/health` | 健康检查 | 无 |
| `/em/csd` | 东财序列数据 | `codes` `indicators` `startdate` `enddate`（可选 `options`） |
| `/em/css` | 东财截面数据 | `codes` `indicators`（可选 `options`，如 `TradeDate=20240105`） |
| `/ths/history` | 同花顺历史行情 | `codes` `indicators` `begin` `end`（可选 `params`） |
| `/ths/basic` | 同花顺基础/截面 | `codes` `indicators`（可选 `params`） |
| `/ths/realtime` | 同花顺实时行情 | `codes` `indicators`（可选 `params`） |

参数约定：
- EM：`codes`/`indicators` 多个用逗号，日期 `YYYY-MM-DD`。
- iFinD：`codes` 多个用逗号，`indicators` 多个用**分号**，日期 `YYYY-MM-DD`。

## 调用示例

浏览器/curl：
```
http://127.0.0.1:8000/em/csd?codes=300059.SZ&indicators=CLOSE&startdate=2024-01-01&enddate=2024-01-05
http://127.0.0.1:8000/em/css?codes=300059.SZ,000002.SZ&indicators=OPEN,CLOSE&options=TradeDate=20240105
http://127.0.0.1:8000/ths/history?codes=300033.SZ&indicators=open;close&begin=2024-01-01&end=2024-01-05
```

其他项目里（任意语言，这里以 Python 为例，**消费端不依赖任何股票 SDK**）：
```python
import requests
r = requests.get("http://127.0.0.1:8000/em/csd", params={
    "codes": "300059.SZ", "indicators": "CLOSE",
    "startdate": "2024-01-01", "enddate": "2024-01-05",
})
print(r.json())
# [{"CODES":"300059.SZ","DATES":"2024/01/02","CLOSE":13.8}, ...]
```

## ⚠️ 安全与限制

- **无鉴权**：按你的要求未加鉴权，知道 ip:端口的人都能调，等于用本账号额度。**仅限内网，不要暴露到公网。**
- **账号授权**：两个账号大概率是个人授权，多人共享可能违反服务协议（被封号风险）。建议先与客户经理确认是否允许内部 API 共享。
- **限频/流量**：EM 截面/序列每分钟 ≤700 次，且按品种有流量额度（官网 `/Flow` 查）；iFinD 单点登录。多人同时调容易打满。
- **单点登录**：iFinD 账号同时只能一处登录，本服务占用该登录位；别处再登会互相挤掉。

## 故障排查

- 启动后 `/health` 不通：看是否端口被占（`netstat -ano | findstr :8000`），或被其他 Python 占用——确认启动用的是 `.venv-api`。
- 接口报 502：多为 SDK 登录失败或取数无权限/流量用尽，错误信息里带原始错误码。

