#!/usr/bin/env python3
from __future__ import annotations
import argparse, math

def main():
    ap=argparse.ArgumentParser(description='Calculate theoretical candidate keyspace; no cracking or network activity.')
    ap.add_argument('--charset-size',type=int,required=True)
    ap.add_argument('--length',type=int,required=True)
    args=ap.parse_args()
    if not (1 <= args.charset_size <= 256 and 1 <= args.length <= 64):
        raise SystemExit('training bounds: charset 1..256, length 1..64')
    k=args.charset_size**args.length
    print('candidates:',k)
    print('log2 bits:',round(math.log2(k),2))
    for rate in (1_000,1_000_000,1_000_000_000):
        sec=k/rate
        print(f'at {rate:,}/s worst-case seconds: {sec:.3e}')
if __name__=='__main__': main()
