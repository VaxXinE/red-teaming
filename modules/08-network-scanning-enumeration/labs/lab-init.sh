#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="${1:-module08-enum}"
[[ -n "$ROOT" && "$ROOT" != "/" ]] || { echo "Unsafe path" >&2; exit 2; }
mkdir -p -- "$ROOT"/{00-scope,01-discovery,02-scans,03-manual,04-inventory,05-evidence,06-summary}
cat > "$ROOT/00-scope/README.md" <<'EOF'
# Module 08 Scope
Allowed targets for the included labs:
- 127.0.0.0/8
- Docker training subnet 172.31.80.0/24 created by multi-service-lab.sh
Do not repurpose these commands against networks you do not own or have explicit authorization to test.
EOF
printf 'Created %s
' "$ROOT"
