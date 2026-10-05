#!/usr/bin/env python3
import argparse, csv, hashlib
from pathlib import Path

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--output', required=True)
    a=ap.parse_args(); root=Path(a.root); out=Path(a.output)
    rows=[]
    for p in sorted(root.rglob('*')):
        if p.is_file(): rows.append([str(p.relative_to(root)), p.stat().st_size, sha256(p)])
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['path','bytes','sha256']); w.writerows(rows)
    print(f'{len(rows)} files -> {out}')
if __name__=='__main__': main()
