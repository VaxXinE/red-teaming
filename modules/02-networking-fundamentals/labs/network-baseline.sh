#!/usr/bin/env bash
set -euo pipefail
umask 077

OUT_DIR="${1:-$HOME/CyberSec/labs/module02/evidence}"
mkdir -p "$OUT_DIR"
OUT="$OUT_DIR/network-baseline-$(date +%Y%m%d-%H%M%S).txt"

{
  echo "=== HOST ==="
  hostname
  echo
  echo "=== ADDRESSES ==="
  ip -brief address
  echo
  echo "=== ROUTES IPv4 ==="
  ip route
  echo
  echo "=== ROUTES IPv6 ==="
  ip -6 route
  echo
  echo "=== NEIGHBORS ==="
  ip neigh
  echo
  echo "=== LISTENERS ==="
  ss -ltnu
  echo
  echo "=== RESOLVER ==="
  if command -v resolvectl >/dev/null 2>&1; then
    resolvectl status
  else
    cat /etc/resolv.conf
  fi
} > "$OUT"

chmod 600 "$OUT"
printf 'Saved: %s\n' "$OUT"
