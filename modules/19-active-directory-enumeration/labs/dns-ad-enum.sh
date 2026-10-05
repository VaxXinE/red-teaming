#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <domain> <output-file>" >&2
  exit 2
fi
DOMAIN="$1"; OUT="$2"
mkdir -p "$(dirname "$OUT")"
{
  printf 'timestamp=%s\n' "$(date -Is)"
  printf 'domain=%s\n\n' "$DOMAIN"
  echo '[LDAP DC SRV]'
  dig +short SRV "_ldap._tcp.dc._msdcs.${DOMAIN}"
  echo '[KERBEROS SRV]'
  dig +short SRV "_kerberos._tcp.${DOMAIN}"
  echo '[DOMAIN A/AAAA]'
  dig +short A "$DOMAIN"
  dig +short AAAA "$DOMAIN"
} > "$OUT"
chmod 600 "$OUT"
echo "Wrote $OUT"
