param([string]$OutputPath = ".\module19-ad-enum\08-trusts\trusts.csv")
$ErrorActionPreference='Stop'
Import-Module ActiveDirectory
New-Item -ItemType Directory -Force -Path (Split-Path $OutputPath) | Out-Null
Get-ADTrust -Filter * |
  Select-Object Name,Source,Target,Direction,ForestTransitive,IntraForest,SelectiveAuthentication,SIDFilteringForestAware |
  Export-Csv $OutputPath -NoTypeInformation
Write-Host "Wrote $OutputPath"
