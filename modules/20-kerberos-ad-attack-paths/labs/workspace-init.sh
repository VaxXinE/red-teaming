#!/usr/bin/env bash
set -euo pipefail
umask 077

ROOT="${1:-module20-ad-paths}"
mkdir -p "$ROOT"/{00-scope,01-kerberos,02-spn,03-delegation,04-acl,05-trust,06-adcs,07-bloodhound,08-evidence,09-findings,10-summary}
cat > "$ROOT/00-scope/README.txt" <<'TXT'
Authorized training only. Record domain/lab name, testing window, permitted hosts, and stop conditions here.
TXT
chmod -R go-rwx "$ROOT"
printf 'Created %s\n' "$ROOT"
