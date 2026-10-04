#!/usr/bin/env bash
set -euo pipefail
NETWORK="redlab08"
SUBNET="172.31.80.0/24"
BASE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

need() { command -v "$1" >/dev/null || { echo "Missing dependency: $1" >&2; exit 3; }; }
need docker

action="${1:-status}"
case "$action" in
  create)
    sudo docker network inspect "$NETWORK" >/dev/null 2>&1 || sudo docker network create --driver bridge --subnet "$SUBNET" "$NETWORK" >/dev/null
    sudo docker rm -f redlab08-nginx redlab08-apache redlab08-redis redlab08-udp >/dev/null 2>&1 || true
    sudo docker run -d --rm --name redlab08-nginx --network "$NETWORK" --ip 172.31.80.10 nginx:alpine >/dev/null
    sudo docker run -d --rm --name redlab08-apache --network "$NETWORK" --ip 172.31.80.11 httpd:alpine >/dev/null
    sudo docker run -d --rm --name redlab08-redis --network "$NETWORK" --ip 172.31.80.12 redis:alpine redis-server --save '' --appendonly no --protected-mode no >/dev/null
    sudo docker run -d --rm --name redlab08-udp --network "$NETWORK" --ip 172.31.80.13 -v "$BASE_DIR/udp-echo.py:/lab/udp-echo.py:ro" python:3-alpine python /lab/udp-echo.py --host 0.0.0.0 --port 9999 >/dev/null
    echo "Created isolated lab on $SUBNET. No service is published to a host/LAN port."
    ;;
  status)
    sudo docker network inspect "$NETWORK" --format '{{range $id,$c := .Containers}}{{$c.Name}} {{$c.IPv4Address}}{{println}}{{end}}' 2>/dev/null || echo "Lab network not present"
    ;;
  cleanup)
    sudo docker rm -f redlab08-nginx redlab08-apache redlab08-redis redlab08-udp >/dev/null 2>&1 || true
    sudo docker network rm "$NETWORK" >/dev/null 2>&1 || true
    echo "Lab removed"
    ;;
  *) echo "Usage: $0 {create|status|cleanup}" >&2; exit 2;;
esac
