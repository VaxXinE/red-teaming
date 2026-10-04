param([string]$OutputPath = ".\windows-inventory.txt")
$ErrorActionPreference = 'SilentlyContinue'
$parent = Split-Path -Parent $OutputPath
if ($parent) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
$lines = New-Object System.Collections.Generic.List[string]
function Add-Section([string]$Name) { $lines.Add(""); $lines.Add("=== $Name ===") }
Add-Section 'Identity'
$lines.Add((whoami)); $lines.Add((whoami /upn 2>&1 | Out-String).Trim()); $lines.Add((whoami /all 2>&1 | Out-String).Trim())
Add-Section 'Computer'
$lines.Add((Get-ComputerInfo | Select-Object CsName,WindowsProductName,WindowsVersion,OsArchitecture,CsDomain,CsPartOfDomain | Format-List | Out-String).Trim())
Add-Section 'Network'
$lines.Add((ipconfig /all | Out-String).Trim())
Add-Section 'DC Locator'
$lines.Add((nltest /dsgetdc:$env:USERDNSDOMAIN 2>&1 | Out-String).Trim())
Add-Section 'AD PowerShell (if available)'
if (Get-Module -ListAvailable ActiveDirectory) {
  Import-Module ActiveDirectory
  $lines.Add((Get-ADDomain | Select-Object DNSRoot,NetBIOSName,DistinguishedName,PDCEmulator,RIDMaster,InfrastructureMaster | Format-List | Out-String).Trim())
  $lines.Add((Get-ADForest | Select-Object Name,RootDomain,Domains,GlobalCatalogs,SchemaMaster,DomainNamingMaster | Format-List | Out-String).Trim())
} else { $lines.Add('ActiveDirectory module not installed.') }
$lines | Set-Content -Encoding UTF8 $OutputPath
Write-Host "Wrote $OutputPath"
