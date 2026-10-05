#!/usr/bin/env python3
import argparse,csv,datetime,pathlib,re
SECRET_RE=re.compile(r'(?i)(password|passwd|secret|token|private[_ -]?key|authorization:|bearer\s+)')

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    a=sp.add_parser('add'); a.add_argument('file'); a.add_argument('--phase',required=True); a.add_argument('--asset',required=True); a.add_argument('--action',required=True); a.add_argument('--outcome',required=True)
    args=ap.parse_args()
    fields=['timestamp_utc','phase','asset','action','outcome']
    values=[args.phase,args.asset,args.action,args.outcome]
    if any(SECRET_RE.search(v or '') for v in values):
        raise SystemExit('refusing likely secret-bearing timeline content; sanitize first')
    p=pathlib.Path(args.file); p.parent.mkdir(parents=True,exist_ok=True); new=not p.exists()
    with p.open('a',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields)
        if new: w.writeheader()
        w.writerow({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),'phase':args.phase,'asset':args.asset,'action':args.action,'outcome':args.outcome})
    p.chmod(0o600); print(p)
if __name__=='__main__': main()
