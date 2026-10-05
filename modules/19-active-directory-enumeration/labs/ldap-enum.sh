#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -lt 4 ]]; then
  echo "Usage: $0 <users|groups|computers|spns> <dc-fqdn> <base-dn> <user-dn> [output-dir]" >&2
  exit 2
fi
MODE="$1"; DC="$2"; BASE="$3"; USER_DN="$4"; OUTDIR="${5:-module19-ad-enum/02-ldap}"
mkdir -p "$OUTDIR"
case "$MODE" in
  users)
    FILTER='(&(objectCategory=person)(objectClass=user))'
    ATTR=(sAMAccountName userPrincipalName memberOf userAccountControl)
    ;;
  groups)
    FILTER='(objectClass=group)'
    ATTR=(cn sAMAccountName member groupType)
    ;;
  computers)
    FILTER='(objectClass=computer)'
    ATTR=(cn dNSHostName operatingSystem operatingSystemVersion memberOf)
    ;;
  spns)
    FILTER='(&(objectClass=user)(servicePrincipalName=*))'
    ATTR=(sAMAccountName servicePrincipalName memberOf pwdLastSet)
    ;;
  *) echo "Unsupported mode: $MODE" >&2; exit 2;;
esac
OUT="$OUTDIR/${MODE}.ldif"
echo "Password will be requested interactively by ldapsearch (-W)." >&2
ldapsearch -x -H "ldap://${DC}" -D "$USER_DN" -W -b "$BASE" "$FILTER" "${ATTR[@]}" > "$OUT"
chmod 600 "$OUT"
echo "Wrote $OUT"
