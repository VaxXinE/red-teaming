#!/usr/bin/env python3
import argparse, json
from collections import deque
p=argparse.ArgumentParser(description='Find a path in a synthetic AD relationship graph. Does not execute abuse steps.')
p.add_argument('graph')
p.add_argument('--from-node', dest='src', required=True)
p.add_argument('--to-node', dest='dst', required=True)
a=p.parse_args()
d=json.load(open(a.graph, encoding='utf-8'))
adj={n:[] for n in d.get('nodes',[])}
for e in d.get('edges',[]): adj.setdefault(e['from'],[]).append((e['to'],e['type']))
q=deque([(a.src,[])]) ; seen={a.src}
while q:
    node,path=q.popleft()
    if node==a.dst:
        print(a.src)
        for edge,to in path: print(f"  --[{edge}]--> {to}")
        raise SystemExit(0)
    for to,edge in adj.get(node,[]):
        if to not in seen:
            seen.add(to); q.append((to,path+[(edge,to)]))
print('No path found')
raise SystemExit(2)
