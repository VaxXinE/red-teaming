#!/usr/bin/env python3
import argparse
LEVELS=['Informational','Low','Medium','High','Critical']
MATRIX={
(1,1):1,(1,2):1,(1,3):2,(1,4):2,(1,5):3,
(2,1):1,(2,2):2,(2,3):2,(2,4):3,(2,5):3,
(3,1):2,(3,2):2,(3,3):3,(3,4):3,(3,5):4,
(4,1):2,(4,2):3,(4,3):3,(4,4):4,(4,5):4,
(5,1):3,(5,2):3,(5,3):4,(5,4):4,(5,5):4,
}
def main():
    ap=argparse.ArgumentParser(description='Training-only qualitative risk matrix. Not CVSS.')
    ap.add_argument('--likelihood', type=int, choices=range(1,6), required=True)
    ap.add_argument('--impact', type=int, choices=range(1,6), required=True)
    a=ap.parse_args()
    idx=MATRIX[(a.likelihood,a.impact)]
    print(f'likelihood={a.likelihood} impact={a.impact} risk={LEVELS[idx]}')
if __name__=='__main__': main()
