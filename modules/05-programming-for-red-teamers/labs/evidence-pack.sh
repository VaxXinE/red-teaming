#!/usr/bin/env bash
# Module 05 - evidence-pack.sh
# Safely package a directory you own and create a SHA-256 manifest.
set -euo pipefail
umask 077

usage() {
  printf 'Usage: %s <input-directory> <output-directory>\n' "$0" >&2
}

[[ $# -eq 2 ]] || { usage; exit 64; }
input=$1
output=$2

[[ -d "$input" ]] || { printf 'Input is not a directory: %s\n' "$input" >&2; exit 66; }
mkdir -p -- "$output"

input_abs=$(realpath -- "$input")
output_abs=$(realpath -- "$output")
[[ "$input_abs" != / ]] || { printf 'Refusing to package /\n' >&2; exit 65; }

stamp=$(date -u +'%Y%m%dT%H%M%SZ')
base=$(basename -- "$input_abs")
archive="$output_abs/${base}-${stamp}.tar.gz"
manifest="$output_abs/${base}-${stamp}.sha256"

tar -C "$(dirname -- "$input_abs")" -czf "$archive" -- "$base"
sha256sum -- "$archive" > "$manifest"
printf 'Archive : %s\nManifest: %s\n' "$archive" "$manifest"
