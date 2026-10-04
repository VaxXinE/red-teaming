#!/usr/bin/env python3
from __future__ import annotations
import argparse, socket

def main():
    ap=argparse.ArgumentParser(description='Tiny UDP echo service for Module 08')
    ap.add_argument('--host',default='0.0.0.0')
    ap.add_argument('--port',type=int,default=9999)
    args=ap.parse_args()
    if not (1 <= args.port <= 65535):
        raise SystemExit('invalid port')
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
        s.bind((args.host,args.port))
        while True:
            data,addr=s.recvfrom(2048)
            reply=b'REDLAB08 UDP ECHO: '+data[:512]
            s.sendto(reply,addr)
if __name__=='__main__': main()
