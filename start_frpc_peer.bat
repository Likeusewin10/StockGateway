@echo off
REM frpc 对等机(peer)隧道 —— 看门狗模式:退出后自动重连。
REM 只暴露一条隧道:本机 agent-only MCP 网关(8765) -> 香港 frps 节点(47.76.104.225)。
REM 配置见 frpc_peer.toml(从 frpc_peer.toml.example 复制填好,已 gitignore);
REM 认证 token 见 frpc.secret.bat(不入库,call 进环境变量)。
REM 计划任务注册:register_frpc_peer_task.ps1(任务名 FrpcTunnel,对等机上唯一)。
cd /d %~dp0

set FRPC=%~dp0frp\frpc.exe
set CFG=%~dp0frpc_peer.toml

REM 载入不入库的认证 token 到环境变量 FRP_TOKEN(供 frpc_peer.toml 的 {{ .Envs.FRP_TOKEN }} 插值)
call "%~dp0frpc.secret.bat"

:loop
echo [%date% %time%] starting frpc peer tunnel (mcp) >> frpc_watchdog.log
"%FRPC%" -c "%CFG%"
echo [%date% %time%] frpc exited, reconnecting in 10s >> frpc_watchdog.log
timeout /t 10 /nobreak >nul
goto loop
