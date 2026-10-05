# Module 25 - Professional Pentest / Red Team Reporting

Module ini mengubah technical assessment menjadi deliverable profesional: evidence standards, finding structure, severity/risk communication, CVSS v4.0 hygiene, attack-path narrative, executive summary, remediation, retest, screenshot/redaction hygiene, report security, peer review, dan final QA.

## Contents

- `docx/` - editable source document
- `pdf/` - final learning module
- `labs/` - local-only reporting utilities and templates

## Safety

Semua lab pada module ini hanya memproses file lokal. Tidak ada scanning, exploitation, credential attack, atau remote target. Raw evidence dari engagement nyata harus diperlakukan sebagai sensitive data dan mengikuti scope, retention, privacy, dan delivery policy organisasi.

## Lab utilities

- `workspace-init.sh` - private reporting workspace
- `finding-note.py` - finding template generator
- `evidence-index.py` - file index + SHA-256
- `evidence-manifest.sh` - SHA-256 manifest
- `severity-matrix.py` - training-only qualitative matrix (**not CVSS**)
- `report-qa.py` - Markdown structure/placeholder/basic-secret/evidence-reference lint
- `report-template.md` - full report skeleton
- `sample-finding.md` - example high-quality finding

## Primary references

- NIST SP 800-115
- OWASP Web Security Testing Guide - Reporting
- FIRST CVSS v4.0
- OffSec OSCP+ Reporting Requirements / Exam Guide
