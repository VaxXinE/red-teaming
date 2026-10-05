#!/usr/bin/env bash
set -euo pipefail
ATTACKER="rt21-attacker"

echo '== attacker routes =='
docker exec "$ATTACKER" ip route

echo
echo '== jump reachable on external network =='
docker exec "$ATTACKER" bash -lc 'nc -zvw2 172.31.210.20 22'

echo
echo '== internal web direct access should fail =='
if docker exec "$ATTACKER" bash -lc 'curl -fsS --connect-timeout 2 http://172.31.211.30/ >/dev/null'; then
  echo 'UNEXPECTED: direct internal access succeeded' >&2
  exit 1
else
  echo 'PASS: attacker cannot directly reach internal web'
fi
