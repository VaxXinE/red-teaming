param([string]$Output = "$env:USERPROFILE\Documents\module24-windows-telemetry.txt")
$ErrorActionPreference = 'Continue'
$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("UTC: $([DateTime]::UtcNow.ToString('o'))")
$lines.Add("=== Sysmon ===")
try {
  $ev = Get-WinEvent -LogName 'Microsoft-Windows-Sysmon/Operational' -MaxEvents 80 -ErrorAction Stop | Where-Object { $_.Id -in 1,3,11,12,13,14,22 }
  foreach ($e in $ev) { $lines.Add("$($e.TimeCreated.ToUniversalTime().ToString('o')) ID=$($e.Id) $($e.ProviderName)") }
} catch { $lines.Add("Sysmon unavailable: $($_.Exception.Message)") }
$lines.Add("=== Security 4688 ===")
try {
  $ev2 = Get-WinEvent -FilterHashtable @{LogName='Security';Id=4688;StartTime=(Get-Date).AddHours(-1)} -MaxEvents 80 -ErrorAction Stop
  foreach ($e in $ev2) { $lines.Add("$($e.TimeCreated.ToUniversalTime().ToString('o')) ID=4688") }
} catch { $lines.Add("4688 unavailable: $($_.Exception.Message)") }
$dir=Split-Path -Parent $Output; if ($dir) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
$lines | Set-Content -LiteralPath $Output -Encoding UTF8
Write-Output $Output
