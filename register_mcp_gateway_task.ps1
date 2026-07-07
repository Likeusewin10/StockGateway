# Register the MCPGatewayBoot scheduled task:
# at-logon autostart + self-heal every 1 min (independent TimeTrigger) + single instance.
# Runs as current interactive user. Mirrors register_frpc_task.ps1 deliberately.
#
# 适用两种形态（由 .env 的 MCP_GATEWAY_MODE 决定，本脚本无需区分）：
#   hub（full 模式）：厂商上游 + agent 工具 + peers 全挂载；
#   对等机（agent-only 模式）：只暴露 agent 工具，供 hub 挂载。
# 看门狗常驻 = start_mcp_gateway.bat；本任务负责开机自启 + 每分钟自愈拉起。
$ErrorActionPreference = 'Stop'
$taskName = 'MCPGatewayBoot'
# $PSScriptRoot 在部分调用方式下为空,用 MyInvocation 兜底,再退回当前目录。
$dir = $PSScriptRoot
if (-not $dir) { $dir = Split-Path -Parent $MyInvocation.MyCommand.Path }
if (-not $dir) { $dir = (Get-Location).Path }
$user = "$env:USERDOMAIN\$env:USERNAME"
$xmlPath = Join-Path $dir 'mcp_gateway_task_def.xml'
$bat = Join-Path $dir 'start_mcp_gateway.bat'

$xml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.3" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>MCP aggregation gateway (port 8765) watchdog: autostart at logon + self-heal every 1 min</Description>
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
    Write-Output "    Stop:        schtasks /End /TN $taskName"
    Write-Output "    Gateway:     http://127.0.0.1:8765/mcp"
    Write-Output "    Uninstall:   schtasks /Delete /TN $taskName /F"
} else {
    Write-Output ("[FAIL] " + ($create -join ' '))
}
