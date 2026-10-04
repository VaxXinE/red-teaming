#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, xml.etree.ElementTree as ET
from pathlib import Path

def main() -> int:
    ap=argparse.ArgumentParser(description='Convert Nmap XML to compact inventory CSV')
    ap.add_argument('xml',type=Path); ap.add_argument('--output',type=Path,required=True)
    ns=ap.parse_args()
    root=ET.parse(ns.xml).getroot()
    rows=[]
    for host in root.findall('host'):
        addr=host.find('address'); ip=addr.get('addr','') if addr is not None else ''
        hs=host.find('status'); state=hs.get('state','') if hs is not None else ''
        for p in host.findall('./ports/port'):
            st=p.find('state'); svc=p.find('service')
            rows.append({
                'host':ip,'host_state':state,'protocol':p.get('protocol',''),'port':p.get('portid',''),
                'port_state':st.get('state','') if st is not None else '',
                'service':svc.get('name','') if svc is not None else '',
                'product':svc.get('product','') if svc is not None else '',
                'version':svc.get('version','') if svc is not None else '',
                'extrainfo':svc.get('extrainfo','') if svc is not None else ''})
    ns.output.parent.mkdir(parents=True,exist_ok=True)
    with ns.output.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['host','host_state','protocol','port','port_state','service','product','version','extrainfo']); w.writeheader(); w.writerows(rows)
    print(f'wrote {len(rows)} rows to {ns.output}')
    return 0
if __name__=='__main__': raise SystemExit(main())
