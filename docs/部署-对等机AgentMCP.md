# 对等机 Agent MCP 部署手册（丢给对等机上的 Claude Code 直接执行）

> **执行者注意（给对等机上的 Claude Code）**：本文档是一份可自动执行的部署任务书。
> 你在一台**对等机**（peer，非 hub 主机）上，目标是把本机部署成 **agent-only MCP 网关节点**：
> 对外只暴露 `agent_run / agent_status / agent_result / agent_sessions / agent_memory_*` 等
> 本机 Agent 工具，经 frp 隧道让 hub 主机聚合调用。**逐步执行、每步自验、失败即停并报告**。
> 涉及凭据的值（API Key、FRP token、GitHub 访问）**只进 `.env` / frpc secret 文件，绝不写进任何入库文件、日志或聊天记录以外的地方**。
>
> **系统分支**：本手册同时覆盖 **Windows** 与 **macOS** 对等机。先跑一句探测（`uname` 有输出即
> macOS/类 Unix，报错即 Windows），然后**只走本机系统的分支**；未标注系统的步骤两边通用。
> 差异总表：
>
> | 事项 | Windows | macOS |
> |---|---|---|
> | venv 内可执行 | `.venv-mcp\Scripts\python.exe` | `.venv-mcp/bin/python` |
> | 常驻 + 自愈 | 计划任务（`register_*.ps1`，看门狗 bat） | `launchd`（`KeepAlive=true` 自带自愈，无需看门狗脚本） |
> | frpc 二进制 | `frp_*_windows_amd64.zip` → `frp\frpc.exe` | `frp_*_darwin_arm64.tar.gz`（Intel 机用 `darwin_amd64`）→ `frp/frpc` |
> | frp token 注入 | `frpc.secret.bat`（`set FRP_TOKEN=…`） | `frpc.secret.sh`（`export FRP_TOKEN=…`），两者均已 gitignore |
> | 安装目录 | `D:\dev\Project\StockSDK`（无 D 盘用 C 盘） | `~/dev/Project/StockSDK` |
>
> ⚠ macOS 上仓库自带的 `*.bat` / `*.ps1` 一律不用；launchd plist 按第 4/5 步模板现场生成
> （生成的 plist 放 `~/Library/LaunchAgents/`，不入库）。

---

## 0. 部署前用户必须提供的参数（执行者先向用户确认齐全再动手）

| 参数 | 说明 | 本次取值（用户填/口头告知） |
|---|---|---|
| `PEER_NAME` | 本机在集群里的名字，小写字母数字下划线且字母开头（如 `pc2`、`mac1`） | ______ |
| `REMOTE_PORT` | frps 上分配给本机的公网端口。**约定：pc2=18766，pc3=18767，mac1=18768**（18000/18765 已被 hub 占用，勿撞车） | ______ |
| `FRP_TOKEN` | 香港 frps 节点（47.76.104.225）的认证 token，向用户要（在 hub 机的 `frpc.secret.bat` 里） | 用户口头/安全渠道提供 |
| 仓库访问 | GitHub 私有仓库 `https://github.com/Likeusewin10/StockGateway.git` 的访问方式（Git Credential Manager 弹窗登录 / PAT / SSH key） | 用户操作或提供 |
| 安装目录 | Windows 推荐 `D:\dev\Project\StockSDK`（无 D 盘则 C 盘）；macOS 推荐 `~/dev/Project/StockSDK` | ______ |

## 1. 前置环境检查（缺什么装什么）

**Windows：**

```powershell
git --version          # 无则: winget install Git.Git
python --version       # 需 3.11.x 64位。无则: winget install Python.Python.3.11
claude --version       # Claude Code CLI。无则: irm https://claude.ai/install.ps1 | iex
```

**macOS：**

```bash
git --version           # 无则先装 Xcode CLT: xcode-select --install
python3.11 --version    # 无则: brew install python@3.11（无 brew 先装 Homebrew）
claude --version        # 无则: curl -fsSL https://claude.ai/install.sh | bash
```

- 两系统通用——**claude CLI 必须已登录**：登录态无法静默检查，直接跑一发验证：
  `claude -p --dangerously-skip-permissions -- "只回复 pong"` 能回 pong 即可。
  未登录则**停下来让用户**在终端跑 `claude` 完成 `/login`（交互式，执行者不能代办）。
- （可选）`codex --version`：装了则两引擎可用，没装不影响（任务会返回 failed，不崩）。

## 2. 克隆仓库 + 建 venv

**Windows：**

```powershell
mkdir D:\dev\Project -Force; cd D:\dev\Project
git clone https://github.com/Likeusewin10/StockGateway.git StockSDK   # GCM 会弹窗让用户登录 GitHub
cd StockSDK
python -m venv .venv-mcp
.venv-mcp\Scripts\pip install -r requirements-mcp.txt
```

**macOS：**

```bash
mkdir -p ~/dev/Project && cd ~/dev/Project
git clone https://github.com/Likeusewin10/StockGateway.git StockSDK
cd StockSDK
python3.11 -m venv .venv-mcp
.venv-mcp/bin/pip install -r requirements-mcp.txt
```

自验（macOS 把 `\` 路径换成 `/bin/`，下同）：
`.venv-mcp\Scripts\python -m pytest tests\test_mcp_gateway_peers.py tests\test_mcp_gateway_providers.py -q` 全绿。

## 3. 写 `.env`（对等机形态的关键配置，两系统内容相同）

生成本机专属强随机 API Key（**每台机器独立一把，不复用 hub 的**）：

```
# Windows: .venv-mcp\Scripts\python  /  macOS: .venv-mcp/bin/python
<venv-python> -c "import secrets; print(secrets.token_urlsafe(32))"
```

在仓库根新建 `.env`（已 gitignore），内容只需三行：

```ini
# 本机网关鉴权 key（上面生成的随机串；hub 会用它连进来）
API_KEY=<刚生成的随机串>
# 对等机形态：只暴露 agent 工具，不挂任何股票厂商上游
MCP_GATEWAY_MODE=agent-only
MCP_GATEWAY_PORT=8765
```

> 不需要 iFinD/Tushare 等任何厂商凭据——agent-only 模式根本不挂它们。

## 4. 常驻网关并启动

**Windows（计划任务 + 看门狗 bat）：**

```powershell
powershell -ExecutionPolicy Bypass -File register_mcp_gateway_task.ps1
schtasks /Run /TN MCPGatewayBoot
```

**macOS（launchd，KeepAlive 自带崩溃自愈 + 登录自启）：**
把下面 plist 写到 `~/Library/LaunchAgents/com.stocksdk.mcpgateway.plist`
（`<REPO>` 全部替换为仓库绝对路径，如 `/Users/<用户名>/dev/Project/StockSDK`）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.stocksdk.mcpgateway</string>
  <key>WorkingDirectory</key><string><REPO></string>
  <key>ProgramArguments</key>
  <array>
    <string><REPO>/.venv-mcp/bin/uvicorn</string>
    <string>mcp_gateway.server:http_app</string>
    <string>--host</string><string>0.0.0.0</string>
    <string>--port</string><string>8765</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string><REPO>/mcp_gateway.log</string>
  <key>StandardErrorPath</key><string><REPO>/mcp_gateway.log</string>
</dict>
</plist>
```

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.stocksdk.mcpgateway.plist
launchctl print gui/$(id -u)/com.stocksdk.mcpgateway | grep state   # 应为 running
# 停止/卸载（排错用）: launchctl bootout gui/$(id -u)/com.stocksdk.mcpgateway
```

本机自验（两系统同）——列出的工具应为裸名 `agent_run`、`agent_status` 等，**没有** `agent_agent_` 双前缀、没有任何 `ifind_/tushare_` 工具：

```
# Windows: $env:CHECK_API_KEY="<本机 API_KEY>"  /  macOS: export CHECK_API_KEY="<本机 API_KEY>"
<venv-python> scripts/check_mcp_gateway.py
```

## 5. 部署 frp 隧道（公网可达）

1. **拿 frpc 二进制**（https://github.com/fatedier/frp/releases 最新稳定版）：
   - Windows：`frp_*_windows_amd64.zip`，解压出 `frpc.exe` 放到仓库根 `frp\frpc.exe`。GitHub 不通就从 hub 机拷同一个。
   - macOS：Apple Silicon 用 `frp_*_darwin_arm64.tar.gz`（Intel 用 `darwin_amd64`），解压出 `frpc` 放 `frp/frpc` 并 `chmod +x frp/frpc`。首次运行若被 Gatekeeper 拦（"无法验证开发者"），执行 `xattr -d com.apple.quarantine frp/frpc` 放行。
2. **配置**（所有产物均已 gitignore）：
   ```bash
   cp frpc_peer.toml.example frpc_peer.toml
   # 编辑 frpc_peer.toml：<PEER_NAME> 换成本机 peer 名、<REMOTE_PORT> 换成分配端口
   # 例（mac1）: name = "mcp-mac1" / remotePort = 18768
   ```
   token 文件按系统写（内容一行，`<真实token>` 换成用户提供值）：
   - Windows：`Set-Content frpc.secret.bat "set FRP_TOKEN=<真实token>" -Encoding ascii`
   - macOS：`echo 'export FRP_TOKEN=<真实token>' > frpc.secret.sh && chmod 600 frpc.secret.sh`

   🔴 proxy `name` 在 frps 全局唯一（hub 已占 `api`/`mcp`），必须带机器名后缀，否则 frps 拒绝注册、frpc 反复重连。
3. **常驻启动**：

   **Windows：**
   ```powershell
   powershell -ExecutionPolicy Bypass -File register_frpc_peer_task.ps1
   schtasks /Run /TN FrpcTunnel
   ```

   **macOS**：写 `~/Library/LaunchAgents/com.stocksdk.frpc.plist`（`<REPO>` 同前替换；
   launchd 不执行 shell 展开，故经 `/bin/sh -c` 先 source token 再起 frpc）：

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
     "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
     <key>Label</key><string>com.stocksdk.frpc</string>
     <key>WorkingDirectory</key><string><REPO></string>
     <key>ProgramArguments</key>
     <array>
       <string>/bin/sh</string>
       <string>-c</string>
       <string>. <REPO>/frpc.secret.sh && exec <REPO>/frp/frpc -c <REPO>/frpc_peer.toml</string>
     </array>
     <key>RunAtLoad</key><true/>
     <key>KeepAlive</key><true/>
     <key>StandardOutPath</key><string><REPO>/frpc_watchdog.log</string>
     <key>StandardErrorPath</key><string><REPO>/frpc_watchdog.log</string>
   </dict>
   </plist>
   ```

   ```bash
   launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.stocksdk.frpc.plist
   ```
4. **公网自验**（两系统同，应与第 4 步本机自验输出一致）：
   ```
   <venv-python> scripts/check_mcp_gateway.py http://47.76.104.225:<REMOTE_PORT>/mcp
   ```
   失败先看 `frpc_peer.log`：`start proxy success` 表示隧道通；`port already used` 表示端口被占（换口并同步告知用户）；token 错则连不上 frps。

## 6. 部署完成后回报给用户（hub 接入需要）

向用户输出如下三行（API Key 让用户通过安全渠道带到 hub 机，别贴进公共聊天）：

```
PEER_NAME  = <peer 名>
PEER_URL   = http://47.76.104.225:<REMOTE_PORT>/mcp
API_KEY    = （已生成，见本机 .env；请安全传递到 hub）
```

## 7. hub 侧接入（在 hub 主机上做，不在对等机）

hub 机 `.env` 追加（多个 peer 逗号相接，Mac peer 与 Windows peer 写法完全一样）：

```ini
MCP_PEERS=pc2=http://47.76.104.225:18766/mcp,mac1=http://47.76.104.225:18768/mcp
PEER_PC2_API_KEY=<pc2 的 API_KEY>
PEER_MAC1_API_KEY=<mac1 的 API_KEY>
```

重启 hub 网关（杀掉 8765 的 uvicorn，看门狗 5s 自动拉起）：

```powershell
Get-CimInstance Win32_Process -Filter "Name='uvicorn.exe'" |
  Where-Object { $_.CommandLine -match 'mcp_gateway' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

验证：`mcp_gateway.log` 出现 `已挂载对等机 mac1 -> 前缀 peer_mac1`；hub 上跑
`scripts\check_mcp_gateway.py`（CHECK_API_KEY 用 **hub 的** key），工具清单里出现
`peer_mac1_agent_run` 等。最后端到端：hub 的 Claude 调
`peer_mac1_agent_run(engine="claude", prompt="报告本机计算机名和 git log -1")`，
确认返回的是**对等机**的机器名。

## 8. 排错速查

| 症状 | 原因/处置 |
|---|---|
| `check_mcp_gateway.py` 报 401 | CHECK_API_KEY 与该网关 `.env` 的 API_KEY 不一致 |
| 本机通、公网不通 | frpc 未起或注册被拒：看 `frpc_peer.log`（token 错 / proxy name 重复 / 端口占用） |
| hub 日志无 `已挂载对等机` | hub `.env` 的 MCP_PEERS 格式错（`name=url` 逗号分隔）或缺 `PEER_<NAME大写>_API_KEY`（缺 key 会 warning 跳过） |
| `peer_*_agent_run` 调用 failed: engine not found | 对等机 claude CLI 未装/未登录（第 1 步没做完） |
| agent 任务 session_id 在别的机器续接失败 | 预期行为：会话历史存各机本地，session_id 只在创建它的那台机器有效 |
| hub tools/list 变慢 | 某 peer 宕机（connect 超时 5s 兜底）；关机的 peer 建议暂时从 MCP_PEERS 摘除 |
| **mac** launchd 服务不在 running | `launchctl print gui/$(id -u)/com.stocksdk.mcpgateway` 看 last exit code；日志在仓库根 `mcp_gateway.log` / `frpc_watchdog.log` |
| **mac** frpc "无法验证开发者" | `xattr -d com.apple.quarantine frp/frpc` 后重试 |
| **mac** 改了 .env/plist 不生效 | launchd 不会自动重载：`launchctl kickstart -k gui/$(id -u)/com.stocksdk.mcpgateway`（frpc 同理，换 Label） |
| **mac** claude 走 launchd 起的任务报找不到命令 | launchd PATH 极简；`agent_runner` 用 `shutil.which` 解析绝对路径，若仍失败，在 plist 加 `EnvironmentVariables` 补 PATH（含 claude 安装目录，如 `~/.local/bin`） |

## 9. 安全红线（执行者与用户都要守）

- 每台机器**独立** API Key；泄露只需换那一台的 `.env` 并同步 hub 的对应 `PEER_*_API_KEY`。
- `agent_run` = 拿到 key 即可在该机仓库目录内无确认执行任意命令（`--dangerously-skip-permissions`），与 hub 现状同级风险 ×N 台。key 只发可信机器。
- `.env`、`frpc.secret.bat` / `frpc.secret.sh`、`frpc_peer.toml` 均已 gitignore；**任何 commit/push 前确认 diff 无凭据**。macOS 的 launchd plist 放 `~/Library/LaunchAgents/`（仓库外），天然不入库。
- 不要把 hub 自己的地址写进 hub 的 MCP_PEERS（会环形自代理）。
