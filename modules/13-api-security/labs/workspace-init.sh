#!/usr/bin/env bash
set -euo pipefail
umask 077
root="${1:-module13-api-security}"
mkdir -p "$root"/{00-scope,01-recon,02-requests,03-responses,04-findings,05-evidence,06-summary}
printf '# Module 13 API Security\n\nAuthorized targets only.\n' > "$root/README.md"
printf 'created: %s\n' "$(date -Is)" > "$root/05-evidence/workspace-created.txt"
printf 'Workspace: %s\n' "$root"
