#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="${1:-module22-threat-emulation}"
mkdir -p "$ROOT"/{00-scope,01-intel,02-mappings,03-navigator,04-flow,05-plan,06-telemetry,07-execution,08-results,09-evidence}
printf '%s\n' "workspace=$ROOT" "created=$(date -Is)"
