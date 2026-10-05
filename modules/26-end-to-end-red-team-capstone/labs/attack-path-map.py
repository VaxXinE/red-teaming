#!/usr/bin/env python3
import json,pathlib,sys
if len(sys.argv)!=3: raise SystemExit(f'usage: {sys.argv[0]} <attack-path.json> <output.md>')
data=json.loads(pathlib.Path(sys.argv[1]).read_text())
allowed={'validated','blocked','detected','logged-only','hypothetical','not-tested'}
lines=['# Attack Path Map','', '```mermaid','flowchart LR']
for n in data.get('nodes',[]):
    nid=n['id'].replace('-','_'); label=n.get('label',n['id']).replace('"','\\"')
    lines.append(f'  {nid}["{label}"]')
for e in data.get('edges',[]):
    st=e.get('state','hypothetical')
    if st not in allowed: raise SystemExit('invalid state: '+st)
    s=e['from'].replace('-','_'); d=e['to'].replace('-','_'); note=e.get('note','').replace('"','\\"')
    lines.append(f'  {s} -->|"{st}: {note}"| {d}')
lines += ['```','','## Edge review','']
for e in data.get('edges',[]):
    lines.append(f"- **{e['from']} -> {e['to']}** — {e.get('state')} — {e.get('note','')}")
out=pathlib.Path(sys.argv[2]); out.parent.mkdir(parents=True,exist_ok=True); out.write_text('\n'.join(lines)+'\n'); out.chmod(0o600); print(out)
