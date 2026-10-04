#!/usr/bin/env python3
from __future__ import annotations
import argparse, os
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Create a minimal credential-security finding note.')
    ap.add_argument('output')
    ap.add_argument('--title',required=True)
    ap.add_argument('--evidence',required=True)
    ap.add_argument('--impact',required=True)
    ap.add_argument('--remediation',required=True)
    args=ap.parse_args()
    p=Path(args.output); p.parent.mkdir(parents=True,exist_ok=True)
    text=f'''# {args.title}\n\n## Evidence\n{args.evidence}\n\n## Impact\n{args.impact}\n\n## Remediation\n{args.remediation}\n\n## Handling note\nDo not include real plaintext credentials in reports unless explicitly required and protected. Prefer redacted identifiers and evidence references.\n'''
    p.write_text(text,encoding='utf-8'); os.chmod(p,0o600); print(p)
if __name__=='__main__': main()
