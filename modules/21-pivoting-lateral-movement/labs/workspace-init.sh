#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="${1:-module21-pivoting}"
mkdir -p "$ROOT"/{00-scope,01-topology,02-routing,03-tunnels,04-enum,05-lateral,06-evidence,07-cleanup,08-report}
printf '%s\n' \
  'Authorized training only.' \
  'Record allowed Docker lab names/subnets and stop conditions here.' \
  > "$ROOT/00-scope/README.txt"
printf '%s\n' "Created $ROOT"
