#!/usr/bin/env python3
import argparse, json
from datetime import datetime, timezone

TYPE_SCORE = {"primary": 35, "official": 32, "secondary": 24, "community": 12}
RECENCY_SCORE = {"current": 25, "recent": 18, "old": 8}
DIRECT_SCORE = {"direct": 20, "corroborated-inference": 14, "inferred": 6}

def confidence(score:int)->str:
    return "high" if score >= 75 else "medium" if score >= 50 else "low"

def main():
    p=argparse.ArgumentParser(description="Score a CTI source for training triage; this is an analyst aid, not truth.")
    p.add_argument("--source", required=True)
    p.add_argument("--type", choices=TYPE_SCORE, required=True)
    p.add_argument("--recency", choices=RECENCY_SCORE, required=True)
    p.add_argument("--directness", choices=DIRECT_SCORE, required=True)
    p.add_argument("--corroboration", type=int, choices=range(0,4), required=True)
    p.add_argument("--notes", default="")
    args=p.parse_args()
    score=min(100, TYPE_SCORE[args.type]+RECENCY_SCORE[args.recency]+DIRECT_SCORE[args.directness]+args.corroboration*7)
    out={"source":args.source,"source_type":args.type,"recency":args.recency,"directness":args.directness,
         "corroboration_count":args.corroboration,"score":score,"confidence":confidence(score),"notes":args.notes,
         "scored_at":datetime.now(timezone.utc).isoformat()}
    print(json.dumps(out, indent=2))
if __name__ == "__main__": main()
