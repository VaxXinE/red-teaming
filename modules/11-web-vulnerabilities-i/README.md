# Module 11 — Web Vulnerabilities I

Fondasi eksploitasi web untuk authorized training environment: SQL injection, reflected XSS, OS command injection, path traversal, file upload, authentication/session integrity, serta access control/IDOR.

## Safety

Semua payload dan script ditujukan hanya untuk:

- local Docker lab di `127.0.0.1:8111`, atau
- PortSwigger Web Security Academy labs yang memang sengaja vulnerable.

Jangan expose local vulnerable lab ke LAN/internet dan jangan gunakan teknik ini terhadap sistem pihak lain tanpa authorization tertulis.

## Struktur

```text
11-web-vulnerabilities-i/
├── README.md
├── docx/
│   └── Red-Team-Module-11-Web-Vulnerabilities-I-Omarchy.docx
├── pdf/
│   └── Red-Team-Module-11-Web-Vulnerabilities-I-Omarchy.pdf
└── labs/
    ├── workspace-init.sh
    ├── finding-note.py
    ├── vuln-web-lab.sh
    └── vuln-web-lab/
        ├── Dockerfile
        └── app.py
```

## Quick Start

```bash
cd labs
./workspace-init.sh
./vuln-web-lab.sh build
./vuln-web-lab.sh create
```

Buka `http://127.0.0.1:8111/` melalui Burp built-in browser.

Cleanup setelah latihan:

```bash
./vuln-web-lab.sh cleanup
```

## Lab Hardening

Launcher menjalankan intentionally vulnerable app dengan:

- bind hanya ke `127.0.0.1`,
- `--cap-drop ALL`,
- `no-new-privileges`,
- read-only root filesystem,
- tmpfs `noexec,nosuid` untuk `/tmp`,
- non-root container user,
- tanpa host volume mount.

Hardening ini mengurangi blast radius, tetapi **bukan** alasan untuk mengekspos app ke network lain.
