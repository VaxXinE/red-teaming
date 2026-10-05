#!/usr/bin/env python3
import argparse, csv, pathlib, shutil, subprocess

def esc(s): return s.replace('\\','\\\\').replace('"','\\"')
def main():
    p=argparse.ArgumentParser(description="Create a simple ordered ATT&CK behavior flow from mapping CSV.")
    p.add_argument("csv_file"); p.add_argument("--dot", required=True); p.add_argument("--svg")
    args=p.parse_args()
    rows=list(csv.DictReader(open(args.csv_file,newline="",encoding="utf-8")))
    rows.sort(key=lambda r:int(r.get("sequence") or 0))
    lines=['digraph G {','rankdir=LR;','graph [bgcolor="white", pad="0.2", nodesep="0.45"];','node [shape=box, style="rounded,filled", fillcolor="#eef5fb", color="#285a84", fontname="DejaVu Sans"];','edge [color="#52606d"];']
    for i,r in enumerate(rows):
        label=f"{r['technique_id']}\\n{r['technique']}"
        lines.append(f'n{i} [label="{esc(label)}"];')
        if i: lines.append(f'n{i-1} -> n{i};')
    lines.append('}')
    pathlib.Path(args.dot).parent.mkdir(parents=True, exist_ok=True); pathlib.Path(args.dot).write_text('\n'.join(lines),encoding='utf-8')
    if args.svg:
        if not shutil.which('dot'): raise SystemExit("graphviz 'dot' not found")
        subprocess.run(['dot','-Tsvg',args.dot,'-o',args.svg],check=True)
        print(f"wrote {args.dot} and {args.svg}")
    else: print(f"wrote {args.dot}")
if __name__=="__main__": main()
