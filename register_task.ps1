# Register the StockDataService scheduled task:
# at-logon autostart + restart every 1 min on failure + single instance.
# Runs as current interactive user (EM token usable; no admin/password needed).
$ErrorActionPreference = 'Stop'
$taskName = 'StockDataService'
$dir = $PSScriptRoot
$bat = Join-Path $dir 'start_server.bat'
$user = "$env:USERDOMAIN\$env:USERNAME"

$action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument "/c `"$bat`"" -WorkingDirectory $dir
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $user
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet `
    -MultipleInstances IgnoreNew `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -RestartCount 999 `
    -ExecutionTimeLimit (New-TimeSpan -Seconds 0)

try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
        -Principal $principal -Settings $settings -Description 'EM + iFinD stock data HTTP service' -Force | Out-Null
    Write-Output "[OK] Task '$taskName' registered: autostart at logon, restart every 1 min on failure."
    Write-Output "    Start now:   schtasks /Run /TN $taskName"
    Write-Output "    Status:      Get-ScheduledTask -TaskName $taskName"
    Write-Output "    Uninstall:   run uninstall_service.bat"
} catch {
    Write-Output ("[FAIL] " + $_.Exception.Message)
}
