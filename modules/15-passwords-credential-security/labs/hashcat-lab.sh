#!/usr/bin/env bash
set -euo pipefail
here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
hashes="$here/fixtures/hashcat-sha512crypt.txt"
words="$here/fixtures/lab-wordlist.txt"
command -v hashcat >/dev/null || { echo 'hashcat is not installed. On Omarchy: omarchy pkg add hashcat' >&2; exit 1; }
mkdir -p "$here/.hashcat-home" "$here/.hashcat-session"
export HOME="$here/.hashcat-home"
chmod 700 "$HOME" "$here/.hashcat-session"
cd "$here/.hashcat-session"
exec hashcat -m 1800 -a 0 --session module15 --potfile-path module15.potfile "$hashes" "$words"
