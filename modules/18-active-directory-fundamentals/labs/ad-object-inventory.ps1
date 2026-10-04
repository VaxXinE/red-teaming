param(
  [string]$OutputDir = ".\ad-inventory",
  [ValidateRange(1,500)][int]$Limit = 100
)
$ErrorActionPreference='Stop'
if (-not (Get-Module -ListAvailable ActiveDirectory)) { throw 'ActiveDirectory PowerShell module is required (RSAT) for this script.' }
Import-Module ActiveDirectory
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
Get-ADUser -Filter * -ResultSetSize $Limit -Properties DisplayName,Enabled,UserPrincipalName | Select-Object SamAccountName,DisplayName,Enabled,UserPrincipalName,DistinguishedName | Export-Csv -NoTypeInformation -Encoding UTF8 (Join-Path $OutputDir 'users.csv')
Get-ADGroup -Filter * -ResultSetSize $Limit | Select-Object Name,GroupScope,GroupCategory,DistinguishedName | Export-Csv -NoTypeInformation -Encoding UTF8 (Join-Path $OutputDir 'groups.csv')
Get-ADComputer -Filter * -ResultSetSize $Limit -Properties OperatingSystem,DNSHostName | Select-Object Name,DNSHostName,OperatingSystem,DistinguishedName | Export-Csv -NoTypeInformation -Encoding UTF8 (Join-Path $OutputDir 'computers.csv')
Write-Host "Wrote inventory to $OutputDir"
