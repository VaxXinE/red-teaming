[CmdletBinding()]
param([string]$OutputDir = "$env:USERPROFILE\Documents\RedTeam\Module22\execution")
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$steps = @(
    @{ Id='T1033'; Name='System Owner/User Discovery'; Script={ whoami } },
    @{ Id='T1082'; Name='System Information Discovery'; Script={ Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsArchitecture,CsName } },
    @{ Id='T1057'; Name='Process Discovery'; Script={ Get-Process | Select-Object -First 40 Name,Id,Path } },
    @{ Id='T1087.001'; Name='Account Discovery: Local Account'; Script={ Get-LocalUser | Select-Object Name,Enabled,LastLogon } }
)
$activity = @()
foreach ($step in $steps) {
    $start = Get-Date
    $result = & $step.Script 2>&1 | Out-String
    $file = Join-Path $OutputDir (($step.Id -replace '\.','_') + '.txt')
    $result | Set-Content -Encoding UTF8 $file
    $activity += [pscustomobject]@{Time=$start.ToString('o');Technique=$step.Id;Name=$step.Name;Output=$file}
}
$activity | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 (Join-Path $OutputDir 'activity.json')
Write-Host "Read-only discovery simulation complete: $OutputDir"
