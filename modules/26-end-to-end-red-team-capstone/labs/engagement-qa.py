#!/usr/bin/env python3
import pathlib,re,sys,csv
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else 'module26-capstone')
checks=[]
def ck(ok,msg): checks.append((bool(ok),msg))
ck((root/'00-scope/README.md').exists(),'scope note exists')
ck((root/'03-notes/objectives.csv').exists(),'objective tracker exists')
ck((root/'03-notes/timeline.csv').exists(),'timeline exists')
ck((root/'06-evidence/sha256-manifest.txt').exists(),'evidence manifest exists')
findings=list((root/'04-findings').glob('*.md')) if (root/'04-findings').exists() else []
ck(bool(findings),'at least one finding/attack-path markdown exists')
if (root/'03-notes/objectives.csv').exists():
    with (root/'03-notes/objectives.csv').open(newline='') as f: rows=list(csv.DictReader(f))
    ck(bool(rows) and all(r.get('status') for r in rows),'objective rows have status')
placeholder=[]; secret=[]
secret_re=re.compile(r'(?i)(AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|authorization:\s*bearer\s+\S+|password\s*[:=]\s*\S+)')
for p in root.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in {'.md','.txt','.csv','.json','.log'}: continue
    try: text=p.read_text(errors='ignore')
    except Exception: continue
    if 'TODO' in text: placeholder.append(str(p))
    if secret_re.search(text): secret.append(str(p))
ck(not secret,'no obvious secret pattern in text artifacts')
print('ENGAGEMENT QA')
for ok,msg in checks: print(('PASS' if ok else 'FAIL')+': '+msg)
if placeholder: print(f'WARN: TODO placeholders remain in {len(placeholder)} file(s)')
if secret: print('Secret-pattern files:'); [print('- '+x) for x in secret]
raise SystemExit(0 if all(x[0] for x in checks) else 2)
