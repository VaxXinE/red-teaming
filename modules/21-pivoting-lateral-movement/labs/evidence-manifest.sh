#!/usr/bin/env bash
set -euo pipefail
DIR="${1:-module21-pivoting/06-evidence}"
OUT="${2:-module21-pivoting/06-evidence/sha256-manifest.txt}"
mkdir -p "$(dirname "$OUT")"
find "$DIR" -type f ! -path "$OUT" -print0 | sort -z | xargs -0 -r sha256sum > "$OUT"
chmod 600 "$OUT"
echo "Wrote $OUT"
