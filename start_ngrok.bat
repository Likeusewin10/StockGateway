@echo off
REM ngrok 隧道 —— 看门狗模式：退出后自动重连。
REM 把本机 8000 端口的股票数据服务暴露到固定公网域名：
REM   https://quaking-trial-tycoon.ngrok-free.dev
REM authtoken 已写入 %LOCALAPPDATA%\ngrok\ngrok.yml；免费版同一 token 仅允许 1 个会话，
REM 故本任务用 schtasks 的 IgnoreNew 策略保证全机唯一实例（见 register_ngrok_task.ps1）。
REM 日志追加写入 ngrok.log。
cd /d %~dp0

set NGROK=D:\dev\ngrok\ngrok.exe
set DOMAIN=quaking-trial-tycoon.ngrok-free.dev
set PORT=8000

:loop
echo [%date% %time%] starting ngrok tunnel >> ngrok.log
"%NGROK%" http --url=%DOMAIN% %PORT% --log=stdout --log-format=logfmt >> ngrok.log 2>&1
echo [%date% %time%] ngrok exited, reconnecting in 10s >> ngrok.log
timeout /t 10 /nobreak >nul
goto loop
