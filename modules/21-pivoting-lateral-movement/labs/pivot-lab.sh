#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB="$ROOT/pivot-lab"
EXT_NET="rt21_external"
INT_NET="rt21_internal"
ATTACKER="rt21-attacker"
JUMP="rt21-jump"
WEB="rt21-web"
SSH_TARGET="rt21-internal-ssh"

build() {
  docker build -t rt21-attacker-img "$LAB/attacker"
  docker build -t rt21-jump-img "$LAB/jump"
  docker build -t rt21-ssh-img "$LAB/internal-ssh"
  docker build -t rt21-web-img "$LAB/web"
}

create() {
  cleanup >/dev/null 2>&1 || true
  docker network create --driver bridge --subnet 172.31.210.0/24 "$EXT_NET" >/dev/null
  docker network create --driver bridge --internal --subnet 172.31.211.0/24 "$INT_NET" >/dev/null

  docker run -d --name "$ATTACKER" --hostname attacker \
    --network "$EXT_NET" --ip 172.31.210.10 \
    --cap-drop ALL --security-opt no-new-privileges:true \
    rt21-attacker-img >/dev/null

  docker run -d --name "$JUMP" --hostname jump \
    --network "$EXT_NET" --ip 172.31.210.20 \
    rt21-jump-img >/dev/null
  docker network connect --ip 172.31.211.20 "$INT_NET" "$JUMP"

  docker run -d --name "$WEB" --hostname internal-web \
    --network "$INT_NET" --ip 172.31.211.30 \
    --read-only --tmpfs /var/cache/nginx --tmpfs /var/run \
    rt21-web-img >/dev/null

  docker run -d --name "$SSH_TARGET" --hostname internal-ssh \
    --network "$INT_NET" --ip 172.31.211.40 \
    rt21-ssh-img >/dev/null

  echo "Lab created. Enter attacker with: $0 shell"
}

status() {
  docker ps --filter "name=rt21-" --format 'table {{.Names}}\t{{.Status}}\t{{.Networks}}'
  echo
  docker network inspect "$EXT_NET" "$INT_NET" --format '{{.Name}} -> {{range .Containers}}{{.Name}}={{.IPv4Address}} {{end}}' 2>/dev/null || true
}

shell() {
  docker exec -it "$ATTACKER" bash
}

jump_shell() {
  docker exec -it "$JUMP" bash
}

cleanup() {
  docker rm -f "$ATTACKER" "$JUMP" "$WEB" "$SSH_TARGET" >/dev/null 2>&1 || true
  docker network rm "$EXT_NET" "$INT_NET" >/dev/null 2>&1 || true
}

case "${1:-}" in
  build) build ;;
  create) create ;;
  status) status ;;
  shell) shell ;;
  jump-shell) jump_shell ;;
  cleanup) cleanup ;;
  *) echo "Usage: $0 {build|create|status|shell|jump-shell|cleanup}" >&2; exit 1 ;;
esac
