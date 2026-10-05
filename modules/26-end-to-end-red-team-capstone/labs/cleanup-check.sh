#!/usr/bin/env bash
set -euo pipefail
bad=0
if command -v docker >/dev/null 2>&1; then
  if docker ps -a --format '{{.Names}}' | grep -q '^capstone26-'; then echo 'FAIL: capstone26 containers remain'; bad=1; else echo 'PASS: no capstone26 containers'; fi
  if docker network ls --format '{{.Name}}' | grep -q '^capstone26_'; then echo 'FAIL: capstone26 networks remain'; bad=1; else echo 'PASS: no capstone26 networks'; fi
else
  echo 'INFO: docker unavailable; container cleanup not testable here'
fi
if ss -ltn 2>/dev/null | grep -Eq '127\.0\.0\.1:(9081|1080)'; then echo 'FAIL: training tunnel listener remains'; bad=1; else echo 'PASS: no known training tunnel listeners'; fi
exit "$bad"
