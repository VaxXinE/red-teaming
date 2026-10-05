#!/usr/bin/env bash
set -euo pipefail
umask 077
root="${1:-module26-capstone}"
mkdir -p "$root"/{00-scope,01-raw,02-normalized,03-notes,04-findings,05-report,06-evidence,07-cleanup}
cat > "$root/00-scope/README.md" <<'TXT'
# Module 26 Capstone Scope

Use only the synthetic dataset shipped with this module or a lab/CTF/platform where you have explicit authorization.
Do not place real credentials, tokens, tickets, private keys, customer data, or production evidence in this training workspace.
TXT
printf 'workspace: %s\n' "$root"
find "$root" -maxdepth 1 -type d -print | sort
