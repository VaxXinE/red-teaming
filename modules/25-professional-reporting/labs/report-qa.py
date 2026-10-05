#!/usr/bin/env python3
import argparse, re, sys
from pathlib import Path

REQ_HEADINGS=[
'Executive Summary','Scope','Methodology','Attack Path','Findings Summary','Detailed Findings','Remediation Roadmap','Limitations','Appendix'
]
SECRET_PATTERNS=[
('private-key', re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),
('aws-access-key', re.compile(r'AKIA[0-9A-Z]{16}')),
('generic-token', re.compile(r'(?i)(?:api[_-]?key|token|secret|password)\s*[:=]\s*[^\s`]{8,}')),
]
PLACEHOLDERS=re.compile(r'\b(?:TODO|TBD|FIXME|CHANGEME)\b', re.I)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('report')
    ap.add_argument('--evidence-root', default=None)
    a=ap.parse_args()
    p=Path(a.report)
    text=p.read_text(encoding='utf-8', errors='replace')
    issues=[]
    for h in REQ_HEADINGS:
        if h.lower() not in text.lower(): issues.append(f'missing section: {h}')
    for m in PLACEHOLDERS.finditer(text): issues.append(f'placeholder remains: {m.group(0)}')
    for name,rx in SECRET_PATTERNS:
        if rx.search(text): issues.append(f'possible secret exposure: {name}')
    if a.evidence_root:
        root=Path(a.evidence_root)
        for ref in re.findall(r'\[evidence:([^\]]+)\]', text, flags=re.I):
            target=(root/ref.strip()).resolve()
            try: target.relative_to(root.resolve())
            except ValueError:
                issues.append(f'evidence path escapes root: {ref}')
                continue
            if not target.exists(): issues.append(f'missing evidence: {ref}')
    if issues:
        print('QA FAIL')
        for i in issues: print(f'- {i}')
        sys.exit(1)
    print('QA PASS')
if __name__=='__main__': main()
