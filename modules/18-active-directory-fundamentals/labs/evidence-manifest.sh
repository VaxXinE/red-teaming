#!/usr/bin/env bash
set -euo pipefail
umask 077
root="${1:-module18-ad}"
[[ -d "$root" ]] || { echo "missing directory: $root" >&2; exit 2; }
out="$root/05-evidence/sha256-manifest.txt"
mkdir -p "$(dirname "$out")"
find "$root" -type f ! -path "$out" -print0 | sort -z | xargs -0 sha256sum > "$out"
chmod 600 "$out"
printf 'wrote %s\n' "$out"
