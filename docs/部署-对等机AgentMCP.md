# 对等机部署手册（丢给对等机上的 Claude Code 直接执行）

> **架构（2026-07 重构）**：对等机只跑一个**永不需要维护的 HTTP 哑执行小服务**
> `peer_service.py`（纯标准库、单文件、~400 行）。所有会演进的业务逻辑（命令模板、
> 会话、文件分块编排、将来的新工具）**全在 hub 侧**，对等机零感知。对等机侧从此只有：
> **系统 Python + claude CLI + `peer_service.py` + 两三行 `.env` + frp 隧道**。不需要 venv、
> 不需要 fastmcp、不需要克隆整个仓库、不需要跟 hub 的功能迭代同步代码。
>
> **执行者注意（给对等机上的 Claude Code）**：本文档是可自动执行的部署任务书。你在一台
> **对等机**上，目标是把本机部署成哑执行节点：对外暴露 `/health /exec /task /file /admin/*`
> HTTP 原语，经 frp 隧道让 hub 聚合调用（hub 侧注册为 `peer_<机器名>_agent_run` 等工具）。
> **逐步执行、每步自验、失败即停并报告**。凭据（API Key、FRP token）**只进 `.env` /
> frpc secret 文件，绝不写进任何入库文件或日志**。
>
> **系统分支**：同时覆盖 **Windows** 与 **macOS**。先跑 `uname`（有输出即 macOS/类 Unix，
> 报错即 Windows），只走本机系统分支；未标注系统的步骤两边通用。

---

## 0. 部署前用户必须提供的参数

| 参数 | 说明 | 取值 |
|---|---|---|
| `PEER_NAME` | 本机集群名，小写字母数字下划线且字母开头（如 `pc2`、`mac1`） | ______ |
| `REMOTE_PORT` | frps 上分配给本机的内部转发端口。**约定：pc2=18766，pc3=18767，mac1=18768**（18000/18765 已被 hub 占用） | ______ |
| `PEER_DOMAIN` | 公网入口域名，规则固定 `mcp-<PEER_NAME>.jiantx.net`（由香港 Caddy 终结 HTTPS） | 按规则派生 |
| `FRP_TOKEN` | 香港 frps 节点（47.76.104.225）认证 token（在 hub 机 `frpc.secret.bat` 里） | 用户安全渠道提供 |
| `peer_service.py` | 从 hub 机取一份（`git`/`scp`/复制均可，只需这一个文件）；或克隆仓库只用该文件 | 用户提供或 hub 拷贝 |
| 安装目录 | Windows 推荐 `D:\dev\Project\StockSDK`（无 D 盘用 C 盘）；macOS `~/dev/Project/StockSDK` | ______ |

> 🔴 **公网链路口径（别用裸 IP:端口）**：香港节点 nftables 把 frps 明文转发口只对
> loopback 放行，公网 drop。真实链路：
> `对等机 frpc →(TLS)→ 香港 frps 127.0.0.1:<REMOTE_PORT> ← Caddy（https://mcp-<peer>.jiantx.net）← hub`。

## 1. 前置环境检查（缺什么装什么）

**Windows：**
```powershell
python --version       # 需 3.11+ 64位(哑服务纯标准库,任何 3.9+ 亦可)。无则: winget install Python.Python.3.11
claude --version       # Claude Code CLI。无则: irm https://claude.ai/install.ps1 | iex
```
**macOS：**
```bash
python3 --version       # 3.9+ 即可。无则: brew install python
claude --version        # 无则: curl -fsSL https://claude.ai/install.sh | bash
```
- 两系统通用——**claude CLI 必须已登录**：`claude -p --dangerously-skip-permissions -- "只回复 pong"`
  能回 pong 即可。未登录则**停下来让用户**跑 `claude` 完成 `/login`（交互式，不能代办）。
- （可选）`codex --version`：装了则两引擎可用，没装不影响。
- ⚠ **不需要 venv、不需要 pip install、不需要 fastmcp** —— 哑服务只用标准库。

## 2. 放置 `peer_service.py` + 写 `.env`

把从 hub 取来的 `peer_service.py` 放进安装目录（如 `D:\dev\Project\StockSDK\peer_service.py`）。
生成本机专属强随机 API Key（**每台机器独立一把，不复用 hub 的**）：
```
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
在同目录新建 `.env`（已 gitignore），内容：
```ini
# 本机哑服务鉴权 key（上面生成的随机串；hub 会用它连进来）
PEER_API_KEY=<刚生成的随机串>
# 监听端口(默认 8765,顶替旧网关位置,frp/域名零改动复用)
PEER_SERVICE_PORT=8765
# exec 子进程工作目录(默认本文件所在目录;想锁到别处可显式设)
# PEER_WORK_DIR=D:\dev\Project\StockSDK
```

## 3. 常驻小服务并启动

**Windows（看门狗 bat + 计划任务）：**
取 hub 仓库里的 `start_peer_service.bat` 放同目录（内容见仓库；就是 `python peer_service.py`
的重启循环）。注册开机自启计划任务指向它，例如：
```powershell
schtasks /Create /TN PeerServiceBoot /TR "%CD%\start_peer_service.bat" /SC ONLOGON /RL HIGHEST /F
schtasks /Run /TN PeerServiceBoot
```

**macOS（launchd，KeepAlive 自带崩溃自愈 + 登录自启）：**
写 `~/Library/LaunchAgents/com.stocksdk.peerservice.plist`（`<REPO>` 换成绝对路径，
`<PY>` 换成 `python3` 的绝对路径 `which python3`）：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.stocksdk.peerservice</string>
  <key>WorkingDirectory</key><string><REPO></string>
  <key>ProgramArguments</key>
  <array>
    <string><PY></string>
    <string><REPO>/peer_service.py</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string><REPO>/peer_service.log</string>
  <key>StandardErrorPath</key><string><REPO>/peer_service.log</string>
</dict>
</plist>
```
```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.stocksdk.peerservice.plist
launchctl print gui/$(id -u)/com.stocksdk.peerservice | grep state   # 应为 running
```

本机自验（两系统同）——`/health` 返回 `service: peer_service` 且列出引擎可用性：
```bash
curl -s -H "X-API-Key: <本机 PEER_API_KEY>" http://127.0.0.1:8765/health
```

## 4. 部署 frp 隧道（公网可达，与旧版完全一致，零改动复用）

1. **拿 frpc 二进制**（https://github.com/fatedier/frp/releases）：
   - Windows：`frp_*_windows_amd64.zip` → `frp\frpc.exe`。GitHub 不通就从 hub 机拷。
   - macOS：`frp_*_darwin_arm64.tar.gz`（Intel 用 `darwin_amd64`）→ `frp/frpc`，`chmod +x`；
     被 Gatekeeper 拦则 `xattr -d com.apple.quarantine frp/frpc`。
2. **配置**（均 gitignore）：
   ```bash
   cp frpc_peer.toml.example frpc_peer.toml
   # 编辑：<PEER_NAME> 换本机 peer 名、<REMOTE_PORT> 换分配端口(如 mac1: name="mcp-mac1"/remotePort=18768)
   # 🔴 本地转发目标是 127.0.0.1:8765(哑服务端口),与旧网关同口,frpc 配置无需改
   ```
   token 文件：
   - Windows：`Set-Content frpc.secret.bat "set FRP_TOKEN=<真实token>" -Encoding ascii`
   - macOS：`echo 'export FRP_TOKEN=<真实token>' > frpc.secret.sh && chmod 600 frpc.secret.sh`

   🔴 proxy `name` 在 frps 全局唯一（hub 已占 `api`/`mcp`），必须带机器名后缀。
3. **常驻启动**：
   - **Windows**：`powershell -ExecutionPolicy Bypass -File register_frpc_peer_task.ps1` → `schtasks /Run /TN FrpcTunnel`
   - **macOS**：写 `~/Library/LaunchAgents/com.stocksdk.frpc.plist`（经 `/bin/sh -c` 先 source token 再起 frpc，模板见旧版；`<REPO>` 替换绝对路径）后 `launchctl bootstrap gui/$(id -u) <plist>`。
4. **隧道自验**：`frpc_peer.log` 出现 `start proxy success` 即注册成功。公网还不通是正常的
   （明文口被香港 nftables 封），要等 5 步 Caddy 配好域名后走 HTTPS 验证。

## 5. 香港节点接入域名（hub 侧/用户操作，不在对等机上做）

与旧版**完全一致**（Caddy 只是把 HTTP 反代到 `127.0.0.1:<REMOTE_PORT>`，不关心后端是 MCP
还是纯 HTTP）。转告用户或由 hub 机 Claude 执行（SSH 私钥在 hub `.ssh-frp/hk_frps`）：

1. **DNS**：`jiantx.net` 加 A 记录 `mcp-<PEER_NAME>` → `47.76.104.225`（Cloudflare 必须灰云 DNS only）。
2. **Caddy**：`/etc/caddy/Caddyfile` 追加 site block（照抄 `mcp.jiantx.net`，换域名和端口）：
   ```caddyfile
   mcp-<PEER_NAME>.jiantx.net {
       reverse_proxy 127.0.0.1:<REMOTE_PORT> {
           flush_interval -1
       }
   }
   ```
   > 注：哑服务是自写的 http.server，**没有** fastmcp 的 DNS-rebinding 防护，故**不再需要**
   > `header_up Host localhost`（留着也无害）。然后 `sudo systemctl restart caddy`。
3. **nftables**：把 `<REMOTE_PORT>` 加进 `inet frpguard` 的 drop 集合（loopback 放行、公网 drop），持久化 `/etc/nftables.conf`。
4. **公网自验**（任意机器，受信证书无需 `-k`）：
   ```bash
   curl -s -H "X-API-Key: <对等机 PEER_API_KEY>" https://mcp-<PEER_NAME>.jiantx.net/health
   ```

## 6. 部署完成后回报给用户（hub 接入需要）

```
PEER_NAME  = <peer 名>
PEER_URL   = https://mcp-<PEER_NAME>.jiantx.net
API_KEY    = （已生成,见本机 .env；请安全传递到 hub,别贴公共聊天）
```
提醒：若第 5 步（DNS+Caddy+nftables）没做，先完成再接 hub。

## 7. hub 侧接入（在 hub 主机上做）

hub 机 `.env` 追加（URL 可带可不带 `/mcp` 尾巴，hub 会自动剥掉）：
```ini
MCP_PEERS=pc2=https://mcp-pc2.jiantx.net,mac1=https://mcp-mac1.jiantx.net
PEER_PC2_API_KEY=<pc2 的 API_KEY>
PEER_MAC1_API_KEY=<mac1 的 API_KEY>
```
重启 hub 网关（杀 8765 uvicorn，看门狗 5s 拉起）。验证：`mcp_gateway.log` 出现
`已挂载对等机 mac1 -> 前缀 peer_mac1`；工具清单里出现 `peer_mac1_agent_run` 等 8 个工具。
端到端：hub 的 Claude 调 `peer_mac1_agent_run(engine="claude", prompt="报告本机计算机名")`，
确认返回对等机的机器名。

## 8. 日后维护（关键收益）

- **改 hub 侧的工具逻辑（命令模板 / 新工具 / fs 编排）**：只在 hub 改代码 + 重启 hub 网关，
  **对等机什么都不用动**。这是本架构的核心收益。
- **改哑服务本体 `peer_service.py`（极少）**：hub 上跑
  `.venv-mcp\Scripts\python scripts\push_peer_service.py`（可 `--peer <name>` 指定单台）——
  经 `peer_<name>_svc_update` 把新源码推过去，对等机 py_compile 自检通过后原子替换 + 延迟
  重启，看门狗/launchd 拉起新版本。确定性、不经 git、不经 LLM。

## 9. 排错速查

| 症状 | 原因/处置 |
|---|---|
| `/health` 401 | X-API-Key 与该机 `.env` 的 PEER_API_KEY 不一致 |
| 本机通、公网不通 | ① `frpc_peer.log` 无 `start proxy success` → frpc 未注册（token 错/proxy name 重复/端口占用）；② 隧道通但域名不通 → 第 5 步没做全（DNS/Caddy/证书）；③ 别裸连 `http://47.76.104.225:187xx`（nftables 封明文） |
| 域名 TLS 报错 | Cloudflare 代理没关（灰云 DNS only），或 Caddy 证书申请中（等 1-2 分钟看 `journalctl -u caddy`） |
| hub 日志无 `已挂载对等机` | hub `.env` 的 MCP_PEERS 格式错或缺 `PEER_<NAME大写>_API_KEY`（缺 key warning 跳过） |
| `peer_*_agent_run` failed: 命令未安装 | 对等机 claude CLI 未装/未登录（第 1 步没做完） |
| hub tools/list 变慢 | 某 peer 宕机（PeerClient connect 超时 5s 兜底）；关机的 peer 建议暂时从 MCP_PEERS 摘除 |
| `svc_update` 报语法自检失败未替换 | 推来的 peer_service.py 有语法错——哑服务拒绝替换（保护自己不被写坏），修好再推 |
| **mac** launchd 服务不 running | `launchctl print gui/$(id -u)/com.stocksdk.peerservice` 看 last exit code；日志 `peer_service.log` |

## 10. 安全红线

- 每台机器**独立** API Key；泄露只需换那台 `.env` 并同步 hub 的对应 `PEER_*_API_KEY`。
- `/exec` = 拿到 key 即可在该机 `PEER_WORK_DIR` 内无确认执行任意命令（与 hub 现状同级风险 ×N 台）。
  key 只发可信机器。可选 `PEER_EXEC_ALLOW=claude,codex` 收窄 argv[0] 白名单。
- `.env`、`frpc.secret.*`、`frpc_peer.toml`、`peer_service.log` 均 gitignore；commit/push 前确认 diff 无凭据。
- 不要把 hub 自己的地址写进 hub 的 MCP_PEERS（环形自代理）。
