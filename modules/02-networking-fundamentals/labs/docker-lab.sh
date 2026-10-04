#!/usr/bin/env bash
set -euo pipefail

NETWORK=redlab02
SUBNET=172.30.20.0/24
CONTAINER=redlab02-web
IP=172.30.20.10

case "${1:-status}" in
  create)
    sudo docker network inspect "$NETWORK" >/dev/null 2>&1 || \
      sudo docker network create --driver bridge --subnet "$SUBNET" "$NETWORK" >/dev/null
    sudo docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
    sudo docker run -d --rm --name "$CONTAINER" --network "$NETWORK" --ip "$IP" \
      -p 127.0.0.1:8088:80 nginx:alpine >/dev/null
    echo "Lab ready: http://127.0.0.1:8088 and $IP:80"
    ;;
  status)
    sudo docker network inspect "$NETWORK" 2>/dev/null || true
    sudo docker ps --filter "name=$CONTAINER"
    ;;
  cleanup)
    sudo docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
    sudo docker network rm "$NETWORK" >/dev/null 2>&1 || true
    echo "Lab removed."
    ;;
  *)
    echo "Usage: $0 {create|status|cleanup}" >&2
    exit 2
    ;;
esac
