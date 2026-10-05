#!/usr/bin/env bash
set -euo pipefail
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; C="$D/capstone-lab/compose.yml"
need(){ command -v docker >/dev/null 2>&1 || { echo 'docker is required'; exit 1; }; }
case "${1:-}" in
  build) need; docker compose -f "$C" build ;;
  create|up) need; docker compose -f "$C" up -d ;;
  status) need; docker compose -f "$C" ps ;;
  shell) need; docker exec -it capstone26-attacker bash ;;
  logs) need; docker compose -f "$C" logs --tail=100 ;;
  cleanup|down) need; docker compose -f "$C" down -v --remove-orphans ;;
  *) echo 'usage: capstone-lab.sh {build|create|status|shell|logs|cleanup}'; exit 2 ;;
esac
