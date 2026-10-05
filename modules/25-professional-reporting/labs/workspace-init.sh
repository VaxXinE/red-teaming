#!/usr/bin/env bash
set -euo pipefail
umask 077
name="${1:-module25-reporting}"
mkdir -p "$name"/{00-admin,01-notes,02-evidence/screenshots,02-evidence/raw,03-findings,04-report,05-retest,06-qa}
printf '%s\n' '# Module 25 Reporting Workspace' > "$name/README.md"
printf '%s\n' "created_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$name/README.md"
find "$name" -type d -exec chmod 700 {} +
printf 'Created %s\n' "$name"
