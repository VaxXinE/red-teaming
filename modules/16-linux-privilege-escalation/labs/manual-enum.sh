#!/usr/bin/env bash
set -euo pipefail
umask 077
OUT="${1:-manual-enum.txt}"
{
  echo '=== identity ==='; id; groups || true
  echo; echo '=== os ==='; uname -a; cat /etc/os-release 2>/dev/null || true
  echo; echo '=== sudo ==='; sudo -l 2>&1 || true
  echo; echo '=== suid ==='; find / -xdev -perm -4000 -type f 2>/dev/null || true
  echo; echo '=== sgid ==='; find / -xdev -perm -2000 -type f 2>/dev/null || true
  echo; echo '=== capabilities ==='; getcap -r / 2>/dev/null || true
  echo; echo '=== mounts ==='; findmnt -o TARGET,SOURCE,FSTYPE,OPTIONS 2>/dev/null || true
  echo; echo '=== processes ==='; ps auxww --forest 2>/dev/null | head -n 100 || true
  echo; echo '=== listeners ==='; ss -lntup 2>/dev/null || true
  echo; echo '=== cron ==='; cat /etc/crontab 2>/dev/null || true; ls -la /etc/cron.d 2>/dev/null || true
  echo; echo '=== path ==='; printf '%s\n' "${PATH:-}" | tr ':' '\n'
} > "$OUT"
chmod 600 "$OUT"
printf 'Wrote %s\n' "$OUT"
