param([string]$Root = "$HOME\Documents\RedTeam\Module17-Windows-PrivEsc")
$ErrorActionPreference = 'Stop'
$dirs = @('00-scope','01-enum','02-notes','03-findings','04-evidence','05-cleanup')
New-Item -ItemType Directory -Force -Path $Root | Out-Null
foreach ($d in $dirs) { New-Item -ItemType Directory -Force -Path (Join-Path $Root $d) | Out-Null }
"Created: $Root" | Set-Content -Encoding UTF8 (Join-Path $Root '04-evidence\workspace-created.txt')
Write-Host "Workspace ready: $Root"
