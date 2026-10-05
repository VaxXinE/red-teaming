#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-module22-threat-emulation}"
OUT="${2:-$ROOT/09-evidence/sha256-manifest.txt}"
mkdir -p "$(dirname "$OUT")"
find "$ROOT" -type f ! -path "$OUT" -print0 | sort -z | xargs -0 sha256sum > "$OUT"
chmod 600 "$OUT"
printf 'manifest=%s\n' "$OUT"
