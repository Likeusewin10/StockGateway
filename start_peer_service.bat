@echo off
REM 对等机哑执行小服务 peer_service.py —— 看门狗模式:退出后自动重启。
REM 纯标准库,不需要任何第三方依赖。优先用仓库内 .venv-mcp 的解释器(对等机通常已有它,
REM 且部分机器无真实系统 python),缺失则回退 PATH 上的 python。监听 8765,顶替旧网关位置,
REM frp 隧道 / 域名 / Caddy 零改动复用。鉴权用 .env 的 PEER_API_KEY / API_KEY。
cd /d %~dp0

set "PYEXE=python"
if exist "%~dp0.venv-mcp\Scripts\python.exe" set "PYEXE=%~dp0.venv-mcp\Scripts\python.exe"

:loop
echo [%date% %time%] starting peer_service with %PYEXE% >> peer_service.log
"%PYEXE%" peer_service.py >> peer_service.log 2>&1
echo [%date% %time%] peer_service exited, restarting in 5s >> peer_service.log
timeout /t 5 /nobreak >nul
goto loop
