#!/usr/bin/env bash
set -euo pipefail
umask 077
dir="${1:-module15-credentials/05-evidence}"
out="${2:-module15-credentials/05-evidence/sha256-manifest.txt}"
mkdir -p "$(dirname "$out")"
: > "$out"
find "$dir" -type f ! -path "$out" -print0 | sort -z | xargs -0 -r sha256sum >> "$out"
chmod 600 "$out"
printf '%s\n' "manifest: $out"
