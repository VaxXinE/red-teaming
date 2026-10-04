#!/usr/bin/env bash
set -euo pipefail
NAME="recon07-web"
PORT="8087"
case "${1:-status}" in
  create)
    sudo docker rm -f "$NAME" >/dev/null 2>&1 || true
    sudo docker run -d --rm --name "$NAME" -p "127.0.0.1:${PORT}:80" nginx:alpine >/dev/null
    printf 'Local lab: http://127.0.0.1:%s/\n' "$PORT"
    ;;
  status)
    sudo docker ps --filter "name=^/${NAME}$" --format 'table {{.Names}}\t{{.Ports}}\t{{.Status}}'
    ;;
  headers)
    curl -sS -D - -o /dev/null "http://127.0.0.1:${PORT}/"
    ;;
  cleanup)
    sudo docker rm -f "$NAME" >/dev/null 2>&1 || true
    echo "Lab cleaned"
    ;;
  *) echo "usage: $0 {create|status|headers|cleanup}" >&2; exit 2;;
esac
