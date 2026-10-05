#!/usr/bin/env bash
set -euo pipefail
umask 077
name="${1:-module24-opsec}"
mkdir -p "$name"/{admin,notes,telemetry,detections,results,cleanup,evidence,tmp}
chmod 700 "$name"
cat > "$name/admin/scope.md" <<'EOF'
# Scope
- Authorized lab hosts only
- No production targets
- No control impairment / log tampering / persistence
EOF
cat > "$name/cleanup/cleanup-proof.md" <<'EOF'
# Cleanup Proof
- [ ] Training processes stopped
- [ ] Temporary files removed
- [ ] Local listeners stopped
- [ ] No config/security-control changes remain
- [ ] Evidence manifest generated
EOF
printf 'workspace=%s\n' "$name"
