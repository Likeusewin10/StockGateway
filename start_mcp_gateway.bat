@echo off
REM MCP 聚合网关 —— 看门狗模式:退出后自动重启。
REM 把多厂商上游 MCP 聚合为本机一个 streamable-http 网关,监听 8765。
REM 与 8000 的 REST 取数服务相互独立,可并存。
REM 鉴权:务必在 .env 配置 API_KEY(对外)与各厂商凭据(如 IFIND_MCP_JWT)。
REM 用 .venv-mcp 的 uvicorn.exe(其 site-packages,非系统 Python)。日志追加 mcp_gateway.log。
cd /d %~dp0

:loop
echo [%date% %time%] starting mcp gateway >> mcp_gateway.log
.venv-mcp\Scripts\uvicorn.exe mcp_gateway.server:http_app --host 0.0.0.0 --port 8765 >> mcp_gateway.log 2>&1
echo [%date% %time%] gateway exited, restarting in 5s >> mcp_gateway.log
timeout /t 5 /nobreak >nul
goto loop
