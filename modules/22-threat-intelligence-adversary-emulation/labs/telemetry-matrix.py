#!/usr/bin/env python3
import argparse, csv, pathlib
MATRIX={
 "T1033":("Process creation / shell or PowerShell","whoami / identity query","Was identity discovery launched from an unusual parent or remote session?"),
 "T1082":("Process creation + OS configuration access","systeminfo, uname, os-release","Was system discovery clustered with other discovery actions?"),
 "T1057":("Process creation; optional process API telemetry","tasklist, Get-Process, ps","Was process discovery executed from a non-standard parent or automation context?"),
 "T1087.001":("Process creation + account database/API query","net user, Get-LocalUser, getent passwd","Was local-account discovery followed by credential or privilege activity?")}
def main():
 p=argparse.ArgumentParser(); p.add_argument("csv_file"); p.add_argument("--output",required=True); args=p.parse_args()
 rows=[]
 for r in csv.DictReader(open(args.csv_file,newline="",encoding="utf-8")):
  src,examples,q=MATRIX.get(r['technique_id'],("Define during review","Define during review","What evidence would prove this behavior?"))
  rows.append({"technique_id":r['technique_id'],"technique":r['technique'],"expected_telemetry":src,"benign_examples":examples,"detection_question":q,"collection_status":"unknown","result":"not-tested"})
 pathlib.Path(args.output).parent.mkdir(parents=True,exist_ok=True)
 with open(args.output,"w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
 print(f"wrote {args.output}")
if __name__=="__main__": main()
