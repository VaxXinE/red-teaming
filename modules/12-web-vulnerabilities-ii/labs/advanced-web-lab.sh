#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
IMAGE="redteam-module12:local"
NAME="redteam-module12"
case "${1:-}" in
  build)
    sudo docker build -t "$IMAGE" "$DIR/advanced-web-lab"
    ;;
  create|start)
    sudo docker rm -f "$NAME" >/dev/null 2>&1 || true
    sudo docker run -d --rm \
      --name "$NAME" \
      --cap-drop ALL \
      --security-opt no-new-privileges:true \
      --read-only \
      --tmpfs /tmp:rw,noexec,nosuid,size=32m \
      -p 127.0.0.1:8120:8120 \
      "$IMAGE"
    echo "Local lab: http://127.0.0.1:8120/"
    ;;
  status)
    sudo docker ps --filter "name=^/${NAME}$"
    ;;
  cleanup|stop)
    sudo docker rm -f "$NAME" >/dev/null 2>&1 || true
    ;;
  *)
    echo "usage: $0 {build|create|status|cleanup}" >&2; exit 2
    ;;
esac
