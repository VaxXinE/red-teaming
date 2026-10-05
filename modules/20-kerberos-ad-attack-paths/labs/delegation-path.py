#!/usr/bin/env python3
import argparse, json
p=argparse.ArgumentParser(description='Explain delegation relationships from synthetic/read-only JSON inventory.')
p.add_argument('json_file')
a=p.parse_args()
data=json.load(open(a.json_file, encoding='utf-8'))
for x in data.get('principals',[]):
    mode=x.get('mode','unknown')
    targets=', '.join(x.get('targets',[])) or '(none)'
    print(f"{x['name']}: {mode} -> {targets}")
    if mode == 'unconstrained': print('  review: broad impersonation boundary; prioritize hardening and host protection')
    elif mode == 'constrained': print('  review: verify permitted backend SPNs and who controls delegating account')
    elif mode.startswith('rbcd'): print('  review: resource object controls who may delegate to it; inspect ACL/control relationship')
