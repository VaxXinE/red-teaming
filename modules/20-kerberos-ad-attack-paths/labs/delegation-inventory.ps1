Import-Module ActiveDirectory -ErrorAction Stop
$OutDir = Join-Path $PWD 'module20-ad-paths\03-delegation'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$rows = @()
$rows += Get-ADComputer -Filter * -Properties TrustedForDelegation,TrustedToAuthForDelegation,msDS-AllowedToDelegateTo,PrincipalsAllowedToDelegateToAccount | ForEach-Object {
    [pscustomobject]@{
        Type='Computer'; Name=$_.Name
        Unconstrained=$_.TrustedForDelegation
        ProtocolTransition=$_.TrustedToAuthForDelegation
        AllowedToDelegateTo=($_.'msDS-AllowedToDelegateTo' -join ';')
        RBCDPrincipals=($_.PrincipalsAllowedToDelegateToAccount -join ';')
    }
}
$rows += Get-ADUser -LDAPFilter '(servicePrincipalName=*)' -Properties TrustedForDelegation,TrustedToAuthForDelegation,msDS-AllowedToDelegateTo,PrincipalsAllowedToDelegateToAccount | ForEach-Object {
    [pscustomobject]@{
        Type='User'; Name=$_.SamAccountName
        Unconstrained=$_.TrustedForDelegation
        ProtocolTransition=$_.TrustedToAuthForDelegation
        AllowedToDelegateTo=($_.'msDS-AllowedToDelegateTo' -join ';')
        RBCDPrincipals=($_.PrincipalsAllowedToDelegateToAccount -join ';')
    }
}
$path = Join-Path $OutDir 'delegation.csv'
$rows | Export-Csv -NoTypeInformation -Encoding UTF8 $path
Write-Host "Saved read-only delegation inventory to $path"
