#!/usr/bin/env python3
import argparse, json, ipaddress
from pathlib import Path

p=argparse.ArgumentParser(description='Summarize Module 21 training topology.')
p.add_argument('file', nargs='?', default=str(Path(__file__).with_name('topology.json')))
args=p.parse_args()
data=json.loads(Path(args.file).read_text())
for key in ('external_network','internal_network'):
    ipaddress.ip_network(data[key], strict=True)
print(f"External: {data['external_network']}")
print(f"Internal: {data['internal_network']}")
for n in data['nodes']:
    print(f"- {n['name']:<13} {', '.join(n['interfaces']):<32} {n['role']}")
print('\nExpected path: attacker -> jump -> internal service')
