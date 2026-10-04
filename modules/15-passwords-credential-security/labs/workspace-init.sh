#!/usr/bin/env bash
set -euo pipefail
umask 077
root="${1:-module15-credentials}"
mkdir -p "$root"/{00-scope,01-fixtures,02-hashes,03-cracking,04-audit,05-evidence,06-report}
printf '%s\n' "Module 15 workspace created at: $root"
printf '%s\n' "Training rule: use only bundled dummy credentials/hashes or data you are explicitly authorized to assess."
