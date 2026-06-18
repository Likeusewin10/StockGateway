# Register the NgrokTunnel scheduled task:
# at-logon autostart + self-heal every 1 min (independent TimeTrigger) + single instance.
# Runs as current interactive user. Mirrors register_task.ps1 (StockDataService) deliberately.
#
# 与 StockDataService 完全平行的一套：start_ngrok.bat 看门狗常驻，schtasks 负责开机自启与
# 退出自愈。免费版 ngrok 同一 authtoken 仅允许 1 个会话，IgnoreNew 策略确保全机唯一实例。
$ErrorActionPreference = 'Stop'
$taskName = 'NgrokTunnel'
$dir = $PSScriptRoot
$user = "$env:USERDOMAIN\$env:USERNAME"
$xmlPath = Join-Path $dir 'ngrok_task_def.xml'
$bat = Join-Path $dir 'start_ngrok.bat'

$xml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.3" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>ngrok tunnel exposing stock data service (port 8000) to fixed public domain</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId>$user</UserId>
    </LogonTrigger>
    <TimeTrigger>
      <Enabled>true</Enabled>
      <StartBoundary>2026-01-01T00:00:00</StartBoundary>
      <Repetition>
        <Interval>PT1M</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
    </TimeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>$user</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>999</Count>
    </RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>cmd.exe</Command>
      <Arguments>/c "$bat"</Arguments>
      <WorkingDirectory>$dir</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"@

# 必须以 UTF-16 (Unicode) 写出，schtasks 才认这个 XML 声明。
[System.IO.File]::WriteAllText($xmlPath, $xml, [System.Text.Encoding]::Unicode)

$create = schtasks /Create /TN $taskName /XML "`"$xmlPath`"" /F 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Output "[OK] Task '$taskName' registered: autostart at logon + self-heal every 1 min (TimeTrigger)."
    Write-Output "    Start now:   schtasks /Run /TN $taskName"
    Write-Output "    Status:      Get-ScheduledTask -TaskName $taskName | Get-ScheduledTaskInfo"
    Write-Output "    Public URL:  https://quaking-trial-tycoon.ngrok-free.dev"
    Write-Output "    Uninstall:   schtasks /Delete /TN $taskName /F"
} else {
    Write-Output ("[FAIL] " + ($create -join ' '))
}
