#!/usr/bin/env bash
set -euo pipefail
umask 077
root="${1:-module18-ad}"
mkdir -p "$root"/{00-scope,01-raw,02-normalized,03-notes,04-report,05-evidence}
cat > "$root/00-scope/README.md" <<'TXT'
# Module 18 AD Lab Scope

Use only your own isolated AD lab, GOAD/MINILAB, or an authorized training platform.
Do not store real credentials, Kerberos ticket material, private keys, or production data here.
TXT
printf 'workspace: %s\n' "$root"
find "$root" -maxdepth 1 -type d -print
