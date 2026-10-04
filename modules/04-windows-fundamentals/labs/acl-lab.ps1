# Module 04 - NTFS ACL practice lab
# Creates and removes files ONLY inside the current user's Documents folder.

[CmdletBinding()]
param(
    [ValidateSet('create','status','cleanup')]
    [string]$Action = 'status'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = "$env:USERPROFILE\Documents\RedTeam\Module04\acl-lab"

switch ($Action) {
    'create' {
        New-Item -ItemType Directory -Path $Root -Force | Out-Null
        'Public training file' | Set-Content -Path (Join-Path $Root 'public.txt') -Encoding utf8
        'Private training file' | Set-Content -Path (Join-Path $Root 'private.txt') -Encoding utf8
        Write-Host "Created: $Root"
        Write-Host 'Use Get-Acl and icacls manually; this helper does not weaken permissions automatically.'
    }
    'status' {
        if (-not (Test-Path $Root)) { Write-Host 'Lab not created.'; break }
        Get-ChildItem -Force $Root
        Get-Acl $Root | Format-List Path, Owner, AccessToString
        icacls $Root
    }
    'cleanup' {
        if (Test-Path $Root) { Remove-Item -Recurse -Force $Root }
        Write-Host 'ACL lab removed.'
    }
}
