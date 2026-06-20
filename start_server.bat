@echo off
REM Stock data HTTP service - watchdog mode: auto-restart on exit.
REM Listens on all NICs (incl Tailscale). Ensure API_KEY is set. Single worker, no --workers.
REM Logs append to server.log. Uses .venv-api uvicorn.exe (its site-packages, NOT system Python).
cd /d %~dp0

:loop
echo [%date% %time%] starting server >> server.log
.venv-api\Scripts\uvicorn.exe app:app --host 0.0.0.0 --port 8000 >> server.log 2>&1
echo [%date% %time%] server exited, restarting in 5s >> server.log
timeout /t 5 /nobreak >nul
goto loop
