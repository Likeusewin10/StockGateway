@echo off
REM 启动股票数据 HTTP 服务（单 worker，勿加 --workers）
REM 同事通过 http://本机IP:8000 访问；交互文档 /docs
cd /d %~dp0
.venv-api\Scripts\python.exe -m uvicorn app:app --host 0.0.0.0 --port 8000
