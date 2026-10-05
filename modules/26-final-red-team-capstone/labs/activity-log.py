#!/usr/bin/env python3
import argparse, datetime, json, os
from pathlib import Path
ap=argparse.ArgumentParser()
ap.add_argument('log')
ap.add_argument('--operator',required=True); ap.add_argument('--asset',required=True); ap.add_argument('--action',required=True)
ap.add_argument('--purpose',required=True); ap.add_argument('--result',required=True); ap.add_argument('--evidence',default='')
a=ap.parse_args(); path=Path(a.log); path.parent.mkdir(parents=True,exist_ok=True)
row={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator':a.operator,'asset':a.asset,'action':a.action,'purpose':a.purpose,'result':a.result,'evidence':a.evidence}
fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o600)
with os.fdopen(fd,'a') as f: f.write(json.dumps(row,separators=(',',':'))+'\n')
print(json.dumps(row,indent=2))
