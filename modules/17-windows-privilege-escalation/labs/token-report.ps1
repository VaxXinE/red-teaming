param([string]$OutFile = "$HOME\Documents\RedTeam\Module17-Windows-PrivEsc\01-enum\token.txt")
$ErrorActionPreference = 'Stop'
$dir = Split-Path -Parent $OutFile
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$lines = @()
$lines += "=== Identity ==="
$lines += (whoami)
$lines += ""
$lines += "=== Access token ==="
$lines += (whoami /all | Out-String)
$lines += ""
$lines += "=== Integrity hints ==="
$lines += (whoami /groups | Select-String 'Mandatory Label' | Out-String)
$lines | Set-Content -Encoding UTF8 $OutFile
Write-Host "Wrote: $OutFile"
