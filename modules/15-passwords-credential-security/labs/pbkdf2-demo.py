#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, hashlib, hmac, os

def derive(password: str, salt: bytes, iterations: int = 600_000) -> bytes:
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations, dklen=32)

def encode(iterations: int, salt: bytes, digest: bytes) -> str:
    return f"pbkdf2_sha256${iterations}${base64.urlsafe_b64encode(salt).decode().rstrip('=')}${base64.urlsafe_b64encode(digest).decode().rstrip('=')}"

def main() -> None:
    ap = argparse.ArgumentParser(description='Local PBKDF2 salt/work-factor demonstration.')
    ap.add_argument('--password', default='Training-Only-Password-15')
    ap.add_argument('--iterations', type=int, default=600_000)
    args = ap.parse_args()
    if not (100_000 <= args.iterations <= 2_000_000):
        raise SystemExit('iterations must be between 100000 and 2000000 for this training utility')
    salt1, salt2 = os.urandom(16), os.urandom(16)
    h1 = derive(args.password, salt1, args.iterations)
    h2 = derive(args.password, salt2, args.iterations)
    print('same password, independent salts:')
    print('hash-1:', encode(args.iterations, salt1, h1))
    print('hash-2:', encode(args.iterations, salt2, h2))
    print('digests equal:', hmac.compare_digest(h1, h2))
    print('verification-1:', hmac.compare_digest(derive(args.password, salt1, args.iterations), h1))
