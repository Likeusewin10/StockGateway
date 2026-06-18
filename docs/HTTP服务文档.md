# 股票数据 HTTP 服务

把 EM（东方财富）和 iFinD（同花顺）两个 SDK 包成一个 HTTP 服务。
**其他项目无需写任何 SDK 代码，只要往 `http://本机IP:端口/...` 发请求 + 带参数，即可取数。**

## 启动

在本机（`D:\dev\Project\StockSDK`）双击 `start_server.bat`，或命令行：
```bat
.venv-api\Scripts\python -m uvicorn app:app --host 0.0.0.0 --port 8000
```
- 两个 SDK 装在同一个 venv（`.venv-api`），一个服务、一个端口同时提供两家数据。
- **必须单 worker**（SDK 单会话，服务内部用全局锁串行化请求）。不要加 `--workers`。

## 访问

- 本机：`http://127.0.0.1:8000`
- 局域网同事：`http://192.168.0.88:8000`（本机当前内网 IP，换网络会变）
- **交互式文档（可直接点着试）**：`http://192.168.0.88:8000/docs`

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
http://192.168.0.88:8000/em/csd?codes=300059.SZ&indicators=CLOSE&startdate=2024-01-01&enddate=2024-01-05
http://192.168.0.88:8000/em/css?codes=300059.SZ,000002.SZ&indicators=OPEN,CLOSE&options=TradeDate=20240105
http://192.168.0.88:8000/ths/history?codes=300033.SZ&indicators=open;close&begin=2024-01-01&end=2024-01-05
```

其他项目里（任意语言，这里以 Python 为例，**消费端不依赖任何股票 SDK**）：
```python
import requests
r = requests.get("http://192.168.0.88:8000/em/csd", params={
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
