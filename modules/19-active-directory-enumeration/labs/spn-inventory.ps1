param([string]$OutputPath = ".\module19-ad-enum\04-relations\spns.csv")
$ErrorActionPreference='Stop'
Import-Module ActiveDirectory
New-Item -ItemType Directory -Force -Path (Split-Path $OutputPath) | Out-Null
$rows = foreach ($u in Get-ADUser -LDAPFilter '(servicePrincipalName=*)' -Properties ServicePrincipalName,MemberOf,PasswordLastSet,Enabled) {
  foreach ($spn in $u.ServicePrincipalName) {
    [pscustomobject]@{SamAccountName=$u.SamAccountName; SPN=$spn; Enabled=$u.Enabled; PasswordLastSet=$u.PasswordLastSet; MemberOf=($u.MemberOf -join ';')}
  }
}
$rows | Export-Csv $OutputPath -NoTypeInformation
Write-Host "Wrote $OutputPath"
