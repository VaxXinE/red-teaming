from __future__ import annotations
from flask import Flask, request, make_response, redirect, send_from_directory
from pathlib import Path
import html, os, sqlite3, subprocess

app = Flask(__name__)
DB = '/tmp/module11.db'
UPLOADS = Path('/tmp/uploads')
FILES = Path('/app/files')
UPLOADS.mkdir(parents=True, exist_ok=True)

def db_init():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS products')
    cur.execute('DROP TABLE IF EXISTS users')
    cur.executemany('INSERT INTO sqlite_master(name,type) VALUES (?,?)', []) if False else None
    cur.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, hidden INTEGER)')
    cur.executemany('INSERT INTO products(name,category,hidden) VALUES (?,?,?)', [
        ('Red Mug','Gifts',0),('Blue Shirt','Apparel',0),('Internal Prototype','Gifts',1)])
    cur.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, role TEXT, bio TEXT)')
    cur.executemany('INSERT INTO users(id,username,role,bio) VALUES (?,?,?,?)', [
        (1,'student','user','Training account'),(2,'admin','admin','Privileged training account')])
    con.commit(); con.close()

@app.before_request
def ensure_db():
    if not Path(DB).exists(): db_init()

@app.get('/')
def home():
    return '''<!doctype html><html><body><h1>Module 11 Vulnerable Web Lab</h1>
    <p>Deliberately vulnerable. Local training only.</p><ul>
    <li><a href="/products?category=Gifts">SQL injection</a></li>
    <li><a href="/search?q=hello">Reflected XSS</a></li>
    <li><a href="/system?host=127.0.0.1">Command injection</a></li>
    <li><a href="/download?file=welcome.txt">Path traversal</a></li>
    <li><a href="/upload">File upload</a></li>
    <li><a href="/login">Authentication/session flaw</a></li>
    <li><a href="/api/profile?id=1">IDOR</a></li>
    </ul></body></html>'''

@app.get('/products')
def products():
    category = request.args.get('category','Gifts')
    query = f"SELECT id,name,category FROM products WHERE category = '{category}' AND hidden = 0"
    try:
        con = sqlite3.connect(DB); rows = con.execute(query).fetchall(); con.close()
        body = '<h2>Products</h2><pre>' + html.escape(repr(rows)) + '</pre><p>Query (lab visibility): <code>' + html.escape(query) + '</code></p>'
        return body
    except Exception as e:
        return '<pre>Database error: ' + html.escape(str(e)) + '</pre>', 500

@app.get('/search')
def search():
    q = request.args.get('q','')
    # Intentionally unsafe: raw reflection into HTML body.
    return f'<!doctype html><html><body><h2>Search</h2><p>Results for: {q}</p></body></html>'

@app.get('/system')
def system():
    host = request.args.get('host','127.0.0.1')
    # Intentionally unsafe shell=True training example. Container is hardened by launcher.
    cmd = 'printf "checking %s\\n" ' + host
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=2, text=True)
    except Exception as e:
        out = f'error: {e}'
    return '<pre>' + html.escape(out) + '</pre>'

@app.get('/download')
def download():
    name = request.args.get('file','welcome.txt')
    # Intentionally vulnerable to ../ traversal.
    path = Path('/app/files/' + name)
    try:
        data = path.read_text(errors='replace')[:12000]
        return '<pre>' + html.escape(data) + '</pre>'
    except Exception as e:
        return '<pre>' + html.escape(str(e)) + '</pre>', 404

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return '''<h2>Upload</h2><form method="post" enctype="multipart/form-data">
        <input type="file" name="file"><button>Upload</button></form>'''
    f = request.files.get('file')
    if not f or not f.filename: return 'missing file', 400
    # Intentionally weak: trusts filename/extension and stores in same-origin served directory.
    name = Path(f.filename).name
    f.save(UPLOADS / name)
    return f'Uploaded. <a href="/uploads/{html.escape(name)}">Open file</a>'

@app.get('/uploads/<path:name>')
def uploads(name):
    return send_from_directory(UPLOADS, name)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return '''<h2>Login</h2><p>Training credentials: student / student</p>
        <form method="post"><input name="username"><input name="password" type="password"><button>Login</button></form>'''
    username = request.form.get('username','')
    password = request.form.get('password','')
    if username == 'student' and password == 'student':
        r = make_response(redirect('/profile'))
        # Intentionally insecure: unsigned identity cookie trusted by server.
        r.set_cookie('user', 'student', httponly=True, samesite='Lax')
        return r
    return 'Invalid credentials', 401

@app.get('/profile')
def profile():
    user = request.cookies.get('user','guest')
    if user == 'admin':
        return '<h2>Admin profile</h2><p>Authentication/session integrity bypass demonstrated.</p>'
    if user == 'student':
        return '<h2>Student profile</h2><p>Edit the unsigned cookie in Burp Repeater.</p>'
    return redirect('/login')

@app.get('/api/profile')
def api_profile():
    user_id = request.args.get('id','1')
    con = sqlite3.connect(DB)
    row = con.execute('SELECT id,username,role,bio FROM users WHERE id=?',(user_id,)).fetchone(); con.close()
    if not row: return {'error':'not found'},404
    # Intentionally missing object-level authorization check.
    return {'id':row[0],'username':row[1],'role':row[2],'bio':row[3]}

if __name__ == '__main__':
    db_init()
    app.run(host='0.0.0.0', port=8111, debug=False)
