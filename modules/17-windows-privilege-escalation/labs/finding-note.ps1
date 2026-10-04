param(
 [Parameter(Mandatory=$true)][string]$Path,
 [Parameter(Mandatory=$true)][string]$Title,
 [string]$Asset='Windows training VM',
 [string]$Evidence='',
 [string]$Impact='',
 [string]$Remediation=''
)
$ErrorActionPreference='Stop'
$parent=Split-Path -Parent $Path
if ($parent) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
@"
# $Title

- Asset: $Asset
- Status: validated-in-training-lab

## Evidence
$Evidence

## Root cause
Describe the exact trust/permission mistake. Avoid calling a tool output a finding by itself.

## Impact
$Impact

## Remediation
$Remediation

## Cleanup / retest
Document what was restored and how the fix was verified.
"@ | Set-Content -Encoding UTF8 $Path
Write-Host "Wrote: $Path"
