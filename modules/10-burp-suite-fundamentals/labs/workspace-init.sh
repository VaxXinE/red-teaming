#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="${1:-module10-burp}"
[[ -n "$ROOT" && "$ROOT" != "/" ]] || { echo "Unsafe path" >&2; exit 2; }
mkdir -p -- "$ROOT"/{00-scope,01-history,02-repeater,03-evidence,04-notes,05-summary}
cat > "$ROOT/00-scope/scope.txt" <<'EOF'
IN SCOPE
http://127.0.0.1:8090/
http://127.0.0.1:3000/

OUT OF SCOPE
Everything else unless separately authorized.
EOF
printf 'Created %s\n' "$ROOT"
