#!/usr/bin/env bash
set -euo pipefail
umask 077
OUT="${1:-module22-threat-emulation/07-execution}"
mkdir -p "$OUT"
LOG="$OUT/activity.jsonl"
run() {
  local id="$1" name="$2"; shift 2
  local ts; ts="$(date -Is)"
  printf '{"time":"%s","technique":"%s","name":"%s","command":"%s"}\n' "$ts" "$id" "$name" "$*" >> "$LOG"
  "$@" > "$OUT/${id//./_}.txt" 2>&1 || true
}
run T1033 "System Owner/User Discovery" whoami
run T1082 "System Information Discovery" uname -a
run T1057 "Process Discovery" ps -eo pid,ppid,user,comm
if command -v getent >/dev/null 2>&1; then run T1087.001 "Local Account Discovery" getent passwd; else run T1087.001 "Local Account Discovery" sh -c 'cat /etc/passwd'; fi
chmod 600 "$LOG" "$OUT"/*.txt
printf 'Read-only discovery simulation completed. Evidence: %s\n' "$OUT"
