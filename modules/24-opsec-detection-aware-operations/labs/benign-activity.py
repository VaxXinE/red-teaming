#!/usr/bin/env python3
import argparse, hashlib, json, os, pathlib, socket, subprocess, threading, time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body=b'Module 24 localhost telemetry lab\n'
        self.send_response(200); self.send_header('Content-Type','text/plain'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self,*a): pass

def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True, check=False)
def emit(logfile, event, **fields):
    row={"timestamp_utc":time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),"event":event,**fields}
    with logfile.open('a') as f: f.write(json.dumps(row,sort_keys=True)+'\n')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--workspace',default='module24-opsec'); ap.add_argument('--marker',default='RTLAB24_MARKER'); a=ap.parse_args()
    w=pathlib.Path(a.workspace).resolve(); w.mkdir(parents=True,exist_ok=True); tele=w/'telemetry'; tmp=w/'tmp'; tele.mkdir(exist_ok=True); tmp.mkdir(exist_ok=True)
    ev=tele/'benign-events.jsonl'; ev.touch(mode=0o600,exist_ok=True)
    # Read-only discovery
    for cmd in (["whoami"],["uname","-a"],["ps","-eo","pid,ppid,user,comm","--sort=pid"]):
        r=run(cmd); emit(ev,'process_observation',command=cmd[0],returncode=r.returncode,marker=a.marker)
    marker=tmp/'RTLAB24_MARKER.txt'; marker.write_text(a.marker+'\n'); marker.chmod(0o600)
    sha=hashlib.sha256(marker.read_bytes()).hexdigest(); emit(ev,'file_create',path=str(marker),sha256=sha,marker=a.marker)
    # Loopback-only local HTTP server
    srv=ThreadingHTTPServer(('127.0.0.1',0),Handler); port=srv.server_address[1]
    th=threading.Thread(target=srv.serve_forever,daemon=True); th.start()
    try:
        with urlopen(f'http://127.0.0.1:{port}/',timeout=2) as r: r.read()
        emit(ev,'network_connect',destination='127.0.0.1',port=port,protocol='http',marker=a.marker)
    finally:
        srv.shutdown(); srv.server_close()
    marker.unlink(); emit(ev,'file_delete',path=str(marker),marker=a.marker)
    print(ev)
if __name__=='__main__': main()
