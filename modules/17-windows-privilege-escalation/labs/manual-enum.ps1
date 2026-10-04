param([string]$OutDir = "$HOME\Documents\RedTeam\Module17-Windows-PrivEsc\01-enum")
$ErrorActionPreference = 'Continue'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
function Save($name, $content) { $content | Out-File -Encoding UTF8 -Width 260 (Join-Path $OutDir $name) }
Save 'identity.txt' (whoami /all | Out-String)
Save 'system.txt' (Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsBuildNumber,OsArchitecture,CsName | Format-List | Out-String)
Save 'users-groups.txt' ((Get-LocalUser | Select-Object Name,Enabled,LastLogon | Format-Table -AutoSize | Out-String) + "`n" + (Get-LocalGroup | Select-Object Name | Format-Table -AutoSize | Out-String))
Save 'processes.txt' (Get-Process | Sort-Object ProcessName | Select-Object ProcessName,Id,Path | Format-Table -AutoSize | Out-String)
Save 'services.txt' (Get-CimInstance Win32_Service | Select-Object Name,StartName,State,StartMode,PathName | Sort-Object Name | Format-Table -AutoSize | Out-String)
Save 'tasks.txt' (Get-ScheduledTask | Select-Object TaskPath,TaskName,State,@{n='RunAs';e={$_.Principal.UserId}},@{n='RunLevel';e={$_.Principal.RunLevel}} | Sort-Object TaskPath,TaskName | Format-Table -AutoSize | Out-String)
Save 'network.txt' ((Get-NetIPAddress -AddressFamily IPv4 | Select-Object InterfaceAlias,IPAddress,PrefixLength | Format-Table -AutoSize | Out-String) + "`n" + (Get-NetTCPConnection -State Listen | Select-Object LocalAddress,LocalPort,OwningProcess | Sort-Object LocalPort | Format-Table -AutoSize | Out-String))
Write-Host "Enumeration saved under: $OutDir"
