#!/usr/bin/env python3
import argparse, json, sys, urllib.request, urllib.error, urllib.parse
from urllib.parse import urlparse

p=argparse.ArgumentParser(description='Loopback-only API client for Module 13')
p.add_argument('method'); p.add_argument('url'); p.add_argument('--token'); p.add_argument('--json',dest='json_body')
a=p.parse_args()
u=urlparse(a.url)
if u.hostname not in {'127.0.0.1','localhost','::1'}:
    raise SystemExit('training client only permits loopback targets')
headers={'Accept':'application/json'}
if a.token: headers['Authorization']='Bearer '+a.token
body=None
if a.json_body is not None:
    obj=json.loads(a.json_body); body=json.dumps(obj).encode(); headers['Content-Type']='application/json'
req=urllib.request.Request(a.url,data=body,headers=headers,method=a.method.upper())
try:
    with urllib.request.urlopen(req,timeout=5) as r:
        print('HTTP',r.status); print(r.read(1024*1024).decode(errors='replace'))
except urllib.error.HTTPError as e:
    print('HTTP',e.code); print(e.read(1024*1024).decode(errors='replace')); sys.exit(1)
