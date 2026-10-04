#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import json, time, threading, os

TOKENS={"token-alice":"alice","token-bob":"bob","token-admin":"admin"}
USERS={
 "alice":{"id":1,"username":"alice","email":"alice@example.test","role":"user","internal_note":"dummy-alice-note"},
 "bob":{"id":2,"username":"bob","email":"bob@example.test","role":"user","internal_note":"dummy-bob-note"},
 "admin":{"id":3,"username":"admin","email":"admin@example.test","role":"admin","internal_note":"dummy-admin-note"},
}
ORDERS={
 101:{"id":101,"owner":"alice","item":"training-book","amount":25},
 102:{"id":102,"owner":"bob","item":"lab-keyboard","amount":60},
 103:{"id":103,"owner":"admin","item":"dummy-admin-order","amount":99},
}
REDEMPTIONS=[]
LOCK=threading.Lock()
OPENAPI={
 "openapi":"3.0.3","info":{"title":"Module 13 Training API","version":"1.0"},
 "paths":{
  "/api/v1/login":{"post":{}},
  "/api/v1/me":{"get":{},"patch":{}},
  "/api/v1/orders/{id}":{"get":{}},
  "/api/v1/admin/stats":{"get":{}},
  "/api/v1/report":{"get":{}},
  "/api/v1/coupons/redeem":{"post":{}},
 }
}

def send_json(h,status,obj,headers=None):
    body=json.dumps(obj,indent=2).encode(); h.send_response(status); h.send_header('Content-Type','application/json'); h.send_header('Content-Length',str(len(body)))
    if headers:
        for k,v in headers.items(): h.send_header(k,v)
    h.end_headers(); h.wfile.write(body)

def auth_user(h):
    value=h.headers.get('Authorization','')
    if not value.startswith('Bearer '): return None
    return TOKENS.get(value[7:])

def read_json(h):
    try:
        n=int(h.headers.get('Content-Length','0')); raw=h.rfile.read(min(n,65536)); return json.loads(raw or b'{}')
    except Exception: return None

class H(BaseHTTPRequestHandler):
    server_version='Module13API/1.0'
    def log_message(self,fmt,*args): print('%s - %s' % (self.address_string(),fmt%args),flush=True)
    def do_GET(self):
        u=urlparse(self.path); path=u.path; q=parse_qs(u.query)
        if path=='/': return send_json(self,200,{"module":"13","lab":"API Security","docs":"/openapi.json","note":"intentionally vulnerable local training API"})
        if path=='/openapi.json': return send_json(self,200,OPENAPI)
        if path=='/health': return send_json(self,200,{"status":"ok"})
        user=auth_user(self)
        if path.startswith('/api/') and not user: return send_json(self,401,{"error":"missing or invalid bearer token"})
        if path=='/api/v1/me':
            # Property-level exposure: returns internal_note too.
            return send_json(self,200,USERS[user])
        if path.startswith('/api/v1/orders/'):
            try: oid=int(path.rsplit('/',1)[1]); order=ORDERS[oid]
            except Exception: return send_json(self,404,{"error":"order not found"})
            # BOLA: deliberately missing owner check.
            return send_json(self,200,order)
        if path=='/api/v1/admin/stats':
            # BFLA: deliberately missing admin role check.
            return send_json(self,200,{"users":len(USERS),"orders":len(ORDERS),"redemptions":len(REDEMPTIONS),"dummy_secret":"training-only"})
        if path=='/api/v1/report':
            raw=q.get('limit',['50'])[0]
            try: requested=int(raw)
            except ValueError: return send_json(self,400,{"error":"limit must be integer"})
            # Deliberately weak business limit; hard safety cap protects the lab.
            effective=max(0,min(requested,2000))
            rows=[{"row":i,"owner":user} for i in range(effective)]
            return send_json(self,200,{"requested":requested,"returned":effective,"rows":rows},headers={"X-Training-Safety-Cap":"2000"})
        if path=='/api/v0/debug/users':
            # Deprecated shadow endpoint for inventory-management exercise.
            return send_json(self,200,{"deprecated":True,"version":"v0","users":list(USERS.values())},headers={"Deprecation":"true"})
        return send_json(self,404,{"error":"not found"})
    def do_POST(self):
        u=urlparse(self.path); path=u.path; data=read_json(self)
        if data is None: return send_json(self,400,{"error":"invalid json"})
        if path=='/api/v1/login':
            username=str(data.get('username','')); password=str(data.get('password',''))
            if username in USERS and password=='training123':
                token={'alice':'token-alice','bob':'token-bob','admin':'token-admin'}[username]
                return send_json(self,200,{"access_token":token,"token_type":"Bearer","user":username})
            return send_json(self,401,{"error":"invalid credentials"})
        user=auth_user(self)
        if not user: return send_json(self,401,{"error":"missing or invalid bearer token"})
        if path=='/api/v1/coupons/redeem':
            code=str(data.get('code',''))
            # Business-flow flaw: no per-user/one-time enforcement.
            with LOCK: REDEMPTIONS.append({"user":user,"code":code,"ts":time.time()})
            return send_json(self,200,{"redeemed":True,"user":user,"code":code,"count_for_user":sum(1 for x in REDEMPTIONS if x['user']==user)})
        return send_json(self,404,{"error":"not found"})
    def do_PATCH(self):
        path=urlparse(self.path).path; data=read_json(self)
        if data is None: return send_json(self,400,{"error":"invalid json"})
        user=auth_user(self)
        if not user: return send_json(self,401,{"error":"missing or invalid bearer token"})
        if path=='/api/v1/me':
            # BOPLA/mass assignment: role should not be client-writable.
            allowed={'email','role'}
            for k,v in data.items():
                if k in allowed: USERS[user][k]=v
            return send_json(self,200,USERS[user])
        return send_json(self,404,{"error":"not found"})

ThreadingHTTPServer((os.getenv('BIND_HOST','127.0.0.1'),8130),H).serve_forever()
