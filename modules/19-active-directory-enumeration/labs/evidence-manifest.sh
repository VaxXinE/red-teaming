#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="${1:-module19-ad-enum}"
[[ -d "$ROOT" ]] || { echo "Not a directory: $ROOT" >&2; exit 2; }
OUT="$ROOT/10-evidence/manifest.sha256"
mkdir -p "$(dirname "$OUT")"
find "$ROOT" -type f ! -path "$OUT" -print0 | sort -z | xargs -0 sha256sum > "$OUT"
chmod 600 "$OUT"
echo "Wrote $OUT"
