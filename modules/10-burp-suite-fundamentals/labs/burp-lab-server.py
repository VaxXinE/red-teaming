#!/usr/bin/env python3
from __future__ import annotations
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlsplit, parse_qs
import argparse, json

class Handler(BaseHTTPRequestHandler):
    server_version='Module10Lab/1.0'
    def _json(self, status:int, obj:dict, headers:dict|None=None):
        data=json.dumps(obj,indent=2,sort_keys=True).encode()
        self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store')
        for k,v in (headers or {}).items(): self.send_header(k,v)
        self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        u=urlsplit(self.path); q=parse_qs(u.query,keep_blank_values=True)
        if u.path=='/':
            body=b'<!doctype html><html><body><h1>Module 10 Burp Lab</h1><ul><li><a href="/echo?name=alice&role=user">Echo</a></li><li><a href="/cookie">Set cookie</a></li><li><a href="/redirect">Redirect</a></li></ul></body></html>'
            self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(body); return
        if u.path=='/echo': self._json(200,{'path':u.path,'query':q,'user_agent':self.headers.get('User-Agent',''),'cookie':self.headers.get('Cookie','')}); return
        if u.path=='/cookie': self._json(200,{'message':'training cookie set'}, {'Set-Cookie':'module10_session=training-only; Path=/; HttpOnly; SameSite=Lax'}); return
        if u.path=='/redirect': self.send_response(302); self.send_header('Location','/final'); self.send_header('Content-Length','0'); self.end_headers(); return
        if u.path=='/final': self._json(200,{'status':'redirect-complete'}); return
        self._json(404,{'error':'not found','path':u.path})
    def do_POST(self):
        n=min(int(self.headers.get('Content-Length','0') or 0), 65536); raw=self.rfile.read(n); ct=self.headers.get('Content-Type','')
        if self.path=='/login':
            try:
                if 'application/json' in ct: data=json.loads(raw or b'{}')
                else: data={'raw':raw.decode('utf-8','replace')}
            except json.JSONDecodeError: self._json(400,{'error':'invalid json'}); return
            user=str(data.get('username',''))[:80]
            self._json(200,{'authenticated':False,'message':'training endpoint; no real authentication','username':user},{'Set-Cookie':'module10_auth=demo; Path=/; HttpOnly; SameSite=Lax'}); return
        if self.path=='/reflect': self._json(200,{'content_type':ct,'length':len(raw),'body':raw.decode('utf-8','replace')[:500]}); return
        self._json(404,{'error':'not found'})
    def log_message(self,fmt,*args): print('[module10]',fmt%args)

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--host',default='127.0.0.1'); ap.add_argument('--port',type=int,default=8090); ns=ap.parse_args()
    if ns.host not in {'127.0.0.1','::1','localhost'}: raise SystemExit('refusing non-loopback bind')
    if not (1024 <= ns.port <= 65535): raise SystemExit('choose an unprivileged port')
    httpd=ThreadingHTTPServer(('127.0.0.1',ns.port),Handler)
    print(f'Listening on http://127.0.0.1:{ns.port}')
    try: httpd.serve_forever()
    except KeyboardInterrupt: pass
    finally: httpd.server_close()
    return 0
if __name__=='__main__': raise SystemExit(main())
