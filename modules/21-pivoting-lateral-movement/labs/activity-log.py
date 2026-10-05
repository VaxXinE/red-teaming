#!/usr/bin/env python3
import argparse, datetime, os
from pathlib import Path
p=argparse.ArgumentParser(description='Append a timestamped Module 21 activity record.')
p.add_argument('file')
p.add_argument('--action', required=True)
p.add_argument('--source', required=True)
p.add_argument('--destination', required=True)
p.add_argument('--purpose', required=True)
a=p.parse_args()
path=Path(a.file); path.parent.mkdir(parents=True, exist_ok=True)
new=not path.exists()
with path.open('a', encoding='utf-8') as f:
    if new: f.write('timestamp\taction\tsource\tdestination\tpurpose\n')
    ts=datetime.datetime.now(datetime.timezone.utc).isoformat()
    f.write(f'{ts}\t{a.action}\t{a.source}\t{a.destination}\t{a.purpose}\n')
os.chmod(path,0o600)
