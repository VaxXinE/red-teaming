#!/usr/bin/env bash
set -euo pipefail
FILE="${1:?usage: sliver-verify.sh /path/to/sliver-server}"
SIG="${FILE}.minisig"
PUB='RWTZPg959v3b7tLG7VzKHRB1/QT+d3c71Uzetfa44qAoX5rH7mGoQTTR'
command -v minisign >/dev/null || { echo 'minisign not installed'; exit 2; }
[[ -f "$FILE" ]] || { echo "file not found: $FILE"; exit 2; }
[[ -f "$SIG" ]] || { echo "signature not found: $SIG"; exit 2; }
minisign -Vm "$FILE" -P "$PUB"
