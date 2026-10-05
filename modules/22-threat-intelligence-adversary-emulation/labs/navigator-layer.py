#!/usr/bin/env python3
import argparse, csv, json, pathlib
COLORS={"high":"#2ca25f","medium":"#feb24c","low":"#de2d26"}
SCORES={"high":90,"medium":60,"low":30}
def main():
    p=argparse.ArgumentParser(description="Generate a minimal ATT&CK Navigator layer from mapping CSV.")
    p.add_argument("csv_file"); p.add_argument("--output", required=True); p.add_argument("--name", default="Module 22 - Synthetic Adversary")
    args=p.parse_args(); techniques=[]
    with open(args.csv_file,newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):
            c=r.get("confidence","low").lower()
            techniques.append({"techniqueID":r["technique_id"],"score":SCORES.get(c,30),"color":COLORS.get(c,COLORS["low"]),
                               "comment":f"{r.get('observation','')} | Source: {r.get('source','')}"})
    layer={"name":args.name,"domain":"enterprise-attack","description":"Training layer generated from analyst mappings. Scores represent mapping confidence, NOT detection coverage.",
           "sorting":2,"layout":{"layout":"side","showName":True,"showID":True,"showAggregateScores":True,"countUnscored":False,"aggregateFunction":"average"},
           "hideDisabled":False,"techniques":techniques,"legendItems":[{"label":"High confidence mapping","color":COLORS["high"]},{"label":"Medium confidence mapping","color":COLORS["medium"]},{"label":"Low confidence mapping","color":COLORS["low"]}]}
    pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    json.dump(layer,open(args.output,"w",encoding="utf-8"),indent=2)
    print(f"wrote Navigator layer -> {args.output}")
if __name__=="__main__": main()
