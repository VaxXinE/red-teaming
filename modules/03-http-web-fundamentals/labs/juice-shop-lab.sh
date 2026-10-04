#!/usr/bin/env bash
set -euo pipefail

NAME="module03-juice-shop"
IMAGE="bkimminich/juice-shop"
PORT="3000"

case "${1:-status}" in
  create)
    if sudo docker ps -a --format '{{.Names}}' | grep -qx "$NAME"; then
      echo "$NAME already exists; run cleanup first."
      exit 1
    fi
    sudo docker pull "$IMAGE"
    sudo docker run -d --rm \
      --name "$NAME" \
      -p "127.0.0.1:${PORT}:3000" \
      "$IMAGE"
    echo "Juice Shop: http://127.0.0.1:${PORT}"
    ;;
  status)
    sudo docker ps --filter "name=^/${NAME}$"
    ;;
  cleanup)
    sudo docker rm -f "$NAME" 2>/dev/null || true
    ;;
  *)
    echo "Usage: $0 {create|status|cleanup}" >&2
    exit 2
    ;;
esac
