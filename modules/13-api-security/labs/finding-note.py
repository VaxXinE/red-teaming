#!/usr/bin/env python3
import argparse, os
p=argparse.ArgumentParser(); p.add_argument('path'); p.add_argument('--title',required=True); p.add_argument('--category',required=True); p.add_argument('--endpoint',required=True); p.add_argument('--evidence',required=True); p.add_argument('--impact',required=True); p.add_argument('--remediation',required=True); a=p.parse_args()
text=(f'# {a.title}\n\n'
      f'Category: {a.category}\n\n'
      f'Endpoint: `{a.endpoint}`\n\n'
      f'## Evidence\n{a.evidence}\n\n'
      f'## Impact\n{a.impact}\n\n'
      f'## Remediation\n{a.remediation}\n')
os.makedirs(os.path.dirname(a.path) or '.',exist_ok=True)
fd=os.open(a.path,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
with os.fdopen(fd,'w') as f: f.write(text)
print(a.path)
