#!/usr/bin/env bash
set -euo pipefail
NAME='module11-vuln-web'
IMAGE='module11-vuln-web:local'
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/vuln-web-lab"
case "${1:-status}" in
  build)
    sudo docker build -t "$IMAGE" "$DIR"
    ;;
  create)
    sudo docker image inspect "$IMAGE" >/dev/null 2>&1 || sudo docker build -t "$IMAGE" "$DIR"
    sudo docker rm -f "$NAME" >/dev/null 2>&1 || true
    sudo docker run -d --rm \
      --name "$NAME" \
      --cap-drop ALL \
      --security-opt no-new-privileges:true \
      --read-only \
      --tmpfs /tmp:rw,noexec,nosuid,size=64m \
      -p 127.0.0.1:8111:8111 \
      "$IMAGE"
    echo 'Lab: http://127.0.0.1:8111/'
    ;;
  status)
    sudo docker ps --filter "name=^/${NAME}$" --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
    ;;
  logs)
    sudo docker logs --tail 80 "$NAME"
    ;;
  cleanup)
    sudo docker rm -f "$NAME" >/dev/null 2>&1 || true
    echo 'cleaned up'
    ;;
  *) echo "usage: $0 {build|create|status|logs|cleanup}" >&2; exit 2 ;;
esac
