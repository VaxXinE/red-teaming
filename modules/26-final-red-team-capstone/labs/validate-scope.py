#!/usr/bin/env python3
import ipaddress, json, sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else 'scope.json')
data=json.loads(p.read_text())
errs=[]
for key in ('engagement','authorized_environment','targets','networks','allowed','prohibited','stop_conditions'):
    if not data.get(key): errs.append(f'missing/empty: {key}')
allowed_nets=[]
for n in data.get('networks',[]):
    try: allowed_nets.append(ipaddress.ip_network(n, strict=False))
    except ValueError: errs.append(f'invalid network: {n}')
for t in data.get('targets',[]):
    for field in ('name','ip','zone','role'):
        if not t.get(field): errs.append(f"target missing {field}: {t}")
    for key in ('ip','internal_ip'):
        if t.get(key):
            try:
                ip=ipaddress.ip_address(t[key])
                if allowed_nets and not any(ip in n for n in allowed_nets): errs.append(f'{t["name"]} {key} outside declared networks')
            except ValueError: errs.append(f'invalid IP: {t.get(key)}')
if data.get('authorized_environment') != 'local-docker-training-only': errs.append('authorized_environment must remain local-docker-training-only for packaged lab')
if errs:
    print('SCOPE VALIDATION FAIL')
    for e in errs: print(f'- {e}')
    raise SystemExit(1)
print('SCOPE VALIDATION PASS')
print(f"targets={len(data['targets'])} networks={len(data['networks'])}")
print('NOTE: structural validation is not legal authorization.')
