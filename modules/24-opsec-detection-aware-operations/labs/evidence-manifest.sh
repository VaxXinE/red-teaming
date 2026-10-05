#!/usr/bin/env bash
set -euo pipefail
root="${1:-module24-opsec}"
out="${2:-$root/evidence/evidence-manifest.sha256}"
mkdir -p "$(dirname "$out")"
tmp="$(mktemp)"; trap 'rm -f "$tmp"' EXIT
find "$root" -type f ! -path "$out" -print0 | sort -z | xargs -0 -r sha256sum > "$tmp"
mv "$tmp" "$out"; chmod 600 "$out"; echo "$out"
