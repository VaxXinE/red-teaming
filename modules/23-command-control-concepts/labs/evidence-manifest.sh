#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-module23-c2}"
OUT="$ROOT/evidence/manifest.sha256"
mkdir -p "$ROOT/evidence"
: > "$OUT"
while IFS= read -r -d '' f; do
  [[ "$f" == "$OUT" ]] && continue
  sha256sum "$f" >> "$OUT"
done < <(find "$ROOT" -type f -print0 | sort -z)
chmod 600 "$OUT"
echo "[+] wrote $OUT"
