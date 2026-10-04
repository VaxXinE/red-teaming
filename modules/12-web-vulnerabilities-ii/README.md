# Module 12 - Web Vulnerabilities II

Advanced web security module for the Omarchy / Arch Linux Red Team Learning Path.

## Scope

This module covers advanced trust-boundary and interpretation-gap vulnerabilities:

- SSRF
- XXE
- SSTI
- Insecure deserialization
- CORS / CSRF
- JWT
- OAuth / OpenID Connect
- GraphQL
- NoSQL injection
- HTTP Host header attacks
- HTTP request smuggling / desync
- Web cache poisoning
- Race conditions
- Prototype pollution
- Business logic flaws

All technical exercises are restricted to the local Module 12 Docker lab or deliberately vulnerable PortSwigger Web Security Academy labs.

## Files

- `pdf/` - final learning PDF
- `docx/` - editable source
- `labs/` - local authorized training utilities and Docker lab

## Local lab

```bash
cd labs
./workspace-init.sh
./advanced-web-lab.sh build
./advanced-web-lab.sh create
```

Lab entry point: `http://127.0.0.1:8120/`

Cleanup:

```bash
./advanced-web-lab.sh cleanup
```

The vulnerable application is published to loopback only. Do not change it to `0.0.0.0`, expose it to a LAN/public network, or mount sensitive host directories into the container.
