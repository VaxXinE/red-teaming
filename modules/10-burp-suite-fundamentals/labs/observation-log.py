#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,datetime,hashlib
from pathlib import Path

def main()->int:
    ap=argparse.ArgumentParser(description='Append a Burp lab observation')
    ap.add_argument('csv',type=Path); ap.add_argument('--tool',required=True); ap.add_argument('--request',required=True)
    ap.add_argument('--observation',required=True); ap.add_argument('--evidence',type=Path)
    ns=ap.parse_args(); ns.csv.parent.mkdir(parents=True,exist_ok=True)
    digest=''
    if ns.evidence:
        b=ns.evidence.read_bytes(); digest=hashlib.sha256(b).hexdigest()
    fields=['timestamp_utc','tool','request','observation','evidence_sha256']
    new=not ns.csv.exists()
    with ns.csv.open('a',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields)
        if new: w.writeheader()
        w.writerow({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tool':ns.tool,'request':ns.request,'observation':ns.observation,'evidence_sha256':digest})
    print(f'appended observation to {ns.csv}')
    return 0
if __name__=='__main__': raise SystemExit(main())
