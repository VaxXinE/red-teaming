#!/usr/bin/env python3
import argparse, csv, pathlib
ALLOWED={"blocked","detected","logged-only","missed","not-testable"}
def main():
 p=argparse.ArgumentParser(description="Record an emulation result without overstating detection quality.")
 p.add_argument("--technique",required=True); p.add_argument("--status",choices=sorted(ALLOWED),required=True); p.add_argument("--telemetry",default=""); p.add_argument("--notes",default=""); p.add_argument("--output",required=True)
 a=p.parse_args(); path=pathlib.Path(a.output); path.parent.mkdir(parents=True,exist_ok=True); exists=path.exists()
 with path.open("a",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=["technique_id","status","telemetry_reference","notes"])
  if not exists: w.writeheader()
  w.writerow({"technique_id":a.technique,"status":a.status,"telemetry_reference":a.telemetry,"notes":a.notes})
 print(f"appended result -> {path}")
if __name__=="__main__": main()
