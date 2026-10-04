#!/usr/bin/env bash
set -euo pipefail

# Module 01 - Local System Survey
# Run only on a host you own or are explicitly authorized to assess.
# This script is intentionally read-only with respect to system configuration.

OUT_DIR=${1:-"$HOME/CyberSec/labs/module01/evidence"}
mkdir -p -- "$OUT_DIR"
chmod 700 -- "$OUT_DIR"
umask 077

STAMP=$(date -u +'%Y%m%dT%H%M%SZ')
OUT="$OUT_DIR/system-survey-$STAMP.txt"

section() {
  printf '\n===== %s =====\n' "$1"
}

{
  section 'TIME'
  date --iso-8601=seconds

  section 'IDENTITY'
  whoami
  id

  section 'HOST'
  hostnamectl 2>/dev/null || hostname
  uname -a
  printf '\n'
  cat /etc/os-release 2>/dev/null || true

  section 'FILESYSTEM'
  df -hT
  printf '\nMounts (first 30):\n'
  findmnt | head -n 30

  section 'PROCESS SNAPSHOT'
  ps -eo pid,ppid,user,stat,comm,args --sort=pid | head -n 40

  section 'FAILED SERVICES'
  systemctl --failed --no-pager 2>/dev/null || true

  section 'NETWORK'
  ip -brief address
  printf '\nRoutes:\n'
  ip route
  printf '\nListening sockets:\n'
  ss -lntup 2>/dev/null || ss -lntu

  section 'RECENT WARNINGS'
  journalctl -b -p warning -n 30 --no-pager 2>/dev/null || true
} > "$OUT"

chmod 600 -- "$OUT"
printf 'survey written to: %s\n' "$OUT"
