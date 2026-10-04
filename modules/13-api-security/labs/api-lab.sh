#!/usr/bin/env bash
set -euo pipefail
name="module13-api-lab"
image="module13-api-lab:local"
dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/api-lab"
cmd="${1:-status}"
case "$cmd" in
  build)
    sudo docker build -t "$image" "$dir" ;;
  create|start)
    sudo docker rm -f "$name" >/dev/null 2>&1 || true
    sudo docker run -d --rm \
      --name "$name" \
      --cap-drop ALL \
      --security-opt no-new-privileges:true \
      --read-only \
      --tmpfs /tmp:rw,noexec,nosuid,size=16m \
      -p 127.0.0.1:8130:8130 \
      "$image" >/dev/null
    printf 'Local API lab: http://127.0.0.1:8130\n' ;;
  status)
    sudo docker ps --filter "name=^/${name}$" ;;
  logs)
    sudo docker logs "$name" ;;
  cleanup|stop)
    sudo docker rm -f "$name" >/dev/null 2>&1 || true
    printf 'Lab container removed.\n' ;;
  *)
    printf 'Usage: %s {build|create|status|logs|cleanup}\n' "$0" >&2; exit 2 ;;
esac
