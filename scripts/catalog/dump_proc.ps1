param([int]$Pid_, [string]$Out)
# 用 dbghelp MiniDumpWriteDump 全内存 dump 指定进程(需与目标同等或更高完整性→提权运行)
$sig = @"
using System;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;
public class Dmp {
 [DllImport("dbghelp.dll", SetLastError=true)]
 public static extern bool MiniDumpWriteDump(IntPtr h, uint pid, SafeFileHandle f, int type, IntPtr ex, IntPtr u, IntPtr c);
}
"@
Add-Type $sig
$p  = [Diagnostics.Process]::GetProcessById($Pid_)
$fs = New-Object IO.FileStream($Out, [IO.FileMode]::Create)
$ok = [Dmp]::MiniDumpWriteDump($p.Handle, [uint32]$Pid_, $fs.SafeFileHandle, 0x2, [IntPtr]::Zero, [IntPtr]::Zero, [IntPtr]::Zero)
$fs.Close()
if ($ok) { "DUMP_OK $((Get-Item $Out).Length) bytes -> $Out" }
else { "DUMP_FAIL err=$([Runtime.InteropServices.Marshal]::GetLastWin32Error())" }
