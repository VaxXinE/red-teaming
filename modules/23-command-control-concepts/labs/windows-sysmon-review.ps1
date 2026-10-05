$ErrorActionPreference = 'Stop'
Write-Host '=== Sysmon ProcessCreate (1) ==='
try { Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; Id=1; StartTime=(Get-Date).AddHours(-4)} -MaxEvents 20 | Select-Object TimeCreated,Id,Message } catch { Write-Warning $_ }
Write-Host '=== Sysmon NetworkConnect (3) ==='
try { Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; Id=3; StartTime=(Get-Date).AddHours(-4)} -MaxEvents 20 | Select-Object TimeCreated,Id,Message } catch { Write-Warning $_ }
Write-Host '=== Sysmon DNSQuery (22) ==='
try { Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; Id=22; StartTime=(Get-Date).AddHours(-4)} -MaxEvents 20 | Select-Object TimeCreated,Id,Message } catch { Write-Warning $_ }
