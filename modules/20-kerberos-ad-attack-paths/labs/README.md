# Module 20 Lab Helpers

Helper di folder ini dibuat untuk **authorized Active Directory training lab** seperti GOAD/MINILAB yang terisolasi atau synthetic datasets bawaan module.

## Guardrails

- Script Python bekerja pada synthetic/read-only data dan tidak mengeksekusi abuse action.
- PowerShell helper melakukan read-only inventory terhadap ticket cache, delegation, trusts, dan AD CS objects.
- Tidak ada password spraying, ticket extraction, Kerberos hash cracking, ACL modification, delegation modification, certificate abuse, atau remote execution.
- Simpan domain credential melalui mekanisme interactive/Windows logon context; jangan hard-code secret ke repository.

## Quick start

```bash
./workspace-init.sh module20-ad-paths
python ./spn-risk-review.py ./sample-spns.csv --output module20-ad-paths/02-spn/spn-review.json
python ./attack-path-model.py ./sample-acl.json --from-node STUDENT --to-node 'DOMAIN ADMINS'
python ./trust-path.py ./sample-trust.json
```

Di Windows domain-joined lab:

```powershell
.\ticket-cache.ps1
.\delegation-inventory.ps1
.\trust-inventory.ps1
.\adcs-inventory.ps1
```
