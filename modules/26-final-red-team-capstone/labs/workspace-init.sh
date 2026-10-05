#!/usr/bin/env bash
set -euo pipefail
umask 077
root="${1:-capstone26}"
mkdir -p "$root"/{00-admin,01-notes,02-evidence/{recon,web,identity,privilege,pivot,objective,detection},03-inventory,04-hypotheses,05-findings,06-attack-path,07-cleanup,08-qa,09-report}
cat > "$root/README.md" <<'EOF'
# Module 26 Capstone Workspace

Keep raw evidence restricted. Do not store real credentials or unrelated personal data.
EOF
printf 'timestamp_utc,asset,zone,source,scope_status,reachability,services,notes\n' > "$root/03-inventory/assets.csv"
printf '# Hypothesis Log\n\n' > "$root/04-hypotheses/hypotheses.md"
printf '# Cleanup Record\n\n' > "$root/07-cleanup/cleanup.md"
chmod -R go-rwx "$root"
printf 'created %s\n' "$root"
