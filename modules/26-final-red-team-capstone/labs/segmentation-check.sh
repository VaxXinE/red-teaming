#!/usr/bin/env bash
set -euo pipefail
name=capstone26-attacker
exec_in(){ docker exec "$name" bash -lc "$1"; }
echo '[DMZ] edge-web should be reachable:'
exec_in "curl -fsS --max-time 2 http://10.26.10.20:8080/ >/dev/null && echo PASS || echo FAIL"
echo '[DMZ] jump SSH should be reachable:'
exec_in "nc -z -w2 10.26.10.30 22 && echo PASS || echo FAIL"
echo '[SEGMENT] internal API direct should NOT be reachable:'
if exec_in "nc -z -w2 10.26.20.40 8081" >/dev/null 2>&1; then echo 'FAIL: internal API reachable direct'; exit 1; else echo 'PASS: internal API not directly reachable'; fi
echo '[SEGMENT] internal SSH direct should NOT be reachable:'
if exec_in "nc -z -w2 10.26.20.50 22" >/dev/null 2>&1; then echo 'FAIL: internal SSH reachable direct'; exit 1; else echo 'PASS: internal SSH not directly reachable'; fi
