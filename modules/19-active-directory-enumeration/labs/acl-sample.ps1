param(
  [Parameter(Mandatory=$true)][string]$Identity,
  [string]$OutputPath = ".\module19-ad-enum\07-acl\acl.csv"
)
$ErrorActionPreference='Stop'
Import-Module ActiveDirectory
New-Item -ItemType Directory -Force -Path (Split-Path $OutputPath) | Out-Null
(Get-Acl "AD:$Identity").Access |
  Select-Object IdentityReference,ActiveDirectoryRights,AccessControlType,ObjectType,InheritedObjectType,IsInherited |
  Export-Csv $OutputPath -NoTypeInformation
Write-Host "Wrote $OutputPath"
