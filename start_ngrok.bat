@echo off
REM ngrok 隧道 —— 看门狗模式：退出后自动重连。由计划任务 NgrokTunnel(开机/登录自启)拉起。
REM 一个 ngrok 会话同时暴露两条隧道(付费版同 authtoken 支持多隧道):
REM   api: https://jtx.ngrok.app      -> 8000  REST 股票数据服务
REM   mcp: https://jtx-mcp.ngrok.app  -> 8765  MCP 聚合网关(含 agent 工具 + iFinD 取数)
REM 隧道定义见 ngrok-gateway.yml;authtoken 在 %LOCALAPPDATA%\ngrok\ngrok.yml。
REM
REM ⚠ 全机唯一实例:勿再单独起第二个 ngrok 看门狗,否则两会话抢同一域名报
REM   "endpoint already online" 致整会话失败退出(历史踩坑)。要加隧道就改本文件 + yml。
REM ssh 隧道(22)不起:需后台分配固定 TCP 地址,留空会拖垮会话。
REM 日志追加写入 ngrok.log。
cd /d %~dp0

set NGROK=D:\dev\ngrok\ngrok.exe
set CFG=%~dp0ngrok-gateway.yml
set GLOBALCFG=%LOCALAPPDATA%\ngrok\ngrok.yml

:loop
echo [%date% %time%] starting ngrok tunnels (api + mcp) >> ngrok.log
"%NGROK%" start api mcp --config "%GLOBALCFG%" --config "%CFG%" --log=stdout --log-format=logfmt >> ngrok.log 2>&1
echo [%date% %time%] ngrok exited, reconnecting in 10s >> ngrok.log
timeout /t 10 /nobreak >nul
goto loop
