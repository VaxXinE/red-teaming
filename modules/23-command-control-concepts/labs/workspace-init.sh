#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="${1:-module23-c2}"
mkdir -p "$ROOT"/{logs,captures,artifacts/agent,notes,evidence,results,tmp}
printf '# Module 23 C2 Lab\n\nScope: localhost only.\n' > "$ROOT/notes/scope.md"
printf '# Detection Hypothesis\n\nData sources:\nBehavior:\nSequence:\nFalse positives:\nExpected result:\n' > "$ROOT/notes/detection-hypothesis.md"
printf '# Cleanup\n\n- controller stopped: [ ]\n- agent stopped: [ ]\n- port 8230 closed: [ ]\n- temp artifacts reviewed: [ ]\n' > "$ROOT/notes/cleanup.md"
chmod -R go-rwx "$ROOT"
echo "[+] Workspace: $ROOT"
