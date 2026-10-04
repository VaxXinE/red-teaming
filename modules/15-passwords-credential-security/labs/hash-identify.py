#!/usr/bin/env python3
from __future__ import annotations
import argparse, re

def classify(value: str) -> str:
    v=value.strip()
    if v.startswith('$argon2id$'): return 'Argon2id password hash'
    if v.startswith(('$2a$','$2b$','$2y$')): return 'bcrypt password hash'
    if v.startswith('$6$'): return 'SHA-512 crypt (sha512crypt)'
    if v.startswith('$5$'): return 'SHA-256 crypt (sha256crypt)'
    if re.fullmatch(r'[0-9a-fA-F]{64}', v): return '64 hex chars: could be raw SHA-256 or another 256-bit value; context required'
    if re.fullmatch(r'[A-Za-z0-9+/]+={0,2}', v) and len(v) % 4 == 0: return 'Base64-looking encoding; encoding is not password hashing'
    return 'unknown / context required'

def main():
    ap=argparse.ArgumentParser(description='Format classifier for local training strings. Does not crack anything.')
    ap.add_argument('value')
    args=ap.parse_args()
    print(classify(args.value))
if __name__=='__main__': main()
