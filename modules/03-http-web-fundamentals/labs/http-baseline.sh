#!/usr/bin/env bash
set -euo pipefail
umask 077

TARGET="${1:-http://127.0.0.1:8083/api/profile}"
case "$TARGET" in
  http://127.0.0.1:*|http://localhost:*) ;;
  *) echo "Refusing non-local target: $TARGET" >&2; exit 2 ;;
esac

STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="http-baseline-$STAMP"
mkdir -m 700 "$OUT"

curl -sS -D "$OUT/headers.txt" "$TARGET" -o "$OUT/body.bin"
sha256sum "$OUT/headers.txt" "$OUT/body.bin" > "$OUT/SHA256SUMS"
printf 'target=%s\n' "$TARGET" > "$OUT/metadata.txt"

echo "Saved to $OUT"
