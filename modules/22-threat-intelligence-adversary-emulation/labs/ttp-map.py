#!/usr/bin/env python3
import argparse, csv, json, pathlib, sys

def main():
    p=argparse.ArgumentParser(description="Validate analyst-proposed ATT&CK mappings against a small local training catalog.")
    p.add_argument("intel")
    p.add_argument("--catalog", default=str(pathlib.Path(__file__).with_name("attack-catalog.json")))
    p.add_argument("--output", required=True)
    args=p.parse_args()
    intel=json.load(open(args.intel, encoding="utf-8")); catalog=json.load(open(args.catalog, encoding="utf-8"))
    rows=[]
    for b in intel.get("behaviors",[]):
        tid=b.get("candidate_technique_id","")
        if tid not in catalog:
            print(f"unknown technique id: {tid}", file=sys.stderr); sys.exit(2)
        meta=catalog[tid]
        rows.append({"sequence":b.get("sequence"),"technique_id":tid,"technique":meta["name"],"tactic":meta["tactic"],
                     "confidence":b.get("confidence","low"),"observation":b.get("observation","").strip(),"source":b.get("source","")})
    pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=rows[0].keys() if rows else ["sequence","technique_id","technique","tactic","confidence","observation","source"])
        w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} mappings -> {args.output}")
if __name__=="__main__": main()
