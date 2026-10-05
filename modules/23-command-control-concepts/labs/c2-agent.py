#!/usr/bin/env python3
import argparse, json, os, platform, socket, hashlib, time, urllib.request, urllib.error
from pathlib import Path

BASE='http://127.0.0.1:8230'

def req(path, obj=None):
    data=None; headers={}
    if obj is not None: data=json.dumps(obj).encode(); headers['Content-Type']='application/json'
    r=urllib.request.Request(BASE+path,data=data,headers=headers,method='POST' if obj is not None else 'GET')
    with urllib.request.urlopen(r,timeout=3) as resp: return resp, resp.read()

def post(path,obj):
    _,raw=req(path,obj); return json.loads(raw)

def get_json(path):
    _,raw=req(path); return json.loads(raw)

def proc_summary():
    if os.name=='posix' and Path('/proc').exists():
        pids=[p.name for p in Path('/proc').iterdir() if p.name.isdigit()]
        return {'process_count':len(pids),'sample_pids':pids[:20]}
    return {'process_count':'unavailable'}

def net_summary():
    return {'hostname':socket.gethostname(),'fqdn':socket.getfqdn(),'addresses':sorted({i[4][0] for i in socket.getaddrinfo(socket.gethostname(),None) if i[0] in (socket.AF_INET,socket.AF_INET6)})[:20]}

def execute(task, workspace):
    typ=task['type']; args=task.get('args') or {}
    if typ=='system_info': return {'user':os.environ.get('USER') or os.environ.get('USERNAME'),'hostname':socket.gethostname(),'platform':platform.platform(),'python':platform.python_version()}
    if typ=='process_summary': return proc_summary()
    if typ=='network_summary': return net_summary()
    if typ=='echo': return {'echo':str(args.get('text',''))[:256]}
    if typ=='get_training_artifact':
        resp,data=req('/artifact/training.txt'); expected=resp.headers.get('X-SHA256',''); actual=hashlib.sha256(data).hexdigest(); out=workspace/'artifacts'/'agent'/'training-artifact.txt'; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(data); os.chmod(out,0o600)
        return {'saved':str(out),'sha256':actual,'header_sha256':expected,'match':actual==expected,'bytes':len(data)}
    return {'error':'unsupported'}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--workspace',default='module23-c2'); ap.add_argument('--agent-id',default='lab-agent-01'); ap.add_argument('--interval',type=float,default=5.0); a=ap.parse_args()
    if not (1.0 <= a.interval <= 30.0): raise SystemExit('interval must be 1..30 seconds for lab')
    w=Path(a.workspace).resolve(); w.mkdir(parents=True,exist_ok=True)
    post('/register',{'agent_id':a.agent_id,'meta':{'hostname':socket.gethostname(),'platform':platform.platform()}}); print(f'[+] registered {a.agent_id}; polling every {a.interval}s (loopback only)')
    try:
        while True:
            try:
                task=get_json('/poll?id='+urllib.parse.quote(a.agent_id)).get('task')
                if task:
                    result=execute(task,w); post('/result',{'agent_id':a.agent_id,'task':task,'result':result}); print('[+] task',task['type'],'done')
            except Exception as e: print('[!] poll error:',e)
            time.sleep(a.interval)
    except KeyboardInterrupt: print('\n[+] agent stopped')
if __name__=='__main__':
    import urllib.parse
    main()
