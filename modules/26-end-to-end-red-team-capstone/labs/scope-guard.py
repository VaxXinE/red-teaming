#!/usr/bin/env python3
import ipaddress, json, pathlib, sys

ALLOWED_SUFFIXES=(".test", ".lab", ".local")

def check_ip(value):
    ip=ipaddress.ip_address(value)
    return ip.is_private or ip.is_loopback or ip.is_link_local

def check_host(value):
    h=value.lower().rstrip('.')
    return h == 'localhost' or h.endswith(ALLOWED_SUFFIXES)

def main():
    if len(sys.argv)!=2:
        raise SystemExit(f"usage: {sys.argv[0]} <scenario.json>")
    data=json.loads(pathlib.Path(sys.argv[1]).read_text())
    errors=[]
    assets=data.get('assets',[])
    if not assets:
        errors.append('no assets defined')
    for a in assets:
        name=a.get('name','<unnamed>')
        ip=a.get('ip')
        host=a.get('hostname')
        if ip:
            try:
                if not check_ip(ip): errors.append(f'{name}: public/non-lab IP refused: {ip}')
            except ValueError: errors.append(f'{name}: invalid IP: {ip}')
        if host and not check_host(host):
            errors.append(f'{name}: hostname must end in .test/.lab/.local: {host}')
    if errors:
        print('SCOPE GUARD: FAIL')
        for e in errors: print('- '+e)
        return 2
    print(f'SCOPE GUARD: PASS ({len(assets)} assets, lab-only address policy)')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
