#!/usr/bin/env bash
set -euo pipefail
out="${1:-linux-telemetry.txt}"
umask 077
{
  echo '=== UTC ==='; date -u +%FT%TZ
  echo '=== PROCESS ==='; ps -eo pid,ppid,user,comm,args --sort=pid | head -80
  echo '=== SOCKETS ==='; ss -tulpn 2>&1 || true
  echo '=== JOURNAL (15m) ==='; journalctl --since '-15 min' --no-pager 2>&1 | tail -200 || true
  echo '=== AUDIT STATUS ==='; command -v auditctl >/dev/null && sudo -n auditctl -s 2>&1 || echo 'audit tooling unavailable or privilege not granted'
} > "$out"
chmod 600 "$out"
printf '%s\n' "$out"
