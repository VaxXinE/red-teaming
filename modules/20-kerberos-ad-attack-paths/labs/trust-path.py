#!/usr/bin/env python3
import argparse,json
p=argparse.ArgumentParser(description='Summarize trust direction/transitivity from JSON. No authentication attempts.')
p.add_argument('json_file')
a=p.parse_args(); d=json.load(open(a.json_file, encoding='utf-8'))
for t in d.get('trusts',[]):
    print(f"{t['source']} -> {t['target']} | {t['direction']} | {t['type']} | transitive={t['transitive']} | selectiveAuth={t['selectiveAuth']}")
    if t.get('selectiveAuth'): print('  note: selective authentication narrows who may authenticate across the trust')
