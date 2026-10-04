#!/usr/bin/env bash
set -euo pipefail
IMAGE='redteam-module16-linux-privesc:local'
NAME='mod16-linux-privesc'
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LABDIR="$HERE/linux-privesc-lab"
cmd="${1:-help}"
need_docker(){ command -v docker >/dev/null 2>&1 || { echo 'docker not found' >&2; exit 1; }; }
case "$cmd" in
  build)
    need_docker
    sudo docker build -t "$IMAGE" "$LABDIR"
    ;;
  create)
    need_docker
    sudo docker rm -f "$NAME" >/dev/null 2>&1 || true
    sudo docker run -d --name "$NAME" \
      --network none \
      --pids-limit 256 \
      --memory 256m \
      --cpus 1 \
      --cap-add DAC_READ_SEARCH \
      "$IMAGE" >/dev/null
    echo "created $NAME"
    ;;
  shell)
    need_docker
    sudo docker exec -it --user trainee -w /home/trainee "$NAME" bash
    ;;
  root-shell)
    echo 'root-shell action intentionally not provided; use minimum proof inside lab.' >&2
    exit 2
    ;;
  status)
    need_docker
    sudo docker ps -a --filter "name=^/${NAME}$"
    ;;
  evidence)
    need_docker
    OUT="${2:-module16-privesc/04-evidence}"
    mkdir -p "$OUT"; chmod 700 "$OUT"
    sudo docker exec --user trainee "$NAME" sh -lc 'id; uname -a; sudo -l 2>&1; echo "--- SUID ---"; find / -xdev -perm -4000 -type f 2>/dev/null; echo "--- CAPS ---"; getcap -r / 2>/dev/null; echo "--- CRON ---"; cat /etc/cron.d/mod16-maintenance 2>/dev/null; echo "--- APP CONFIG META ---"; stat -c "%A %U:%G %n" /opt/app/config.env' > "$OUT/manual-enum.txt"
    chmod 600 "$OUT/manual-enum.txt"
    echo "wrote $OUT/manual-enum.txt"
    ;;
  reset)
    "$0" create
    ;;
  cleanup)
    need_docker
    sudo docker rm -f "$NAME" >/dev/null 2>&1 || true
    echo "removed $NAME"
    ;;
  *)
    cat <<EOF
usage: $0 {build|create|shell|status|evidence [DIR]|reset|cleanup}

Safety: disposable training container only; no host mounts, no Docker socket, no network.
EOF
    ;;
esac
