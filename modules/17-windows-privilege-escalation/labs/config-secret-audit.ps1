param([string]$Root = 'C:\ProgramData')
$ErrorActionPreference = 'Continue'
$patterns = 'password|passwd|token|secret|api[_-]?key|credential'
$ext = '*.ini','*.conf','*.config','*.xml','*.json','*.yml','*.yaml','*.txt','*.ps1'
Get-ChildItem -Path $Root -File -Recurse -Include $ext -ErrorAction SilentlyContinue |
  Select-Object -First 250 |
  ForEach-Object {
    $m = Select-String -Path $_.FullName -Pattern $patterns -CaseSensitive:$false -ErrorAction SilentlyContinue
    if ($m) { [pscustomobject]@{ Path=$_.FullName; Matches=$m.Count } }
  } | Format-Table -AutoSize
Write-Host "`nThis script reports candidate files only; do not print secret values into notes or chat."
