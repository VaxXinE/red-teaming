#!/usr/bin/env python3
"""Extract and normalize DNS names from crt.sh JSON already downloaded by the student."""
import argparse, json, re, sys
from pathlib import Path

DOMAIN_RE = re.compile(r"^(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,63}$")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("json_file", type=Path)
    ap.add_argument("--domain", required=True)
    args=ap.parse_args()
    domain=args.domain.rstrip('.').lower()
    if not DOMAIN_RE.fullmatch(domain):
        print("invalid domain", file=sys.stderr); return 2
    data=json.loads(args.json_file.read_text(encoding='utf-8'))
    names=set()
    for row in data if isinstance(data,list) else []:
        for raw in str(row.get('name_value','')).splitlines():
            n=raw.strip().lower().rstrip('.')
            if n.startswith('*.'): n=n[2:]
            if n==domain or n.endswith('.'+domain): names.add(n)
    for n in sorted(names): print(n)
    return 0
if __name__=='__main__': raise SystemExit(main())
