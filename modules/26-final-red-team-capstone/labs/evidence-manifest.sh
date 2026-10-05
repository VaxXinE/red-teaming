#!/usr/bin/env bash
set -euo pipefail
root="${1:?usage: evidence-manifest.sh <evidence-dir> <output>}"; out="${2:?output required}"
mkdir -p "$(dirname "$out")"
tmp="$(mktemp)"; trap 'rm -f "$tmp"' EXIT
find "$root" -type f -print0 | sort -z | xargs -0 -r sha256sum > "$tmp"
install -m 600 "$tmp" "$out"
printf 'manifest: %s (%s files)\n' "$out" "$(wc -l < "$out")"
