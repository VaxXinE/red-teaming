#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Create a Module 11 finding note')
    ap.add_argument('output',type=Path); ap.add_argument('--title',required=True); ap.add_argument('--category',required=True)
    ap.add_argument('--endpoint',required=True); ap.add_argument('--evidence',required=True); ap.add_argument('--impact',required=True); ap.add_argument('--remediation',required=True)
    ns=ap.parse_args(); ns.output.parent.mkdir(parents=True,exist_ok=True)
    ts=datetime.datetime.now(datetime.timezone.utc).isoformat()
    ns.output.write_text(f'''# {ns.title}\n\n- Category: {ns.category}\n- Endpoint: {ns.endpoint}\n- Timestamp UTC: {ts}\n\n## Evidence\n{ns.evidence}\n\n## Impact\n{ns.impact}\n\n## Remediation\n{ns.remediation}\n''',encoding='utf-8')
    ns.output.chmod(0o600)
    print(ns.output)
if __name__=='__main__': main()
