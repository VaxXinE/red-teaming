#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="${1:-module11-web-vulns}"
[[ -n "$ROOT" && "$ROOT" != "/" ]] || { echo 'unsafe path' >&2; exit 2; }
mkdir -p -- "$ROOT"/{00-scope,01-baseline,02-sqli,03-xss,04-command-injection,05-path-traversal,06-file-upload,07-auth,08-access-control,09-evidence,10-findings}
printf '%s\n' 'IN SCOPE: http://127.0.0.1:8111/ and explicitly authorized PortSwigger labs.' > "$ROOT/00-scope/scope.txt"
printf 'Created %s\n' "$ROOT"
