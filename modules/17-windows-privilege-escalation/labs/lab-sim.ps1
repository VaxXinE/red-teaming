param(
  [ValidateSet('setup','status','run-elevated','cleanup')][string]$Action = 'status',
  [string]$Root = 'C:\ProgramData\RedTeamLab17'
)
$ErrorActionPreference = 'Stop'
$task = Join-Path $Root 'task.ps1'
$proofDir = Join-Path $Root 'proof'
$flag = Join-Path $proofDir 'admin-flag.txt'
$out = Join-Path $Root 'student-output.txt'
function Need-Admin {
  $id=[Security.Principal.WindowsIdentity]::GetCurrent(); $p=New-Object Security.Principal.WindowsPrincipal($id)
  if (-not $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) { throw 'Run this action from an elevated PowerShell.' }
}
if ($Action -eq 'setup') {
  Need-Admin
  New-Item -ItemType Directory -Force -Path $Root,$proofDir | Out-Null
  'MODULE17-ADMIN-PROOF' | Set-Content -Encoding UTF8 $flag
  icacls $proofDir /inheritance:r | Out-Null
  icacls $proofDir /grant:r '*S-1-5-32-544:(OI)(CI)F' '*S-1-5-18:(OI)(CI)F' | Out-Null
  @'
# This script is intentionally writable by normal users for Module 17 training.
"baseline task executed: $(Get-Date -Format o)" | Set-Content -Encoding UTF8 "C:\ProgramData\RedTeamLab17\student-output.txt"
'@ | Set-Content -Encoding UTF8 $task
  icacls $task /inheritance:r | Out-Null
  icacls $task /grant:r '*S-1-5-32-544:F' '*S-1-5-18:F' '*S-1-5-32-545:M' | Out-Null
  Write-Host "Lab ready at $Root"
  Write-Host "A normal user may edit task.ps1, but only the instructor/elevated terminal should run 'run-elevated'."
}
elseif ($Action -eq 'run-elevated') {
  Need-Admin
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $task
  Write-Host "Elevated runner executed task.ps1"
}
elseif ($Action -eq 'cleanup') {
  Need-Admin
  if (Test-Path $Root) { Remove-Item -Recurse -Force $Root }
  Write-Host 'Lab removed.'
}
else {
  Get-Item $Root,$task,$flag,$out -ErrorAction SilentlyContinue | Select-Object FullName,Length,LastWriteTime
  if (Test-Path $task) { icacls $task }
  if (Test-Path $proofDir) { icacls $proofDir }
}
