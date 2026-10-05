#!/usr/bin/env python3
import argparse, pathlib, re, sys
REQ=['title:','status:','logsource:','detection:','condition:','falsepositives:','level:']
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('rule'); a=ap.parse_args(); text=pathlib.Path(a.rule).read_text()
    missing=[k for k in REQ if k not in text]
    if missing:
        print('missing: '+', '.join(missing),file=sys.stderr); raise SystemExit(2)
    if 'RTLAB24_MARKER' not in text: print('warning: training marker not found')
    print('PASS: minimum training-rule structure present (not a full Sigma schema validation)')
if __name__=='__main__': main()
