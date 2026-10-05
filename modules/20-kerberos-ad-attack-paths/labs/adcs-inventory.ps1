Import-Module ActiveDirectory -ErrorAction Stop
$OutDir = Join-Path $PWD 'module20-ad-paths\06-adcs'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$root = Get-ADRootDSE
$config = $root.configurationNamingContext
$enrollBase = "CN=Enrollment Services,CN=Public Key Services,CN=Services,$config"
$templateBase = "CN=Certificate Templates,CN=Public Key Services,CN=Services,$config"
Get-ADObject -SearchBase $enrollBase -LDAPFilter '(objectClass=pKIEnrollmentService)' -Properties dNSHostName,certificateTemplates | Select-Object Name,dNSHostName,certificateTemplates | Export-Csv -NoTypeInformation -Encoding UTF8 (Join-Path $OutDir 'cas.csv')
Get-ADObject -SearchBase $templateBase -LDAPFilter '(objectClass=pKICertificateTemplate)' -Properties displayName,pKIExtendedKeyUsage,msPKI-Certificate-Name-Flag,msPKI-Enrollment-Flag | Select-Object Name,displayName,pKIExtendedKeyUsage,msPKI-Certificate-Name-Flag,msPKI-Enrollment-Flag | Export-Csv -NoTypeInformation -Encoding UTF8 (Join-Path $OutDir 'templates.csv')
Write-Host "Saved read-only AD CS inventory under $OutDir"
