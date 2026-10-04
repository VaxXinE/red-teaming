#!/usr/bin/env python3
import argparse, json, csv
p=argparse.ArgumentParser(); p.add_argument('openapi'); p.add_argument('--output',required=True); a=p.parse_args()
data=json.load(open(a.openapi,encoding='utf-8'))
rows=[]
for path,item in data.get('paths',{}).items():
    if not isinstance(item,dict): continue
    for method,meta in item.items():
        if method.lower() in {'get','post','put','patch','delete','options','head'}:
            rows.append((method.upper(),path))
with open(a.output,'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['method','path']); w.writerows(sorted(rows,key=lambda x:(x[1],x[0])))
print(f'wrote {len(rows)} endpoints to {a.output}')
