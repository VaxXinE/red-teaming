param([string]$OutputPath = ".\gpo.txt")
$parent = Split-Path -Parent $OutputPath
if ($parent) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
@(
  "=== User policy ==="
  (gpresult /r /scope user 2>&1 | Out-String).Trim()
  ""
  "=== Computer policy ==="
  (gpresult /r /scope computer 2>&1 | Out-String).Trim()
) | Set-Content -Encoding UTF8 $OutputPath
Write-Host "Wrote $OutputPath"
