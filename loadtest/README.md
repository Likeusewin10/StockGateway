# 生产实践测试（loadtest/）

对已上线的两套服务做生产条件验证：**会不会自动崩溃重启**、**能扛多少并发**、
**WebSocket 长连接稳不稳**。不改动任何生产取数/会话/路由逻辑，只新增本目录工具。

> 统计原语在 `_common.py`（纯函数，有单测 `tests/test_loadtest_harness.py`）。
> 端口/限流/队列阈值一律从 `stocksdk.config` 读，绝不写死。

## 先认清架构（决定数字怎么解读）

| 事实 | 含义 |
|---|---|
| 两套 SDK 单会话、单点登录，强制**单 worker** | 不能用 `--workers` 扩容 |
| 所有取数 `with lock:` 全局串行（`stocksdk/sessions.py`） | **并发≠并行取数**；取数端点吞吐不随并发翻倍、延迟随并发线性上升，是**设计预期，不是缺陷** |
| `/health` 不持锁、不吃限流 | 用它压「连接处理/排队能力」最干净，零 SDK 配额消耗 |
| 每 IP `60 次 / 60s` 限流（`config.py`） | 单机直压取数端点第 61 个就 429——测的是限流不是承载 |
| 看门狗 5s 重启（`start_server.bat`） | 崩溃自愈第一层 |
| 计划任务每分钟兜底 + RestartOnFailure×999（`register_task.ps1`） | 崩溃自愈第二层 |

## 前置

1. 服务已在 8000 运行（`start_server.bat` 或已注册的计划任务 `StockDataService`）。
2. 依赖在 `.venv-api`：`pip install -r requirements-api.txt`（含 `psutil`）。
3. **一律用 `.venv-api\Scripts\python.exe` 运行**（它的 site-packages）。
4. ⚠ **别用 Git-Bash 直接跑**：它会把 `--target /health` 转义成 Windows 路径，
   导致全部请求连接失败。用 `cmd`，或设 `MSYS_NO_PATHCONV=1`。脚本已加预检会
   拦住这种情况。

## 三类测试

### 1. 并发承载
```cmd
.venv-api\Scripts\python.exe loadtest\concurrency.py --target /health --concurrency 1,4,16,64 --duration 15
```
输出每档 p50/p95/p99 + 吞吐，落 `results/concurrency.csv`。
- `/health` 吞吐**应随并发上升**直到单 worker 事件循环饱和后趋平、延迟上升。
- 想看**取数端点**的真实串行排队，又不想打真 SDK / 撞限流：临时挂一个 sleep
  mock 端点压它（生产端点受限流，直压会变成测限流）。
- 脚本检测到 429 占比 >5% 会告警「你测到的是限流而非承载」。

### 2. 崩溃自愈
```cmd
REM 层一：杀 uvicorn 子进程，验看门狗 ~5s 拉起
.venv-api\Scripts\python.exe loadtest\crash_recovery.py --layer watchdog

REM 层二：连看门狗 cmd 一起杀，验计划任务 1 分钟兜底（需已注册任务）
.venv-api\Scripts\python.exe loadtest\crash_recovery.py --layer task
```
按**监听端口**精确定位 PID 后强杀（不按进程名，避免误伤 8765 网关），轮询
`/health` 量化恢复秒数。层二未注册计划任务时自动 SKIP。

### 3. WebSocket 长稳 / 背压
```cmd
.venv-api\Scripts\python.exe loadtest\ws_soak.py --path /ths/ws --codes 300033.SZ --indicators latest --connections 16 --duration 180
```
开 M 路订阅跑若干分钟，统计收包速率、断连、是否触发每连接 1000 条队列上限
（`WS_QUEUE_MAXSIZE`）、服务 RSS 漂移。
- EM(`/em/ws`)若账号无 csq 行情权限会返回 error 事件，属已知；换 `/ths/ws` 验推送链路。
- **RSS 告警的已知噪声**：短测（采样次数少）时首次订阅会触发 SDK 懒加载，RSS
  一次性抬高，会误报「漂移」。看趋势请跑 ≥3 分钟、关注是否**单调上涨**而非单次跳变。

### 一键全跑
```cmd
loadtest\run_all.bat
```

## 已验证的实测结果（本机基线）

| 测试 | 结果 |
|---|---|
| 并发 `/health` 1→8 | 吞吐 259 → 502 req/s（随并发上升） |
| 并发 `/health` 8→32 | 吞吐 ~500 req/s 趋平、p50 16→63ms（单 worker 饱和，符合预期） |
| 崩溃自愈（看门狗层） | kill 后 **6.1s** 恢复（预算 15s）✓ |
| WS `/ths/ws` 4 路 10s | 4/4 订阅成功、0 断连 |

> 绝对吞吐随机器/网络而变，趋势（随并发上升后趋平、自愈秒数）才是判读重点。

## 工具自测
```cmd
.venv-api\Scripts\pytest.exe tests\test_loadtest_harness.py -q
```
统计/分类/CSV 纯函数单测，保证压测工具本身可信。
