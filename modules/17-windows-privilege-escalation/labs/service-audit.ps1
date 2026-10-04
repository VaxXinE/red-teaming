$ErrorActionPreference = 'Continue'
$services = Get-CimInstance Win32_Service | Where-Object { $_.PathName } | Sort-Object Name
$services | ForEach-Object {
    $s = $_
    $raw = [string]$s.PathName
    $exe = $null
    if ($raw -match '^"([^\"]+)"') { $exe = $Matches[1] }
    elseif ($raw -match '^([^ ]+\.exe)') { $exe = $Matches[1] }
    $exists = if ($exe) { Test-Path -LiteralPath $exe } else { $false }
    [pscustomobject]@{ Name=$s.Name; StartName=$s.StartName; State=$s.State; PathName=$raw; ParsedExe=$exe; ExeExists=$exists }
} | Format-Table -AutoSize
Write-Host "`nUse AccessChk or icacls on interesting service objects/files before making any conclusion."
