#!/usr/bin/env bash
set -euo pipefail
NAME='module10-juice-shop'
IMAGE='bkimminich/juice-shop'
case "${1:-status}" in
  create)
    command -v docker >/dev/null || { echo 'docker not found' >&2; exit 3; }
    sudo docker rm -f "$NAME" >/dev/null 2>&1 || true
    sudo docker run -d --rm --name "$NAME" -p 127.0.0.1:3000:3000 "$IMAGE"
    echo 'Juice Shop: http://127.0.0.1:3000/'
    ;;
  status) sudo docker ps --filter "name=^/${NAME}$" --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' ;;
  logs) sudo docker logs --tail 60 "$NAME" ;;
  cleanup) sudo docker rm -f "$NAME" >/dev/null 2>&1 || true; echo 'cleaned up' ;;
  *) echo "usage: $0 {create|status|logs|cleanup}" >&2; exit 2 ;;
esac
