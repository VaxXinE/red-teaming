#!/usr/bin/env python3
import argparse
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description='Create a minimal Module 12 finding note.')
    p.add_argument('output')
    for name in ('title','category','endpoint','evidence','impact','remediation'):
        p.add_argument(f'--{name}', required=True)
    a=p.parse_args()
    out=Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    body=f'''# {a.title}\n\nCategory: {a.category}\nEndpoint: {a.endpoint}\n\n## Evidence\n{a.evidence}\n\n## Impact\n{a.impact}\n\n## Remediation\n{a.remediation}\n'''
    out.write_text(body, encoding='utf-8')
    out.chmod(0o600)
    print(out)
if __name__=='__main__': main()
