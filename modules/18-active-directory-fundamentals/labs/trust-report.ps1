param([string]$OutputPath = ".\trusts.txt")
$parent = Split-Path -Parent $OutputPath
if ($parent) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
@(
  "=== Domain Trusts (read-only nltest) ==="
  (nltest /domain_trusts 2>&1 | Out-String).Trim()
) | Set-Content -Encoding UTF8 $OutputPath
Write-Host "Wrote $OutputPath"
