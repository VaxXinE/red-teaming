#!/usr/bin/env bash
set -euo pipefail
umask 077

ROOT="${1:-recon-lab}"
if [[ -z "$ROOT" || "$ROOT" == "/" ]]; then
  echo "Refusing unsafe root path" >&2
  exit 2
fi

mkdir -p -- "$ROOT"/{00-scope,01-raw,02-normalized,03-assets,04-evidence,05-summary}
cat > "$ROOT/00-scope/README.md" <<'EOF'
# Recon Scope Notes

Training defaults:
- Public registration/DNS data for example.com is acceptable for learning.
- Direct probing is limited to localhost or assets you explicitly own/control.
- A discovered asset is a candidate, not automatic authorization.
EOF
cat > "$ROOT/03-assets/assets.csv" <<'EOF'
timestamp_utc,asset_type,value,source,scope_status,confidence,notes
EOF
printf 'Created recon workspace: %s\n' "$ROOT"
