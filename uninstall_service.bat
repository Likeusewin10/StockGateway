@echo off
REM 卸载"股票数据服务"计划任务并停止正在运行的服务。
REM 右键"以管理员身份运行"本脚本。
setlocal
set TASKNAME=StockDataService

schtasks /End /TN "%TASKNAME%" 2>nul
schtasks /Delete /TN "%TASKNAME%" /F
REM 兜底：杀掉残留的服务进程
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -like '*uvicorn app:app*'} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
echo.
echo [OK] 已卸载任务并停止服务。
endlocal
pause
