#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <server> <DOMAIN/user> <output-file>" >&2
  exit 2
fi
SERVER="$1"; USER="$2"; OUT="$3"
mkdir -p "$(dirname "$OUT")"
echo "smbclient will request the password interactively." >&2
{
  printf 'timestamp=%s\nserver=%s\nidentity=%s\n\n' "$(date -Is)" "$SERVER" "$USER"
  smbclient -L "//$SERVER" -U "$USER"
} > "$OUT"
chmod 600 "$OUT"
echo "Wrote $OUT"
