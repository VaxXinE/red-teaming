#!/usr/bin/env bash
set -euo pipefail
umask 077

DOMAIN="${1:-example.com}"
OUT="${2:-dns-baseline.txt}"

if [[ ! "$DOMAIN" =~ ^([A-Za-z0-9-]+\.)+[A-Za-z]{2,63}$ ]]; then
  echo "Invalid domain name: $DOMAIN" >&2
  exit 2
fi

command -v dig >/dev/null || { echo "dig not found. Install package: bind" >&2; exit 3; }

{
  printf '# DNS baseline for %s\n' "$DOMAIN"
  printf '# Collected UTC: %s\n\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  for TYPE in A AAAA MX NS TXT CAA SOA; do
    printf '## %s\n' "$TYPE"
    dig +noall +answer "$DOMAIN" "$TYPE"
    printf '\n'
  done
} > "$OUT"
chmod 600 "$OUT"
printf 'Wrote %s\n' "$OUT"
