# Module 19 — Active Directory Enumeration

Module ini mengubah fondasi AD dari Module 18 menjadi workflow enumeration yang bisa diaudit: DNS/DC discovery, LDAP, native PowerShell, users/groups/computers, nested memberships, SPNs, SMB/RPC, GPO links, sample ACLs, trusts, BloodHound CE, dan attack-path reasoning.

## Safety boundary

Gunakan hanya pada GOAD/MINILAB, domain milik sendiri, HTB/THM, atau engagement dengan izin tertulis. Enumeration tetap menghasilkan network traffic dan telemetry.

Module ini **tidak** melakukan password spraying, Kerberoasting, remote execution, ACL/GPO modification, persistence, credential dumping, atau privilege escalation.

## Struktur

```text
19-active-directory-enumeration/
├── README.md
├── docx/
├── pdf/
└── labs/
```

## Lab flow

1. DNS/DC baseline
2. LDAP RootDSE + object inventory
3. PowerShell structured inventory
4. Nested group relationships
5. SPN/service account inventory
6. SMB/RPC read-only review
7. GPO links
8. Sample AD ACL review
9. Trust map
10. BloodHound CE DCOnly baseline
11. Attack-path triage
12. Evidence manifest + capstone

Treat BloodHound edges as relationship evidence that still requires provenance, freshness, precondition, scope, and reachability validation.
