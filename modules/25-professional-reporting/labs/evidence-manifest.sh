#!/usr/bin/env bash
set -euo pipefail
umask 077
root="${1:-module25-reporting/02-evidence}"
out="${2:-module25-reporting/06-qa/evidence-manifest.sha256}"
mkdir -p "$(dirname "$out")"
: > "$out"
if [ -d "$root" ]; then
  while IFS= read -r -d '' f; do
    sha256sum "$f" >> "$out"
  done < <(find "$root" -type f -print0 | sort -z)
fi
chmod 600 "$out"
printf 'Wrote %s\n' "$out"
