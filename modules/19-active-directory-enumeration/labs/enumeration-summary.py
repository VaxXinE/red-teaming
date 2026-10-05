#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, datetime

ap=argparse.ArgumentParser(description='Summarize Module 19 enumeration evidence without modifying targets.')
ap.add_argument('root', type=Path)
ap.add_argument('--output', type=Path, required=True)
a=ap.parse_args()
if not a.root.is_dir(): raise SystemExit('root directory does not exist')
counts={}
for ext in ('*.csv','*.ldif','*.txt','*.json','*.md','*.zip'):
    counts[ext]=len(list(a.root.rglob(ext)))
lines=[
'# Module 19 Enumeration Summary','',
f'Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}','',
'## Evidence file counts',''
]
for k,v in counts.items(): lines.append(f'- `{k}`: {v}')
lines += ['', '## Analyst checklist','',
'- [ ] Domain/DC validated', '- [ ] Users/groups/computers inventoried', '- [ ] Group relationships reviewed',
'- [ ] SPNs inventoried', '- [ ] SMB shares reviewed', '- [ ] GPO links reviewed', '- [ ] Sample ACLs reviewed',
'- [ ] Trusts reviewed', '- [ ] BloodHound collection timestamp/hash recorded', '- [ ] 3 attack hypotheses documented',
'', '> File counts are not proof of completeness. Review scope, provenance, freshness, and collection errors.'
]
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.write_text('\n'.join(lines)+'\n', encoding='utf-8')
a.output.chmod(0o600)
print(a.output)
