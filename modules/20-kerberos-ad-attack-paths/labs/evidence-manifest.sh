#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="${1:-module20-ad-paths}"
OUT="${2:-$ROOT/08-evidence/evidence-manifest.sha256}"
mkdir -p "$(dirname "$OUT")"
find "$ROOT" -type f ! -path "$OUT" -print0 | sort -z | xargs -0 sha256sum > "$OUT"
chmod 600 "$OUT"
printf 'Wrote %s\n' "$OUT"
