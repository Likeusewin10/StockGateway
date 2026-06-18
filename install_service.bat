@echo off
REM 注册"股票数据服务"为登录自启 + 崩溃自动重启的计划任务。
REM 直接双击运行即可（无需管理员）。用 PowerShell 生成任务并注册，避免 bat 的 XML 转义问题。
cd /d %~dp0
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0register_task.ps1"
pause
