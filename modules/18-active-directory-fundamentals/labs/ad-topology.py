#!/usr/bin/env python3
import argparse, json, pathlib
p=argparse.ArgumentParser(description='Render a small AD topology JSON into Markdown.')
p.add_argument('--input',required=True); p.add_argument('--output',required=True)
a=p.parse_args()
data=json.loads(pathlib.Path(a.input).read_text())
lines=['# Active Directory Topology Map','']
for forest in data.get('forests',[]):
    lines += [f"## Forest: {forest.get('name','unknown')}",'']
    for domain in forest.get('domains',[]):
        lines += [f"### Domain: {domain.get('name','unknown')}"]
        if domain.get('dcs'):
            lines.append('- Domain Controllers: ' + ', '.join(domain['dcs']))
        if domain.get('dns_servers'):
            lines.append('- DNS: ' + ', '.join(domain['dns_servers']))
        if domain.get('ous'):
            lines.append('- OUs: ' + ', '.join(domain['ous']))
        if domain.get('groups'):
            lines.append('- Groups: ' + ', '.join(domain['groups']))
        if domain.get('spns'):
            lines.append('- Sample SPNs: ' + ', '.join(domain['spns']))
        lines.append('')
    trusts=forest.get('trusts',[])
    if trusts:
        lines.append('### Trusts')
        for t in trusts:
            lines.append(f"- {t.get('source')} -> {t.get('target')} ({t.get('type','unknown')})")
        lines.append('')
out=pathlib.Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
out.write_text('\n'.join(lines)+'\n')
out.chmod(0o600)
print(out)
