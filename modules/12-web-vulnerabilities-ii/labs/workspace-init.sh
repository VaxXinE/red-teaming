#!/usr/bin/env bash
set -euo pipefail
umask 077
root="${1:-module12-web-vulns-ii}"
mkdir -p "$root"/{00-scope,01-baseline,02-requests,03-responses,04-notes,05-findings,06-evidence,07-cleanup}
printf 'Module 12 authorized local / training lab only\n' > "$root/00-scope/README.txt"
printf 'Created %s\n' "$root"
