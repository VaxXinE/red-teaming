# Module 03 - HTTP & Web Fundamentals for Red Teamers

Modul ini membangun fondasi HTTP/web sebelum masuk ke vulnerability classes seperti SQL injection, XSS, access control/IDOR, SSRF, authentication flaws, dan API security.

## Isi

- HTTP request/response mental model
- URL, methods, status codes, headers, content types
- Forms, JSON, encoding
- Cookies, sessions, authentication, authorization
- Redirects, caching, Same-Origin Policy, CORS basics
- TLS/HTTPS fundamentals
- `curl`, `jq`, Browser DevTools
- Burp Suite Community: Proxy HTTP history & Repeater
- OWASP Juice Shop lokal
- 10 hands-on labs + practical challenge

## Safety boundary

Semua lab utama menggunakan `127.0.0.1` atau container lokal. Jangan mengarahkan command, proxy, scanner, atau modifikasi request ke sistem pihak lain tanpa authorization eksplisit.

## Struktur

```text
03-http-web-fundamentals/
├── README.md
├── docx/
│   └── Red-Team-Module-03-HTTP-Web-Fundamentals-Omarchy.docx
├── pdf/
│   └── Red-Team-Module-03-HTTP-Web-Fundamentals-Omarchy.pdf
└── labs/
    ├── http-lab-server.py
    ├── http-baseline.sh
    └── juice-shop-lab.sh
```

## Quick start local HTTP lab

```bash
cd labs
./http-lab-server.py
```

Di terminal lain:

```bash
curl -i http://127.0.0.1:8083/
curl -sS http://127.0.0.1:8083/api/profile | jq .
```

## Juice Shop local

```bash
./juice-shop-lab.sh create
./juice-shop-lab.sh status
```

Buka `http://127.0.0.1:3000`. Setelah selesai:

```bash
./juice-shop-lab.sh cleanup
```

## Baseline evidence helper

```bash
./http-baseline.sh
```

Script menolak target non-local secara default dan menyimpan headers/body dengan permission ketat (`umask 077`).
