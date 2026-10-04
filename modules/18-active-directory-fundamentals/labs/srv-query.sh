#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "usage: $0 <private-dns-server-ip> <domain> [output-file]" >&2
  exit 2
fi
server="$1"; domain="$2"; out="${3:-dns-srv-${domain}.txt}"
python - "$server" <<'PY'
import ipaddress, sys
ip=ipaddress.ip_address(sys.argv[1])
if not (ip.is_private or ip.is_loopback):
    raise SystemExit('refusing non-private DNS server; use your isolated lab DNS/DC')
PY
mkdir -p "$(dirname "$out")"
{
  echo "# Module 18 AD SRV inventory"
  echo "# dns_server=$server domain=$domain"
  for q in \
    "_ldap._tcp.dc._msdcs.$domain" \
    "_kerberos._tcp.$domain" \
    "_gc._tcp.$domain"; do
    echo
    echo "## $q"
    dig "@$server" +noall +answer "$q" SRV
  done
} > "$out"
chmod 600 "$out"
printf 'wrote %s\n' "$out"
