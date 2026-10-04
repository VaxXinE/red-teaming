#!/usr/bin/env python3
import argparse, os
from pathlib import Path
p=argparse.ArgumentParser(description='Create a compact Module 16 finding note.')
p.add_argument('output')
p.add_argument('--title', required=True)
p.add_argument('--vector', required=True)
p.add_argument('--evidence', required=True)
p.add_argument('--impact', required=True)
p.add_argument('--remediation', required=True)
a=p.parse_args()
out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
text=f"""# {a.title}\n\n## Vector\n{a.vector}\n\n## Evidence\n{a.evidence}\n\n## Impact\n{a.impact}\n\n## Root Cause\nPrivilege boundary trusts attacker-controlled input or permission.\n\n## Remediation\n{a.remediation}\n\n## Retest\n- [ ] Privileged primitive removed or constrained\n- [ ] Original proof no longer succeeds\n- [ ] Legitimate function still works\n"""
out.write_text(text, encoding='utf-8')
os.chmod(out, 0o600)
print(out)
