@echo off
REM 对等机哑执行小服务 peer_service.py —— 看门狗模式:退出后自动重启。
REM 纯标准库,用系统 Python(不需要 venv)。监听 8765,顶替旧 MCP 网关位置,
REM frp 隧道 / 域名 / Caddy 零改动复用。鉴权用 .env 的 PEER_API_KEY / API_KEY。
REM 常驻:把计划任务(如 PeerServiceBoot)指向本 bat,或直接双击运行。
cd /d %~dp0

:loop
echo [%date% %time%] starting peer_service >> peer_service.log
python peer_service.py >> peer_service.log 2>&1
echo [%date% %time%] peer_service exited, restarting in 5s >> peer_service.log
timeout /t 5 /nobreak >nul
goto loop
