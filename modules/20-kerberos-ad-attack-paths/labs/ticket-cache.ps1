$ErrorActionPreference = 'Stop'
$OutDir = Join-Path $PWD 'module20-ad-paths\01-kerberos'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$Out = Join-Path $OutDir 'ticket-cache.txt'
"Collected: $(Get-Date -Format o)" | Set-Content -Path $Out -Encoding UTF8
"Identity: $(whoami)" | Add-Content -Path $Out
"`n=== klist ===" | Add-Content -Path $Out
(klist 2>&1 | Out-String) | Add-Content -Path $Out
Write-Host "Saved read-only Kerberos cache inventory to $Out"
