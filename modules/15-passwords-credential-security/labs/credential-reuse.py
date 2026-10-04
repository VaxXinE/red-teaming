#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib
from collections import defaultdict
from pathlib import Path

def tag(secret: str) -> str:
    return hashlib.sha256(secret.encode()).hexdigest()[:12]

def main():
    ap=argparse.ArgumentParser(description='Analyze a local authorized CSV for exact credential reuse without printing plaintext passwords.')
    ap.add_argument('csv_file')
    args=ap.parse_args()
    groups=defaultdict(list)
    with Path(args.csv_file).open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            groups[tag(row['password'])].append((row['system'],row['username'],row.get('mfa','')))
    for fingerprint,items in sorted(groups.items()):
        if len(items)>1:
            print(f'reuse-group {fingerprint}: {len(items)} records')
            for system,user,mfa in items: print(f'  - {system}: {user} (mfa={mfa})')
if __name__=='__main__': main()
