#!/usr/bin/env python3
import sys, json

def split_dn(dn: str):
    parts=[]; buf=[]; esc=False
    for ch in dn:
        if esc:
            buf.append(ch); esc=False
        elif ch == '\\':
            buf.append(ch); esc=True
        elif ch == ',':
            parts.append(''.join(buf).strip()); buf=[]
        else:
            buf.append(ch)
    if buf: parts.append(''.join(buf).strip())
    result=[]
    for p in parts:
        if '=' not in p: raise ValueError(f'invalid DN component: {p!r}')
        k,v=p.split('=',1); result.append({'type':k.upper(),'value':v})
    return result

if len(sys.argv)!=2:
    raise SystemExit(f'usage: {sys.argv[0]} <distinguished-name>')
parts=split_dn(sys.argv[1])
domain='.'.join(x['value'] for x in parts if x['type']=='DC')
ous=[x['value'] for x in parts if x['type']=='OU']
print(json.dumps({'dn':sys.argv[1],'components':parts,'domain':domain,'ous':ous},indent=2))
