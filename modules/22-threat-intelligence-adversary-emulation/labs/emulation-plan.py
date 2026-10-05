#!/usr/bin/env python3
import argparse, csv, pathlib

def main():
    p=argparse.ArgumentParser(description="Generate a conservative micro-emulation plan from reviewed behavior mappings.")
    p.add_argument("csv_file"); p.add_argument("--output", required=True)
    args=p.parse_args(); rows=list(csv.DictReader(open(args.csv_file,newline="",encoding="utf-8"))); rows.sort(key=lambda r:int(r.get('sequence') or 0))
    out=["# Micro Emulation Plan - Module 22","","## Objective","Validate visibility and detection of a small, discovery-focused behavior chain in an authorized disposable lab.","","## Rules","- Lab/VM only; no production targets.","- Use native, read-only discovery commands.","- Review every action before execution.","- Stop if scope, telemetry, or system health becomes uncertain.","","## Steps"]
    for idx,r in enumerate(rows,1):
        out += [f"### Step {idx} - {r['technique_id']} {r['technique']}",f"- Intelligence basis: {r['observation']}",f"- Mapping confidence: {r['confidence']}","- Execution: use the low-risk local behavior from the module lab.","- Expected telemetry: process creation / command line / script activity where collection is enabled.","- Evidence: timestamp, host, command, result, relevant event/log reference.","- Cleanup: none expected for read-only discovery; verify no artifacts were created.",""]
    out += ["## Success criteria","- Every step is either blocked, detected, logged-only, or explicitly documented as missed.","- Evidence links behavior to telemetry.","- No step leaves persistent configuration or credentials behind."]
    pathlib.Path(args.output).parent.mkdir(parents=True,exist_ok=True); pathlib.Path(args.output).write_text('\n'.join(out),encoding='utf-8'); print(f"wrote {args.output}")
if __name__=="__main__": main()
