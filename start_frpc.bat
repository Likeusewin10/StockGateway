@echo off
REM frpc 隧道 —— 看门狗模式:退出后自动重连。由计划任务 FrpcTunnel(开机/登录自启)拉起。
REM 一个 frpc 进程同时暴露两条隧道到香港 frps 节点(47.76.104.225:7000):
REM   api: 47.76.104.225:18000  -> 127.0.0.1:8000  REST 股票数据服务(含 WebSocket)
REM   mcp: 47.76.104.225:18765  -> 127.0.0.1:8765  MCP 聚合网关(含 SSE)
REM 隧道定义见 frpc.toml;认证 token 见 frpc.secret.bat(不入库,call 进环境变量)。
REM
REM 与 NgrokTunnel 并行独立(不同节点/端口,无抢占冲突)。切换稳定后再停 ngrok。
REM ⚠ 全机唯一实例:计划任务 IgnoreNew 保证;勿再单独起第二个 frpc 看门狗。
REM 日志由 frpc 自身写入 frpc.log(log.to);本看门狗循环状态写 frpc_watchdog.log。
cd /d %~dp0

set FRPC=%~dp0frp\frpc.exe
set CFG=%~dp0frpc.toml

REM 载入不入库的认证 token 到环境变量 FRP_TOKEN(供 frpc.toml 的 {{ .Envs.FRP_TOKEN }} 插值)
call "%~dp0frpc.secret.bat"

:loop
echo [%date% %time%] starting frpc tunnels (api + mcp) >> frpc_watchdog.log
"%FRPC%" -c "%CFG%"
echo [%date% %time%] frpc exited, reconnecting in 10s >> frpc_watchdog.log
timeout /t 10 /nobreak >nul
goto loop
