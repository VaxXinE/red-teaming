#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="${1:-module19-ad-enum}"
mkdir -p "$ROOT"/{00-scope,01-dns,02-ldap,03-powershell,04-relations,05-smb,06-gpo,07-acl,08-trusts,09-graph,10-evidence,11-summary}
printf '# Module 19 AD Enumeration Activity Log\n\n' > "$ROOT/10-evidence/activity-log.md"
printf 'Workspace created: %s\n' "$ROOT"
