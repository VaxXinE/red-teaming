#!/usr/bin/env python3
import pathlib,sys,re
if len(sys.argv)!=4: raise SystemExit(f'usage: {sys.argv[0]} <ID> <title> <output.md>')
fid,title,out=sys.argv[1:]
if not re.fullmatch(r'[A-Z]+-\d{3}',fid): raise SystemExit('finding id should look like F-001')
p=pathlib.Path(out); p.parent.mkdir(parents=True,exist_ok=True)
text=f'''# {fid} - {title}

## Status
Draft

## Severity / risk rationale
TODO

## Affected assets
TODO

## Summary
TODO

## Preconditions
TODO

## Observation / evidence
- Baseline: TODO
- Changed condition: TODO
- Observed result: TODO
- Raw evidence references: TODO

## Validated impact
TODO

## Potential impact (clearly labeled)
TODO

## Root cause
TODO

## Remediation
TODO

## Retest criteria
TODO

## Detection / telemetry notes
TODO
'''
p.write_text(text); p.chmod(0o600); print(p)
