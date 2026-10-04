$ErrorActionPreference = 'Continue'
$keys = @(
  'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run',
  'HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce',
  'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run',
  'HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce'
)
foreach ($k in $keys) {
  Write-Host "`n=== $k ==="
  if (Test-Path $k) { Get-ItemProperty $k | Format-List } else { Write-Host '(not present)' }
}
