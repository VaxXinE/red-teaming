#!/usr/bin/env python3
"""Concurrency demo for the local Module 12 race-condition endpoint only."""
import concurrent.futures
from urllib.request import Request, urlopen
from urllib.error import HTTPError
URL='http://127.0.0.1:8120/race/redeem'

def one(_):
    req=Request(URL, data=b'', method='POST')
    try:
        with urlopen(req, timeout=3) as r:
            return r.status, r.read().decode(errors='replace').strip()
    except HTTPError as e:
        return e.code, e.read().decode(errors='replace').strip()
    except Exception as e:
        return 0, str(e)

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        results=list(ex.map(one, range(10)))
    for i,(code,text) in enumerate(results,1):
        print(f'{i:02d} status={code} body={text}')
if __name__=='__main__': main()
