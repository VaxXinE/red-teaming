Import-Module ActiveDirectory -ErrorAction Stop
$OutDir = Join-Path $PWD 'module20-ad-paths\05-trust'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$path = Join-Path $OutDir 'trusts.csv'
Get-ADTrust -Filter * | Select-Object Name,Source,Target,Direction,TrustType,ForestTransitive,IntraForest,SelectiveAuthentication,SIDFilteringForestAware,SIDFilteringQuarantined | Export-Csv -NoTypeInformation -Encoding UTF8 $path
Write-Host "Saved read-only trust inventory to $path"
