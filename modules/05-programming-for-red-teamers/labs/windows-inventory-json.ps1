# Module 05 - windows-inventory-json.ps1
# Read-only inventory for the Windows VM from Module 04.
[CmdletBinding()]
param(
    [string]$OutputPath = "$env:USERPROFILE\Documents\RedTeam\Module05\windows-inventory.json"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$parent = Split-Path -Parent $OutputPath
New-Item -ItemType Directory -Path $parent -Force | Out-Null

try {
    $listeners = Get-NetTCPConnection -State Listen -ErrorAction Stop |
        Sort-Object LocalPort |
        Select-Object LocalAddress, LocalPort, OwningProcess

    $data = [ordered]@{
        generatedAt = (Get-Date).ToUniversalTime().ToString('o')
        computer    = $env:COMPUTERNAME
        user        = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        powershell  = $PSVersionTable.PSVersion.ToString()
        listeners   = $listeners
        processes   = Get-Process | Sort-Object Id | Select-Object -First 30 Name, Id
    }

    $data | ConvertTo-Json -Depth 5 | Set-Content -Path $OutputPath -Encoding utf8
    $hash = Get-FileHash -Algorithm SHA256 -Path $OutputPath
    Write-Host "Wrote: $OutputPath"
    Write-Host "SHA256: $($hash.Hash)"
}
catch {
    Write-Error "Inventory failed: $($_.Exception.Message)"
    exit 1
}
