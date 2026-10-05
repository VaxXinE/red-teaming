#!/usr/bin/env python3
import argparse,json,statistics
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('log'); a=ap.parse_args()
rows=[json.loads(x) for x in Path(a.log).read_text().splitlines() if x.strip()]
polls={}
for r in rows:
    if r.get('event')=='poll': polls.setdefault(r.get('agent_id','?'),[]).append(float(r['ts']))
for aid,times in polls.items():
    ints=[b-a for a,b in zip(times,times[1:])]
    print(f'agent={aid} polls={len(times)}')
    if ints:
        mean=statistics.mean(ints); med=statistics.median(ints); sd=statistics.pstdev(ints) if len(ints)>1 else 0; cv=(sd/mean) if mean else 0
        print(f'  interval mean={mean:.3f}s median={med:.3f}s min={min(ints):.3f}s max={max(ints):.3f}s cv={cv:.3f}')
        print('  interpretation: lower CV means more regular timing; correlate with process/destination context before alerting.')
print('event_counts:')
from collections import Counter
for k,v in Counter(r.get('event') for r in rows).most_common(): print(f'  {k}: {v}')
