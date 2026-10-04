param([string]$OutputPath = ".\kerberos.txt")
$parent = Split-Path -Parent $OutputPath
if ($parent) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
@(
  "=== Identity ==="
  (whoami /upn 2>&1 | Out-String).Trim()
  ""
  "=== Kerberos Ticket Cache ==="
  (klist 2>&1 | Out-String).Trim()
) | Set-Content -Encoding UTF8 $OutputPath
Write-Host "Wrote $OutputPath"
