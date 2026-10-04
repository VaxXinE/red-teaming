#!/usr/bin/env bash
set -euo pipefail
DIR="${1:-module16-privesc/04-evidence}"
[[ -d "$DIR" ]] || { echo "Evidence directory not found: $DIR" >&2; exit 1; }
OUT="${DIR%/}/SHA256SUMS"
find "$DIR" -maxdepth 1 -type f ! -name 'SHA256SUMS' -print0 | sort -z | xargs -0 -r sha256sum > "$OUT"
chmod 600 "$OUT"
printf 'Wrote %s\n' "$OUT"
