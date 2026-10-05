#!/usr/bin/env python3
import argparse, json, urllib.request
BASE='http://127.0.0.1:8230'; ALLOWED={'system_info','process_summary','network_summary','echo','get_training_artifact'}
def request(path,obj=None):
    data=json.dumps(obj).encode() if obj is not None else None; headers={'Content-Type':'application/json'} if obj is not None else {}
    req=urllib.request.Request(BASE+path,data=data,headers=headers,method='POST' if obj is not None else 'GET')
    with urllib.request.urlopen(req,timeout=3) as r: return json.loads(r.read())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('action',choices=sorted(ALLOWED|{'state'})); ap.add_argument('--agent',default='lab-agent-01'); ap.add_argument('--text',default='hello from operator'); a=ap.parse_args()
    if a.action=='state': out=request('/state')
    else: out=request('/queue',{'agent_id':a.agent,'type':a.action,'args':{'text':a.text}})
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
