#!/usr/bin/env python3
import argparse,csv,json,pathlib,sys
VALID={'pending','in-progress','done','blocked','not-tested'}

def read_rows(path):
    p=pathlib.Path(path)
    if not p.exists(): return []
    with p.open(newline='') as f: return list(csv.DictReader(f))

def write_rows(path,rows):
    p=pathlib.Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    fields=['id','objective','status','note']
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    p.chmod(0o600)

def init(args):
    data=json.loads(pathlib.Path(args.scenario).read_text())
    rows=[{'id':o['id'],'objective':o['objective'],'status':'pending','note':''} for o in data.get('objectives',[])]
    write_rows(args.output,rows); print(args.output)

def set_status(args):
    if args.status not in VALID: raise SystemExit('invalid status: '+args.status)
    rows=read_rows(args.file); found=False
    for r in rows:
        if r['id']==args.id:
            r['status']=args.status; r['note']=args.note or r.get('note',''); found=True
    if not found: raise SystemExit('objective not found: '+args.id)
    write_rows(args.file,rows); print(args.file)

def show(args):
    rows=read_rows(args.file)
    for r in rows: print(f"{r['id']:7} {r['status']:12} {r['objective']}" + (f" | {r['note']}" if r.get('note') else ''))

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    a=sp.add_parser('init'); a.add_argument('scenario'); a.add_argument('output'); a.set_defaults(func=init)
    a=sp.add_parser('set'); a.add_argument('file'); a.add_argument('id'); a.add_argument('status'); a.add_argument('--note',default=''); a.set_defaults(func=set_status)
    a=sp.add_parser('show'); a.add_argument('file'); a.set_defaults(func=show)
    args=ap.parse_args(); args.func(args)
if __name__=='__main__': main()
