param([string]$OutputDir = ".\module19-ad-enum\06-gpo")
$ErrorActionPreference='Stop'
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
Import-Module ActiveDirectory
Import-Module GroupPolicy
Get-GPO -All | Select-Object DisplayName,Id,GpoStatus,CreationTime,ModificationTime |
  Export-Csv "$OutputDir\gpos.csv" -NoTypeInformation
Get-ADOrganizationalUnit -Filter * -Properties gPLink |
  Select-Object DistinguishedName,gPLink |
  Export-Csv "$OutputDir\ou-gplinks.csv" -NoTypeInformation
Write-Host "Wrote GPO inventory to $OutputDir"
