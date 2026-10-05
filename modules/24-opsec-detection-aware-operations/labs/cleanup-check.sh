#!/usr/bin/env bash
set -euo pipefail
w="${1:-module24-opsec}"
failed=0
if pgrep -f '^python(3)? .*benign-activity.py' >/dev/null 2>&1; then echo 'FAIL: benign-activity.py still running'; failed=1; else echo 'PASS: no benign simulator process'; fi
if [[ -e "$w/tmp/RTLAB24_MARKER.txt" ]]; then echo 'FAIL: marker file remains'; failed=1; else echo 'PASS: marker file absent'; fi
if ss -ltn 2>/dev/null | grep -qE ':8240\b'; then echo 'WARN: port 8240 listener exists; verify ownership'; else echo 'PASS: no expected lab listener on 8240'; fi
exit "$failed"
