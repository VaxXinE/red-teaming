#!/usr/bin/env python3
import argparse, datetime, os
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('file'); ap.add_argument('--observation',required=True); ap.add_argument('--hypothesis',required=True); ap.add_argument('--test',required=True); ap.add_argument('--result',required=True); ap.add_argument('--confidence',choices=['low','medium','high'],required=True); ap.add_argument('--next',default='')
a=ap.parse_args(); p=Path(a.file); p.parent.mkdir(parents=True,exist_ok=True)
text=f"\n## {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n- Observation: {a.observation}\n- Hypothesis: {a.hypothesis}\n- Test: {a.test}\n- Result: {a.result}\n- Confidence: {a.confidence}\n- Next action: {a.next or 'none'}\n"
fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o600)
with os.fdopen(fd,'a') as f:f.write(text)
print(p)
