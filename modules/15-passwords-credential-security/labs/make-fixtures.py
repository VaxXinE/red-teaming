#!/usr/bin/env python3
from __future__ import annotations
import hashlib, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parent/'fixtures'
ROOT.mkdir(exist_ok=True)
accounts=[
    ('alice','Training123!','mod15a'),
    ('bob','BlueTeam2026','mod15b'),
    ('carol','MapleRiver22','mod15c'),
]
wordlist=['password','Password123','Training123!','BlueTeam','BlueTeam2026','MapleRiver','MapleRiver22','Welcome1!','letmein']
(ROOT/'lab-wordlist.txt').write_text('\n'.join(wordlist)+'\n',encoding='utf-8')
(ROOT/'blocklist.txt').write_text('password\npassword123\nqwerty123\nletmein\nwelcome1!\nadmin123\n',encoding='utf-8')
lines=[]; hashcat=[]
for user,pw,salt in accounts:
    cp=subprocess.run(['openssl','passwd','-6','-salt',salt,pw],check=True,capture_output=True,text=True)
    h=cp.stdout.strip(); lines.append(f'{user}:{h}'); hashcat.append(h)
(ROOT/'john-sha512crypt.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(ROOT/'hashcat-sha512crypt.txt').write_text('\n'.join(hashcat)+'\n',encoding='utf-8')
raw=hashlib.sha256(b'Training123!').hexdigest()
(ROOT/'raw-sha256.txt').write_text(raw+'\n',encoding='utf-8')
(ROOT/'dummy-credentials.csv').write_text(
    'system,username,password,mfa\n'
    'portal-a,alice,Training123!,yes\n'
    'portal-b,alice,Training123!,no\n'
    'vpn,bob,BlueTeam2026,yes\n'
    'wiki,bob,BlueTeam2026,no\n'
    'lab,carol,MapleRiver22,no\n',encoding='utf-8')
print('fixtures written to',ROOT)
