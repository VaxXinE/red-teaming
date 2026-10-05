param([string]$OutputDir = ".\module19-ad-enum\03-powershell")
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
Import-Module ActiveDirectory
Get-ADDomain | Select-Object * | ConvertTo-Json -Depth 4 | Set-Content "$OutputDir\domain.json"
Get-ADForest | Select-Object * | ConvertTo-Json -Depth 4 | Set-Content "$OutputDir\forest.json"
Get-ADUser -Filter * -Properties Enabled,MemberOf,ServicePrincipalName,LastLogonDate |
  Select-Object SamAccountName,UserPrincipalName,Enabled,LastLogonDate,MemberOf,ServicePrincipalName |
  Export-Csv "$OutputDir\users.csv" -NoTypeInformation
Get-ADGroup -Filter * -Properties GroupScope,GroupCategory,Member |
  Select-Object Name,SamAccountName,GroupScope,GroupCategory,Member |
  Export-Csv "$OutputDir\groups.csv" -NoTypeInformation
Get-ADComputer -Filter * -Properties DNSHostName,OperatingSystem,OperatingSystemVersion,LastLogonDate |
  Select-Object Name,DNSHostName,OperatingSystem,OperatingSystemVersion,LastLogonDate |
  Export-Csv "$OutputDir\computers.csv" -NoTypeInformation
Write-Host "Inventory written to $OutputDir"
