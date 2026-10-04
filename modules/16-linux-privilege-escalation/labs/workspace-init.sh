#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="${1:-module16-privesc}"
mkdir -p "$ROOT"/{01-enum,02-notes,03-findings,04-evidence,05-cleanup}
printf '%s\n' "# Module 16 - Linux Privilege Escalation" > "$ROOT/02-notes/notes.md"
printf '%s\n' "created_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$ROOT/04-evidence/workspace-created.txt"
printf 'Created %s\n' "$ROOT"
