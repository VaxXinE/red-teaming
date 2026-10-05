#!/usr/bin/env python3
import argparse, os
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('path'); p.add_argument('--title',required=True); p.add_argument('--evidence',required=True); p.add_argument('--impact',required=True); p.add_argument('--remediation',required=True); p.add_argument('--assumptions',default='')
a=p.parse_args(); out=Path(a.path); out.parent.mkdir(parents=True,exist_ok=True)
text=f"# {a.title}\n\n## Evidence\n{a.evidence}\n\n## Assumptions / Preconditions\n{a.assumptions or 'Document required privileges and environmental assumptions.'}\n\n## Impact\n{a.impact}\n\n## Remediation\n{a.remediation}\n"
out.write_text(text,encoding='utf-8'); os.chmod(out,0o600); print(out)
