from flask import Flask, request, jsonify, make_response, render_template_string
from lxml import etree
import base64, json, threading, time, requests as http_requests
from urllib.parse import urlparse

app=Flask(__name__)
internal=Flask('internal')
state={'transfers':0,'coupon_used':False,'race_success':0,'cache':{}}

@internal.get('/internal/admin')
def internal_admin():
    return jsonify({'service':'internal-only','flag':'module12-internal-demo','note':'not published to host'})

def b64decode_part(part):
    part += '=' * ((4-len(part)%4)%4)
    return json.loads(base64.urlsafe_b64decode(part.encode()))

@app.get('/')
def index():
    return '''<h1>Module 12 Advanced Web Trust Lab</h1><ul>
<li>/ssrf?url=http://127.0.0.1:8121/internal/admin</li>
<li>/ssti?name=student</li><li>POST /xml</li><li>/login</li><li>/cors-data</li>
<li>POST /transfer</li><li>/jwt-login</li><li>/jwt-admin</li><li>POST /nosql-login</li>
<li>/reset-link</li><li>/cache-home</li><li>POST /race/reset</li><li>POST /race/redeem</li>
<li>/logic/checkout?price=100&quantity=1</li></ul>'''

@app.get('/ssrf')
def ssrf():
    url=request.args.get('url','')
    u=urlparse(url)
    if u.scheme not in ('http','https') or u.hostname not in ('127.0.0.1','localhost'):
        return jsonify({'error':'training guardrail: only loopback destinations are permitted'}),400
    try:
        r=http_requests.get(url, timeout=2)
        return jsonify({'status':r.status_code,'body':r.text[:1000]})
    except Exception as e:
        return jsonify({'error':str(e)}),502

@app.get('/ssti')
def ssti():
    name=request.args.get('name','student')
    return render_template_string('Hello '+name)

@app.post('/xml')
def xml():
    parser=etree.XMLParser(load_dtd=True, resolve_entities=True, no_network=False)
    try:
        root=etree.fromstring(request.data, parser)
        return jsonify({'value':''.join(root.itertext())[:1000]})
    except Exception as e:
        return jsonify({'error':str(e)}),400

@app.get('/login')
def login():
    resp=make_response('local demo session set for student')
    resp.set_cookie('session','student',httponly=True,samesite='Lax')
    return resp

@app.get('/cors-data')
def cors_data():
    resp=jsonify({'account':'student','demo_secret':'cors-local-demo'})
    origin=request.headers.get('Origin')
    if origin:
        resp.headers['Access-Control-Allow-Origin']=origin
        resp.headers['Access-Control-Allow-Credentials']='true'
        resp.headers['Vary']='Origin'
    return resp

@app.post('/transfer')
def transfer():
    if request.cookies.get('session')!='student':
        return 'login first via /login',401
    amount=int(request.form.get('amount','0'))
    state['transfers'] += amount
    return jsonify({'ok':True,'total_transferred':state['transfers']})

@app.get('/jwt-login')
def jwt_login():
    header=base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').rstrip(b'=').decode()
    payload=base64.urlsafe_b64encode(b'{"sub":"student","role":"user"}').rstrip(b'=').decode()
    return jsonify({'token':header+'.'+payload+'.'})

@app.get('/jwt-admin')
def jwt_admin():
    auth=request.headers.get('Authorization','')
    if not auth.startswith('Bearer '): return 'Bearer token required',401
    token=auth[7:]
    try:
        h,p,_=token.split('.',2)
        header=b64decode_part(h); payload=b64decode_part(p)
        # Deliberately broken training verifier: alg=none is accepted without a signature.
        if header.get('alg')=='none' and payload.get('role')=='admin':
            return jsonify({'admin':True,'flag':'jwt-local-demo'})
        return jsonify({'admin':False,'claims':payload}),403
    except Exception as e:
        return jsonify({'error':str(e)}),400

@app.post('/nosql-login')
def nosql_login():
    data=request.get_json(force=True,silent=True) or {}
    username=data.get('username'); password=data.get('password')
    # Deliberately unsafe operator-like handling for local training.
    user_ok = username=='student' or (isinstance(username,dict) and '$ne' in username)
    pass_ok = password=='student' or (isinstance(password,dict) and '$ne' in password)
    return jsonify({'authenticated': bool(user_ok and pass_ok)})

@app.get('/reset-link')
def reset_link():
    host=request.headers.get('Host','127.0.0.1:8120')
    return jsonify({'reset_link':f'http://{host}/reset?token=LOCAL-DEMO'})

@app.get('/cache-home')
def cache_home():
    key=request.path  # Deliberately ignores unkeyed header and query string.
    if key in state['cache']:
        body=state['cache'][key]; resp=make_response(body); resp.headers['X-Cache']='hit'; return resp
    host=request.headers.get('X-Forwarded-Host','static.local')
    body=f'<html><script src="https://{host}/tracking.js"></script><h1>cached home</h1></html>'
    state['cache'][key]=body
    resp=make_response(body); resp.headers['X-Cache']='miss'; return resp

@app.post('/cache-reset')
def cache_reset():
    state['cache'].clear(); return jsonify({'reset':True})

@app.post('/race/reset')
def race_reset():
    state['coupon_used']=False; state['race_success']=0; return jsonify({'reset':True})

@app.post('/race/redeem')
def race_redeem():
    if state['coupon_used']:
        return 'already used',409
    time.sleep(0.15)
    state['coupon_used']=True
    state['race_success'] += 1
    return f'redeemed success_count={state["race_success"]}'

@app.get('/logic/checkout')
def logic_checkout():
    price=float(request.args.get('price','100')); quantity=int(request.args.get('quantity','1'))
    total=price*quantity
    return jsonify({'price':price,'quantity':quantity,'total':total,'accepted':True})

def run_internal():
    internal.run(host='127.0.0.1',port=8121,debug=False,use_reloader=False)

if __name__=='__main__':
    threading.Thread(target=run_internal,daemon=True).start()
    time.sleep(0.2)
    app.run(host='0.0.0.0',port=8120,debug=False,threaded=True,use_reloader=False)
