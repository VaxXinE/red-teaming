#!/usr/bin/env python3
import argparse, os
from pathlib import Path

TEMPLATE = """# {ref} - {title}\n\n**Severity:** {severity}\n\n**Affected asset(s):** {asset}\n\n## Summary\n{summary}\n\n## Preconditions\n- TODO\n\n## Technical details\nTODO: explain root cause, trust boundary, and affected component.\n\n## Evidence\n- TODO: evidence path / screenshot / raw request-response / command output.\n\n## Reproduction\n1. TODO\n2. TODO\n\n## Impact\nTODO: describe realistic technical and business impact.\n\n## Remediation\n1. TODO: durable root-cause fix.\n2. TODO: compensating control if relevant.\n\n## Validation / Retest\n- Status: Not retested\n- Evidence: TODO\n\n## References\n- TODO\n"""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output')
    ap.add_argument('--ref', required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--severity', default='TBD')
    ap.add_argument('--asset', default='TBD')
    ap.add_argument('--summary', default='TODO')
    a=ap.parse_args()
    out=Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TEMPLATE.format(**vars(a)), encoding='utf-8')
    os.chmod(out, 0o600)
    print(out)
if __name__=='__main__': main()
