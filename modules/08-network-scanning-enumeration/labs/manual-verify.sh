#!/usr/bin/env bash
set -euo pipefail
printf '== HTTP nginx ==\n'
curl --fail --silent --show-error -I http://172.31.80.10/ | sed -n '1,8p'
printf '\n== HTTP Apache ==\n'
curl --fail --silent --show-error -I http://172.31.80.11/ | sed -n '1,8p'
printf '\n== Redis protocol ==\n'
printf '*1\r\n$4\r\nPING\r\n' | nc -w 2 172.31.80.12 6379
printf '\n== UDP echo ==\n'
printf 'hello' | nc -u -w 2 172.31.80.13 9999 || true
