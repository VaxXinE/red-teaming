#!/usr/bin/env python3
"""Safety wrapper for Module 08 Nmap labs.
Allows only loopback and the dedicated Docker subnet 172.31.80.0/24.
Arguments after -- are passed to nmap unchanged.
"""
from __future__ import annotations
import argparse, ipaddress, os, shutil, subprocess, sys
ALLOWED=[ipaddress.ip_network('127.0.0.0/8'), ipaddress.ip_network('172.31.80.0/24')]

def allowed(target: str) -> bool:
    try:
        if '/' in target:
            net=ipaddress.ip_network(target,strict=False)
            return any(net.subnet_of(a) for a in ALLOWED)
        ip=ipaddress.ip_address(target)
        return any(ip in a for a in ALLOWED)
    except ValueError:
        return False

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('target')
    ap.add_argument('nmap_args',nargs=argparse.REMAINDER)
    ns=ap.parse_args()
    if not allowed(ns.target):
        print(f'refusing target outside training ranges: {ns.target}',file=sys.stderr); return 2
    nmap=shutil.which('nmap')
    if not nmap:
        print('nmap not found',file=sys.stderr); return 3
    args=ns.nmap_args
    if args and args[0]=='--': args=args[1:]
    cmd=[nmap,*args,ns.target]
    print('+',' '.join(cmd),file=sys.stderr)
    return subprocess.run(cmd,check=False).returncode
if __name__=='__main__': raise SystemExit(main())
