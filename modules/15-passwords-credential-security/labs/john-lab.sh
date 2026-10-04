#!/usr/bin/env bash
set -euo pipefail
here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
hashes="$here/fixtures/john-sha512crypt.txt"
words="$here/fixtures/lab-wordlist.txt"
command -v john >/dev/null || { echo 'john is not installed. On Omarchy: omarchy pkg add john' >&2; exit 1; }
mkdir -p "$here/.john-home"
export HOME="$here/.john-home"
chmod 700 "$HOME"
exec john --format=sha512crypt --wordlist="$words" "$hashes"
