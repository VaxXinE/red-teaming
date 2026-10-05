#!/usr/bin/env python3
import argparse, json, pathlib
from datetime import datetime, timezone, timedelta

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); a=ap.parse_args(); out=pathlib.Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    t=datetime.now(timezone.utc).replace(microsecond=0)
    rows=[
      (0,'process_create',{'host':'lab-win','user':'student','process':'powershell.exe','parent':'explorer.exe','command_line':'powershell.exe -NoProfile -Command "Write-Output RTLAB24_MARKER"'}),
      (2,'file_create',{'host':'lab-win','user':'student','process':'powershell.exe','path':'C:\\Lab\\RTLAB24_MARKER.txt','sha256':'traininghash'}),
      (4,'dns_query',{'host':'lab-win','user':'student','process':'powershell.exe','query':'training.invalid'}),
      (5,'network_connect',{'host':'lab-win','user':'student','process':'powershell.exe','destination':'127.0.0.1','port':8240}),
      (8,'file_delete',{'host':'lab-win','user':'student','process':'powershell.exe','path':'C:\\Lab\\RTLAB24_MARKER.txt'}),
      (10,'cleanup',{'host':'lab-win','user':'student','status':'verified'})]
    with out.open('w') as f:
        for off,kind,data in rows:
            f.write(json.dumps({'timestamp_utc':(t+timedelta(seconds=off)).isoformat().replace('+00:00','Z'),'event':kind,'marker':'RTLAB24_MARKER',**data},sort_keys=True)+'\n')
    out.chmod(0o600); print(out)
if __name__=='__main__': main()
