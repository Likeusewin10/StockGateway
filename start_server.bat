@echo off
REM 股票数据 HTTP 服务 —— 看门狗模式：服务退出后自动重启。
REM 仅本机访问：http://127.0.0.1:8000  交互文档 /docs
REM 日志写入 server.log（追加）。单 worker，勿加 --workers。
cd /d %~dp0

:loop
echo [%date% %time%] starting server >> server.log
.venv-api\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000 >> server.log 2>&1
echo [%date% %time%] server exited, restarting in 5s >> server.log
timeout /t 5 /nobreak >nul
goto loop
