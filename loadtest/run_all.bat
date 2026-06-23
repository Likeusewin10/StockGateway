@echo off
REM 一键跑三类生产实践测试（在仓库根目录双击或命令行执行）。
REM 前置：服务已在 8000 运行（start_server.bat 或计划任务 StockDataService）。
REM 注意：必须用 .venv-api 的 python（其 site-packages）。
cd /d %~dp0\..

echo ============================================================
echo [1/3] 并发承载（压 /health，不吃限流、不耗 SDK 配额）
echo ============================================================
.venv-api\Scripts\python.exe loadtest\concurrency.py --target /health --concurrency 1,4,16,64 --duration 15

echo.
echo ============================================================
echo [2/3] 崩溃自愈 - 看门狗层（杀 uvicorn，验 5s 内拉起）
echo ============================================================
.venv-api\Scripts\python.exe loadtest\crash_recovery.py --layer watchdog

echo.
echo ============================================================
echo [3/3] WebSocket 长稳（16 路订阅 3 分钟）
echo ============================================================
.venv-api\Scripts\python.exe loadtest\ws_soak.py --path /ths/ws --connections 16 --duration 180

echo.
echo 全部完成。结果 CSV 见 loadtest\results\
pause
