#!/usr/bin/env python3
import argparse, json, pathlib

def classify(s):
    if not s.get('observed'): return 'not-testable'
    if s.get('analytic_expected') and s.get('alert_observed'): return 'detected'
    if s.get('analytic_expected') and not s.get('alert_observed'): return 'missed'
    return 'logged-only'
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('observations'); ap.add_argument('--output',required=True); a=ap.parse_args(); d=json.loads(pathlib.Path(a.observations).read_text())
    out=pathlib.Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    lines=['# Detection Evaluation','', '| Step | Expected telemetry | Observed | Analytic expected | Alert | Classification |','|---|---|:---:|:---:|:---:|---|']
    for s in d['steps']:
        c=classify(s); lines.append(f"| {s['name']} | {s['expected_telemetry']} | {s['observed']} | {s['analytic_expected']} | {s['alert_observed']} | {c} |")
    out.write_text('\n'.join(lines)+'\n'); out.chmod(0o600); print(out)
if __name__=='__main__': main()
