#!/usr/bin/env python3
import argparse, json, pathlib, sys
REQ = ["engagement","objective","scope","allowed_actions","prohibited_actions","stop_conditions","exposure_budget","expected_telemetry","cleanup_owner","evidence_plan"]
def load(p):
    return json.loads(pathlib.Path(p).read_text())
def validate(d):
    missing=[k for k in REQ if k not in d]
    if missing: return False, [f"missing: {x}" for x in missing]
    errs=[]
    if not isinstance(d["scope"], list) or not d["scope"]: errs.append("scope must be a non-empty list")
    if not isinstance(d["prohibited_actions"], list) or not d["prohibited_actions"]: errs.append("prohibited_actions required")
    b=d.get("exposure_budget",{})
    for k in ("hosts","duration_minutes","max_requests","max_privilege"):
        if k not in b: errs.append(f"exposure_budget.{k} missing")
    return len(errs)==0, errs
def render(d):
    lines=[f"# OPSEC Plan - {d['engagement']}","",f"**Objective:** {d['objective']}","","## Scope"]
    lines += [f"- {x}" for x in d["scope"]]
    for key,title in [("allowed_actions","Allowed Actions"),("prohibited_actions","Prohibited Actions"),("stop_conditions","Stop Conditions"),("expected_telemetry","Expected Telemetry"),("evidence_plan","Evidence Plan")]:
        lines += ["",f"## {title}"]+[f"- {x}" for x in d[key]]
    lines += ["","## Exposure Budget"]+[f"- {k}: {v}" for k,v in d["exposure_budget"].items()]
    lines += ["",f"**Cleanup owner:** {d['cleanup_owner']}",""]
    return "\n".join(lines)
def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    v=sp.add_parser('validate'); v.add_argument('plan')
    r=sp.add_parser('render'); r.add_argument('plan'); r.add_argument('--output',required=True)
    a=ap.parse_args(); d=load(a.plan); ok,errs=validate(d)
    if not ok:
        for e in errs: print(e,file=sys.stderr)
        raise SystemExit(2)
    if a.cmd=='validate': print('PASS: OPSEC plan structure is complete')
    else:
        out=pathlib.Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(render(d)); out.chmod(0o600); print(out)
if __name__=='__main__': main()
