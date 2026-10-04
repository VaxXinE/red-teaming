param([string]$EvidenceDir = "$HOME\Documents\RedTeam\Module17-Windows-PrivEsc\04-evidence")
$ErrorActionPreference = 'Stop'
if (-not (Test-Path $EvidenceDir)) { throw "Missing evidence directory: $EvidenceDir" }
$files = Get-ChildItem -Path $EvidenceDir -File -Recurse | Where-Object { $_.Name -ne 'SHA256SUMS.txt' }
$manifest = foreach ($f in $files) {
  $h = Get-FileHash -Algorithm SHA256 -LiteralPath $f.FullName
  "{0}  {1}" -f $h.Hash.ToLowerInvariant(), $f.FullName
}
$manifest | Set-Content -Encoding UTF8 (Join-Path $EvidenceDir 'SHA256SUMS.txt')
Write-Host "Wrote manifest for $($files.Count) file(s)."
