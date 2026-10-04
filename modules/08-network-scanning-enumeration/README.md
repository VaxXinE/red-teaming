# Module 08 - Network Scanning & Enumeration

Module ini membangun workflow enumeration yang repeatable: host discovery, TCP/UDP port scanning, service/version detection, explicit NSE, manual verification, dan evidence handling.

## Files

- `docx/Red-Team-Module-08-Network-Scanning-Enumeration-Omarchy.docx` - editable source
- `pdf/Red-Team-Module-08-Network-Scanning-Enumeration-Omarchy.pdf` - final learning module
- `labs/lab-init.sh` - membuat workspace enumeration
- `labs/multi-service-lab.sh` - membuat/menghapus isolated Docker lab
- `labs/udp-echo.py` - UDP echo service untuk training
- `labs/lab-nmap.py` - Nmap safety wrapper untuk loopback + 172.31.80.0/24
- `labs/nmap-inventory.py` - parse Nmap XML menjadi CSV inventory
- `labs/manual-verify.sh` - manual protocol verification untuk local lab

## Safety

Seluruh included lab dibatasi ke loopback atau subnet Docker training `172.31.80.0/24`. Teknik scanning tetap hanya boleh digunakan terhadap aset milik sendiri atau target yang secara eksplisit mengizinkan pengujian.
