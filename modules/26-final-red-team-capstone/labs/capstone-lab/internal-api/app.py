#!/usr/bin/env python3
import json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
TOKEN='TRAINING_INTERNAL_26'
class H(BaseHTTPRequestHandler):
    def log_message(self,fmt,*args): print('internal-api',self.address_string(),fmt%args,flush=True)
    def reply(self,code,obj):
        b=(json.dumps(obj)+'\n').encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path=='/health': return self.reply(200,{'status':'ok','service':'internal-api'})
        if self.path=='/api/ops/credential':
            if self.headers.get('X-Training-Token') != TOKEN: return self.reply(403,{'error':'forbidden'})
            return self.reply(200,{'username':'operator','password':'Internal26!','target':'10.26.20.50','purpose':'training-only'})
        return self.reply(404,{'error':'not found'})
bind=os.environ.get('LAB_BIND','127.0.0.1'); ThreadingHTTPServer((bind,8081),H).serve_forever()
