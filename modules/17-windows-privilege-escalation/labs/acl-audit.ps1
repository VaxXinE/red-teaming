param([Parameter(Mandatory=$true)][string]$Path)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Path)) { throw "Path not found: $Path" }
Write-Host "Target: $Path"
Get-Acl -LiteralPath $Path | Format-List Path,Owner,AccessToString
Write-Host "`nicacls view:"
icacls $Path
