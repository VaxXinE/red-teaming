#!/usr/bin/env python3
# Intentionally vulnerable training service. Run only inside the packaged isolated lab.
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
ROOT='/app/files'
class H(BaseHTTPRequestHandler):
    def log_message(self, fmt,*args): print('edge-web', self.address_string(), fmt%args, flush=True)
    def send(self,code,body,ctype='text/plain; charset=utf-8'):
        b=body.encode(); self.send_response(code); self.send_header('Content-Type',ctype); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u=urlparse(self.path)
        if u.path=='/':
            return self.send(200,'Module 26 Edge Service\nGET /download?file=welcome.txt\n')
        if u.path=='/download':
            name=parse_qs(u.query).get('file',[''])[0]
            if not name: return self.send(400,'file required\n')
            # TRAINING FLAW: user-controlled path is joined without enforcing containment.
            path=os.path.join(ROOT,name)
            try:
                with open(path,'r',encoding='utf-8',errors='replace') as f: data=f.read(8192)
                return self.send(200,data)
            except Exception as e: return self.send(404,f'not found: {type(e).__name__}\n')
        return self.send(404,'not found\n')
bind=os.environ.get('LAB_BIND','127.0.0.1'); port=8080
print(f'edge-web listening on {bind}:{port}',flush=True)
ThreadingHTTPServer((bind,port),H).serve_forever()
