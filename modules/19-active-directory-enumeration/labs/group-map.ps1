param(
  [Parameter(Mandatory=$true)][string]$Identity,
  [string]$OutputPath = ".\module19-ad-enum\04-relations\group-map.csv"
)
$ErrorActionPreference='Stop'
Import-Module ActiveDirectory
New-Item -ItemType Directory -Force -Path (Split-Path $OutputPath) | Out-Null
Get-ADPrincipalGroupMembership -Identity $Identity |
  Select-Object Name,SamAccountName,GroupScope,GroupCategory,DistinguishedName |
  Export-Csv $OutputPath -NoTypeInformation
Write-Host "Wrote $OutputPath"
