#!/usr/bin/env python3
import argparse,json
p=argparse.ArgumentParser(); p.add_argument('a'); p.add_argument('b'); a=p.parse_args()
A=json.load(open(a.a)); B=json.load(open(a.b))
ka=set(A) if isinstance(A,dict) else set(); kb=set(B) if isinstance(B,dict) else set()
print('only_in_a:',sorted(ka-kb)); print('only_in_b:',sorted(kb-ka)); print('shared:',sorted(ka&kb))
for k in sorted(ka&kb):
    if A[k]!=B[k]: print(f'changed {k!r}: {A[k]!r} -> {B[k]!r}')
