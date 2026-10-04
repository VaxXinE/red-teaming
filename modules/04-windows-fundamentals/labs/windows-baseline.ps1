# Module 04 - Windows Baseline Collector
# Read-only inventory for your own Windows VM. No credential dumping.

[CmdletBinding()]
param(
    [string]$OutputRoot = "$env:USERPROFILE\Documents\RedTeam\Module04\evidence"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$out = Join-Path $OutputRoot "windows-baseline-$stamp.txt"

function Add-Section {
    param([string]$Title, [scriptblock]$Body)
    "`r`n===== $Title =====" | Out-File -FilePath $out -Append -Encoding utf8
    try {
        & $Body | Out-String -Width 240 | Out-File -FilePath $out -Append -Encoding utf8
    } catch {
        "ERROR: $($_.Exception.Message)" | Out-File -FilePath $out -Append -Encoding utf8
    }
}

"Module 04 Windows baseline - $(Get-Date -Format o)" | Out-File -FilePath $out -Encoding utf8

Add-Section 'Identity' { whoami /all }
Add-Section 'OS' { Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber, OsArchitecture, CsName }
Add-Section 'Local Users' { Get-LocalUser | Select-Object Name, Enabled, LastLogon }
Add-Section 'Local Groups' { Get-LocalGroup | Select-Object Name, Description }
Add-Section 'Administrators Group' { Get-LocalGroupMember -Group 'Administrators' }
Add-Section 'Top Processes' { Get-Process | Sort-Object CPU -Descending | Select-Object -First 20 Name, Id, CPU, Path }
Add-Section 'Running Services' { Get-Service | Where-Object Status -eq 'Running' | Sort-Object Name | Select-Object Name, DisplayName, Status }
Add-Section 'Scheduled Tasks (summary)' { Get-ScheduledTask | Select-Object -First 100 TaskPath, TaskName, State }
Add-Section 'Network Configuration' { Get-NetIPConfiguration }
Add-Section 'Listening TCP' { Get-NetTCPConnection -State Listen | Sort-Object LocalPort | Select-Object LocalAddress, LocalPort, OwningProcess }
Add-Section 'Routes' { Get-NetRoute | Sort-Object DestinationPrefix, RouteMetric | Select-Object DestinationPrefix, NextHop, InterfaceAlias, RouteMetric }
Add-Section 'Recent System Warnings/Errors' { Get-WinEvent -FilterHashtable @{LogName='System'; Level=2,3; StartTime=(Get-Date).AddDays(-1)} -MaxEvents 30 | Select-Object TimeCreated, Id, ProviderName, LevelDisplayName, Message }
Add-Section 'Recent Application Warnings/Errors' { Get-WinEvent -FilterHashtable @{LogName='Application'; Level=2,3; StartTime=(Get-Date).AddDays(-1)} -MaxEvents 30 | Select-Object TimeCreated, Id, ProviderName, LevelDisplayName, Message }

$hash = Get-FileHash -Algorithm SHA256 -Path $out
"`r`nSHA256: $($hash.Hash)" | Out-File -FilePath $out -Append -Encoding utf8
Write-Host "Baseline written to: $out"
