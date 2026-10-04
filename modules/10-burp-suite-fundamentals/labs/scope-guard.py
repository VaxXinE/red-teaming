#!/usr/bin/env python3
from __future__ import annotations
import argparse, ipaddress
from urllib.parse import urlsplit
ALLOWED_PORTS={8090,3000,8080}
def main()->int:
    ap=argparse.ArgumentParser(description='Validate Module 10 training URLs')
    ap.add_argument('url'); ns=ap.parse_args(); u=urlsplit(ns.url)
    if u.scheme not in {'http','https'}: raise SystemExit('only http/https URLs are allowed')
    host=u.hostname
    if host is None: raise SystemExit('URL has no hostname')
    try: ip=ipaddress.ip_address(host)
    except ValueError: raise SystemExit('training guard accepts literal loopback IPs only')
    if not ip.is_loopback: raise SystemExit('refusing non-loopback target')
    port=u.port or (443 if u.scheme=='https' else 80)
    if port not in ALLOWED_PORTS: raise SystemExit(f'refusing port {port}; allowed: {sorted(ALLOWED_PORTS)}')
    print('PASS: loopback training URL')
    return 0
if __name__=='__main__': raise SystemExit(main())
