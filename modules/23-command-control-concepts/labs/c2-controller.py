#!/usr/bin/env python3
import argparse, json, hashlib, time, threading, urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

AGENTS={}; QUEUES={}; RESULTS=[]; LOCK=threading.Lock(); ROOT=None
ALLOWED={'system_info','process_summary','network_summary','echo','get_training_artifact'}

def now(): return time.time()
def log(event, **kw):
    rec={'ts': now(),'event':event,**kw}
    p=ROOT/'logs'/'controller.jsonl'; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a',encoding='utf-8') as f: f.write(json.dumps(rec,sort_keys=True)+'\n')

def send_json(h,obj,status=200):
    data=json.dumps(obj).encode(); h.send_response(status); h.send_header('Content-Type','application/json'); h.send_header('Content-Length',str(len(data))); h.end_headers(); h.wfile.write(data)

class H(BaseHTTPRequestHandler):
    server_version='Module23Lab/1.0'
    def log_message(self,*a): return
    def do_POST(self):
        n=int(self.headers.get('Content-Length','0')); raw=self.rfile.read(n)
        try: obj=json.loads(raw or b'{}')
        except: return send_json(self,{'error':'bad json'},400)
        if self.path=='/register':
            aid=str(obj.get('agent_id',''))
            if not aid or len(aid)>64: return send_json(self,{'error':'bad agent id'},400)
            with LOCK: AGENTS[aid]={'last_seen':now(),'meta':obj.get('meta',{})}; QUEUES.setdefault(aid,[])
            log('register',agent_id=aid,bytes=n); return send_json(self,{'ok':True})
        if self.path=='/result':
            aid=str(obj.get('agent_id','')); task=obj.get('task',{}); result=obj.get('result',{})
            with LOCK: RESULTS.append({'ts':now(),'agent_id':aid,'task':task,'result':result}); AGENTS.setdefault(aid,{})['last_seen']=now()
            (ROOT/'results'/f"{aid}.jsonl").parent.mkdir(parents=True,exist_ok=True)
            with (ROOT/'results'/f"{aid}.jsonl").open('a',encoding='utf-8') as f: f.write(json.dumps({'ts':now(),'task':task,'result':result})+'\n')
            log('result',agent_id=aid,task_type=task.get('type'),bytes=n); return send_json(self,{'ok':True})
        if self.path=='/queue':
            aid=str(obj.get('agent_id','')); typ=str(obj.get('type','')); args=obj.get('args',{})
            if typ not in ALLOWED: return send_json(self,{'error':'task not allowed','allowed':sorted(ALLOWED)},400)
            if not aid: return send_json(self,{'error':'agent required'},400)
            task={'id':hashlib.sha256(f'{now()}:{aid}:{typ}'.encode()).hexdigest()[:12],'type':typ,'args':args,'queued_at':now()}
            with LOCK: QUEUES.setdefault(aid,[]).append(task)
            log('task_queued',agent_id=aid,task_type=typ,task_id=task['id']); return send_json(self,{'ok':True,'task':task})
        return send_json(self,{'error':'not found'},404)
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); q=urllib.parse.parse_qs(u.query)
        if u.path=='/poll':
            aid=q.get('id',[''])[0]
            with LOCK:
                if aid in AGENTS: AGENTS[aid]['last_seen']=now()
                task=QUEUES.setdefault(aid,[]).pop(0) if QUEUES.setdefault(aid,[]) else None
            log('poll',agent_id=aid,task_type=(task or {}).get('type'),task_id=(task or {}).get('id'))
            return send_json(self,{'task':task})
        if u.path=='/state':
            with LOCK: state={'agents':AGENTS,'queued':{k:len(v) for k,v in QUEUES.items()},'results':RESULTS[-20:]}
            return send_json(self,state)
        if u.path=='/artifact/training.txt':
            data=(Path(__file__).parent/'training-artifact.txt').read_bytes(); sha=hashlib.sha256(data).hexdigest()
            self.send_response(200); self.send_header('Content-Type','text/plain'); self.send_header('X-SHA256',sha); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data); log('artifact_download',bytes=len(data)); return
        return send_json(self,{'error':'not found'},404)

def main():
    global ROOT
    ap=argparse.ArgumentParser(); ap.add_argument('--workspace',default='module23-c2'); args=ap.parse_args(); ROOT=Path(args.workspace).resolve(); (ROOT/'logs').mkdir(parents=True,exist_ok=True); (ROOT/'results').mkdir(parents=True,exist_ok=True)
    srv=ThreadingHTTPServer(('127.0.0.1',8230),H); print('[+] controller listening on http://127.0.0.1:8230'); log('controller_start',bind='127.0.0.1',port=8230)
    try: srv.serve_forever()
    except KeyboardInterrupt: pass
    finally: log('controller_stop'); srv.server_close()
if __name__=='__main__': main()
