#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, os, time

def main():
    ap=argparse.ArgumentParser(description='Compare fast SHA-256 hashing with PBKDF2 work factor locally.')
    ap.add_argument('--fast-count',type=int,default=100_000)
    ap.add_argument('--pbkdf2-count',type=int,default=8)
    ap.add_argument('--iterations',type=int,default=600_000)
    args=ap.parse_args()
    if args.fast_count>500_000 or args.pbkdf2_count>20 or args.iterations>1_000_000:
        raise SystemExit('training bounds exceeded')
    pw=b'Training123!'; salt=os.urandom(16)
    t=time.perf_counter()
    for i in range(args.fast_count): hashlib.sha256(pw+str(i).encode()).digest()
    fast=time.perf_counter()-t
    t=time.perf_counter()
    for _ in range(args.pbkdf2_count): hashlib.pbkdf2_hmac('sha256',pw,salt,args.iterations,32)
    slow=time.perf_counter()-t
    print(f'SHA-256: {args.fast_count} ops in {fast:.3f}s (~{args.fast_count/max(fast,1e-9):,.0f}/s)')
    print(f'PBKDF2: {args.pbkdf2_count} ops in {slow:.3f}s (~{args.pbkdf2_count/max(slow,1e-9):,.2f}/s)')
    print('Interpretation: password hashing should intentionally make guesses expensive.')
if __name__=='__main__': main()
