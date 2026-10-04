#!/usr/bin/env python3
"""Append a normalized asset observation to assets.csv."""
import argparse, csv, datetime as dt, os, sys
from pathlib import Path

STATUSES={"candidate","in-scope","out-of-scope","needs-validation"}
CONF={"low","medium","high"}
TYPES={"domain","hostname","ip","url","email-domain","document","other"}

def main():
    os.umask(0o077)
    ap=argparse.ArgumentParser()
    ap.add_argument("csv_file", type=Path)
    ap.add_argument("--type", required=True, choices=sorted(TYPES))
    ap.add_argument("--value", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--scope", default="candidate", choices=sorted(STATUSES))
    ap.add_argument("--confidence", default="medium", choices=sorted(CONF))
    ap.add_argument("--notes", default="")
    args=ap.parse_args()
    if any(c in args.value for c in "\r\n") or any(c in args.source for c in "\r\n"):
        print("newlines are not allowed in value/source", file=sys.stderr); return 2
    args.csv_file.parent.mkdir(parents=True,exist_ok=True)
    exists=args.csv_file.exists()
    with args.csv_file.open('a',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        if not exists: w.writerow(["timestamp_utc","asset_type","value","source","scope_status","confidence","notes"])
        w.writerow([dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),args.type,args.value,args.source,args.scope,args.confidence,args.notes])
    try: args.csv_file.chmod(0o600)
    except OSError: pass
    print(f"logged {args.type}: {args.value}")
    return 0
if __name__=='__main__': raise SystemExit(main())
