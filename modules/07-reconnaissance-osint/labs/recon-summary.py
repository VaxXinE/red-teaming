#!/usr/bin/env python3
"""Create a small Markdown recon summary from assets.csv."""
import argparse, collections, csv, os
from pathlib import Path

def main():
    os.umask(0o077)
    ap=argparse.ArgumentParser(); ap.add_argument("csv_file",type=Path); ap.add_argument("--output",type=Path,default=Path("recon-summary.md")); args=ap.parse_args()
    rows=list(csv.DictReader(args.csv_file.open(encoding='utf-8')))
    by_scope=collections.Counter(r.get('scope_status','unknown') for r in rows)
    by_type=collections.Counter(r.get('asset_type','unknown') for r in rows)
    lines=["# Recon Summary","",f"Total observations: **{len(rows)}**","","## By scope status"]
    lines += [f"- {k}: {v}" for k,v in sorted(by_scope.items())] or ["- none"]
    lines += ["","## By asset type"] + ([f"- {k}: {v}" for k,v in sorted(by_type.items())] or ["- none"])
    lines += ["","## Candidate assets requiring validation"]
    candidates=[r for r in rows if r.get('scope_status') in {'candidate','needs-validation'}]
    if candidates:
        for r in candidates: lines.append(f"- `{r.get('value','')}` ({r.get('asset_type','')}) via {r.get('source','')}; confidence={r.get('confidence','')}")
    else: lines.append("- none")
    lines += ["","> Discovery does not equal authorization. Validate ownership and scope before active testing.",""]
    args.output.write_text("\n".join(lines),encoding='utf-8');
    try: args.output.chmod(0o600)
    except OSError: pass
    print(f"wrote {args.output}")
    return 0
if __name__=='__main__': raise SystemExit(main())
