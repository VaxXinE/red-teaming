#!/usr/bin/env python3
from __future__ import annotations
import argparse, re
from collections import Counter, defaultdict
from pathlib import Path
PAT=re.compile(r'auth (success|failure) user=(\S+) src=(\S+)')
def main():
    ap=argparse.ArgumentParser(description='Analyze synthetic/local auth logs for simple failure patterns.')
    ap.add_argument('logfile')
    args=ap.parse_args()
    src=Counter(); users=Counter(); uniq=defaultdict(set)
    for line in Path(args.logfile).read_text(encoding='utf-8').splitlines():
        m=PAT.search(line)
        if not m: continue
        status,user,ip=m.groups()
        if status=='failure':
            src[ip]+=1; users[user]+=1; uniq[ip].add(user)
    print('failure count by source:')
    for ip,n in src.most_common(): print(f'  {ip}: {n} failures across {len(uniq[ip])} users')
    print('failure count by user:')
    for user,n in users.most_common(): print(f'  {user}: {n}')
    print('training hints: one source failing across many users resembles spraying/stuffing telemetry; many failures on one user resembles brute-force telemetry.')
if __name__=='__main__': main()
