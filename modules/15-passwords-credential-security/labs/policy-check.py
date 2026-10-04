#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path

def main() -> None:
    ap = argparse.ArgumentParser(description='Training password policy checker based on NIST SP 800-63B-4 concepts.')
    ap.add_argument('password')
    ap.add_argument('--mfa', action='store_true', help='Treat password as part of MFA; training minimum becomes 8 instead of 15.')
    ap.add_argument('--blocklist', default=str(Path(__file__).with_name('fixtures') / 'blocklist.txt'))
    args = ap.parse_args()
    min_len = 8 if args.mfa else 15
    blocked = {x.strip().casefold() for x in Path(args.blocklist).read_text(encoding='utf-8').splitlines() if x.strip()}
    reasons = []
    if len(args.password) < min_len:
        reasons.append(f'length {len(args.password)} < required training minimum {min_len}')
    if args.password.casefold() in blocked:
        reasons.append('password appears in local compromised/common blocklist fixture')
    print('mode:', 'password + MFA' if args.mfa else 'single-factor password')
    print('length:', len(args.password))
    print('composition rule enforced: no')
    print('routine rotation required: no')
    if reasons:
        print('result: REJECT')
        for r in reasons: print('-', r)
        raise SystemExit(2)
    print('result: ACCEPT (training policy checks only; not a strength guarantee)')

if __name__ == '__main__':
    main()
