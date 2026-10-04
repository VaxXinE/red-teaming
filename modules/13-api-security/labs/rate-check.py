#!/usr/bin/env python3
import argparse,time,urllib.request
from urllib.parse import urlparse
p=argparse.ArgumentParser(); p.add_argument('url'); p.add_argument('--token',required=True); p.add_argument('--count',type=int,default=8); a=p.parse_args()
u=urlparse(a.url)
if u.hostname not in {'127.0.0.1','localhost','::1'}: raise SystemExit('loopback only')
count=max(1,min(a.count,12))
for i in range(count):
    req=urllib.request.Request(a.url,headers={'Authorization':'Bearer '+a.token,'Accept':'application/json'})
    t=time.perf_counter()
    with urllib.request.urlopen(req,timeout=5) as r:
        r.read(128); ms=(time.perf_counter()-t)*1000; print(f'{i+1:02d} status={r.status} ms={ms:.1f} retry_after={r.headers.get("Retry-After")}')
