# Module 20 - Kerberos & Active Directory Attack Paths

Module ini melanjutkan Active Directory Fundamentals (18) dan AD Enumeration (19) dengan fokus pada **attack-path reasoning**: Kerberos ticket flow, SPN/service identities, delegation, ACL relationships, trusts, AD CS, BloodHound graph interpretation, controlled validation, telemetry, evidence, dan remediation.

## Learning goals

- Memahami TGT, service tickets, KDC, SPN, PAC, dan authentication/authorization boundary.
- Menilai service identities dan SPNs sebagai relationship evidence, bukan otomatis vulnerability.
- Memetakan unconstrained/constrained/resource-based constrained delegation secara read-only.
- Membaca ACL edges dan BloodHound paths sebagai hypotheses yang harus divalidasi.
- Memahami trust direction/transitivity/selective authentication dan AD CS certificate-template risk factors.
- Membuat attack-path hypothesis yang punya preconditions, uncertainty, rollback, telemetry, dan remediation.

## Safety model

Hands-on menggunakan synthetic datasets, read-only PowerShell inventory, dan authorized isolated AD labs. Module ini **tidak** menyediakan automation untuk ticket extraction, credential cracking, ACL/delegation modification, certificate impersonation, persistence, atau remote execution.

## Files

- `pdf/` - final learning module.
- `docx/` - editable source.
- `labs/` - safe helpers dan synthetic datasets.

## Recommended lab

GOAD/MINILAB boleh dipakai hanya dalam jaringan terisolasi. Project GOAD sendiri memperingatkan bahwa environment sangat vulnerable dan tidak boleh dipublish ke internet.
