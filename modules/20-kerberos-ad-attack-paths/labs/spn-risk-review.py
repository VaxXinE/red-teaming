#!/usr/bin/env python3
import argparse, csv, json
from pathlib import Path

p=argparse.ArgumentParser(description='Rank synthetic SPN-bearing accounts for review. No ticket extraction or cracking.')
p.add_argument('csv_file')
p.add_argument('--output', default='spn-review.json')
a=p.parse_args()
rows=[]
with open(a.csv_file, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        score=0; reasons=[]
        age=int(r['PasswordAgeDays'])
        enc=r['EncryptionTypes'].upper()
        if age >= 365: score+=2; reasons.append('password age >= 365 days')
        if 'RC4' in enc: score+=2; reasons.append('legacy RC4 listed')
        if r['Privileged'].lower() == 'true': score+=3; reasons.append('privileged service identity')
        if not r['SamAccountName'].endswith('$'): score+=1; reasons.append('user-backed service account')
        rows.append({'account':r['SamAccountName'],'score':score,'reasons':reasons,'spns':r['SPNs']})
rows.sort(key=lambda x:(-x['score'],x['account']))
Path(a.output).write_text(json.dumps(rows, indent=2), encoding='utf-8')
for x in rows:
    print(f"{x['score']:>2}  {x['account']:<16}  {', '.join(x['reasons']) or 'baseline'}")
