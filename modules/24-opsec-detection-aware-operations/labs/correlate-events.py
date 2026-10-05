#!/usr/bin/env python3
import argparse, json, pathlib

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('events'); a=ap.parse_args(); rows=[json.loads(x) for x in pathlib.Path(a.events).read_text().splitlines() if x.strip()]
    by={}
    for r in rows: by.setdefault((r.get('host'),r.get('user'),r.get('marker')),[]).append(r)
    for key,evs in by.items():
        types=[e['event'] for e in evs]
        print(f'group={key} events={" -> ".join(types)}')
        required={'process_create','file_create','network_connect'}
        print('correlation=', 'MATCH' if required.issubset(types) else 'NO_MATCH')
if __name__=='__main__': main()
