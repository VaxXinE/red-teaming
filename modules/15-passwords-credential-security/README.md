# Module 15 - Passwords & Credential Security

Omarchy / Arch Linux edition of the Red Team Learning Path.

This module covers credential threat modeling, modern password policy, password hashing/KDFs, salts/peppers, offline password auditing with **dummy local hashes**, John the Ripper, Hashcat, rules/masks/keyspace reasoning, credential reuse, MFA/recovery, credential handling, authentication telemetry, reporting, and remediation.

> [!IMPORTANT]
> The cracking labs in this module use only bundled training hashes and dummy credentials. Do not replace the fixtures with real credentials, `/etc/shadow`, third-party password dumps, or hashes from systems you are not explicitly authorized to assess. The module does not include online password spraying, credential stuffing, or brute-force against login services.

## Files

```text
15-passwords-credential-security/
├── README.md
├── docx/
│   └── Red-Team-Module-15-Passwords-Credential-Security-Omarchy.docx
├── pdf/
│   └── Red-Team-Module-15-Passwords-Credential-Security-Omarchy.pdf
└── labs/
    ├── workspace-init.sh
    ├── pbkdf2-demo.py
    ├── policy-check.py
    ├── hash-identify.py
    ├── make-fixtures.py
    ├── john-lab.sh
    ├── hashcat-lab.sh
    ├── keyspace.py
    ├── credential-reuse.py
    ├── hash-benchmark.py
    ├── synthetic-auth.log
    ├── auth-log-analyze.py
    ├── evidence-manifest.sh
    ├── finding-note.py
    └── fixtures/
        ├── blocklist.txt
        ├── dummy-credentials.csv
        ├── hashcat-sha512crypt.txt
        ├── john-sha512crypt.txt
        ├── lab-wordlist.txt
        └── raw-sha256.txt
```

## Suggested setup

```bash
omarchy pkg add john hashcat
```

Hashcat also needs a supported compute backend. Check:

```bash
hashcat -I
```

If no usable backend is available, the learning objectives can still be completed with John and the bundled Python utilities. Do not install untrusted GPU/OpenCL packages just to make the lab work.

## Start

```bash
cd modules/15-passwords-credential-security/labs
./workspace-init.sh
python pbkdf2-demo.py
python policy-check.py 'this is a long passphrase 2026'
```

Offline training audit:

```bash
./john-lab.sh
```

Hashcat is optional when the local compute backend is available:

```bash
./hashcat-lab.sh
```

## Safety / sensitive-data hygiene

- Keep cracked output, potfiles, session files, client-derived wordlists, hashes, tokens, and private keys out of Git.
- Do not use the bundled wrapper pattern on real credential data without explicit authorization and a data-handling plan.
- Prefer minimum sufficient proof; do not include real plaintext credentials in reports when redacted evidence is enough.
- Destroy or return sensitive evidence according to the engagement Rules of Engagement and retention policy.

## Primary references

- NIST SP 800-63B-4 - https://pages.nist.gov/800-63-4/sp800-63b.html
- OWASP Password Storage Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- OWASP Authentication Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- OWASP Credential Stuffing Prevention Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html
- OWASP Multifactor Authentication Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html
- John the Ripper documentation - https://www.openwall.com/john/doc/
- Hashcat wiki - https://hashcat.net/wiki/?id=hashcat
