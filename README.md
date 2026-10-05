# Red Team Learning Path — Omarchy

> A structured, lab-first red-team learning curriculum built around **Omarchy / Arch Linux**, progressing from foundational systems knowledge to an end-to-end red-team capstone.

![Curriculum](https://img.shields.io/badge/Curriculum-27%20Modules-7c3aed)
![Modules](https://img.shields.io/badge/Modules-00--26-2563eb)
![Platform](https://img.shields.io/badge/Primary%20Platform-Omarchy%20%2F%20Arch%20Linux-0f172a)
![Status](https://img.shields.io/badge/Status-Capstone%20Ready-16a34a)
![Use](https://img.shields.io/badge/Use-Authorized%20Labs%20Only-b91c1c)

## About This Repository

Repository ini adalah learning path pribadi untuk mempelajari **red teaming dan offensive security secara terstruktur**, mulai dari fondasi Linux, networking, HTTP, Windows, dan programming; dilanjutkan dengan reconnaissance, vulnerability assessment, web/API security, exploitation fundamentals, privilege escalation, Active Directory, lateral movement, threat intelligence, OPSEC, reporting, hingga **end-to-end red-team capstone**.

Materi dirancang dengan pendekatan **lab-first**, **evidence-driven**, dan **detection-aware**. Fokusnya bukan sekadar menjalankan tools, tetapi memahami *why*, *how*, dampak keamanan, batas scope, bukti yang perlu dikumpulkan, serta cara menyampaikan hasil secara profesional.

> [!IMPORTANT]
> Seluruh materi dan lab di repository ini ditujukan untuk **sistem milik sendiri, lab terisolasi, CTF, atau target yang memiliki izin eksplisit**. Jangan gunakan teknik di repository ini terhadap sistem pihak lain tanpa otorisasi tertulis.

---

## Curriculum Roadmap

### Phase 0 — Foundations

| Module | Topic | Focus |
|---|---|---|
| [00](modules/00-red-team-lab-ethics/) | Lab & Ethics | Lab safety, authorization, scope, ethics, evidence discipline |
| [01](modules/01-linux-fundamentals/) | Linux Fundamentals | Filesystem, permissions, processes, services, shell workflow |
| [02](modules/02-networking-fundamentals/) | Networking Fundamentals | TCP/IP, routing, DNS, ports, packet flow, troubleshooting |
| [03](modules/03-http-web-fundamentals/) | HTTP & Web Fundamentals | HTTP lifecycle, headers, cookies, sessions, browser/server behavior |
| [04](modules/04-windows-fundamentals/) | Windows Fundamentals | Windows architecture, users, services, permissions, PowerShell |
| [05](modules/05-programming-for-red-teamers/) | Programming for Red Teamers | Python/Bash automation, parsing, safe tooling, reusable scripts |
| [06](modules/06-pentest-methodology-scope-roe/) | Pentest Methodology, Scope & RoE | Engagement planning, Rules of Engagement, scope control, evidence |

### Phase 1 — Discovery & Assessment

| Module | Topic | Focus |
|---|---|---|
| [07](modules/07-reconnaissance-osint/) | Reconnaissance & OSINT | Passive discovery, asset mapping, source validation |
| [08](modules/08-network-scanning-enumeration/) | Network Scanning & Enumeration | Service discovery, enumeration workflow, result validation |
| [09](modules/09-vulnerability-assessment/) | Vulnerability Assessment | Findings validation, prioritization, false-positive reduction |
| [10](modules/10-burp-suite-fundamentals/) | Burp Suite Fundamentals | Proxy workflow, request inspection, repeater-driven testing |

### Phase 2 — Web & API Security

| Module | Topic | Focus |
|---|---|---|
| [11](modules/11-web-vulnerabilities-i/) | Web Vulnerabilities I | Common web weakness patterns and safe lab validation |
| [12](modules/12-web-vulnerabilities-ii/) | Web Vulnerabilities II | Deeper web attack-surface reasoning and chained findings |
| [13](modules/13-api-security/) | API Security | Authentication, authorization, object-level access, API abuse cases |

### Phase 3 — Exploitation & Credential Security

| Module | Topic | Focus |
|---|---|---|
| [14](modules/14-exploitation-fundamentals/) | Exploitation Fundamentals | Applicability checks, controlled PoCs, evidence, cleanup |
| [15](modules/15-passwords-credential-security/) | Passwords & Credential Security | Credential risk, password storage, controlled credential testing |
| [16](modules/16-linux-privilege-escalation/) | Linux Privilege Escalation | Misconfiguration analysis, privilege boundaries, remediation thinking |
| [17](modules/17-windows-privilege-escalation/) | Windows Privilege Escalation | Windows privilege boundaries, services, permissions, detection context |

### Phase 4 — Active Directory & Internal Networks

| Module | Topic | Focus |
|---|---|---|
| [18](modules/18-active-directory-fundamentals/) | Active Directory Fundamentals | Domain architecture, identities, groups, Kerberos, LDAP concepts |
| [19](modules/19-active-directory-enumeration/) | Active Directory Enumeration | Authorized directory discovery and attack-path mapping |
| [20](modules/20-kerberos-ad-attack-paths/) | Kerberos & AD Attack Paths | Kerberos security concepts, AD exposure paths, defensive visibility |
| [21](modules/21-pivoting-lateral-movement/) | Pivoting & Lateral Movement | Segmentation reasoning, controlled lab pivots, movement evidence |

### Phase 5 — Red-Team Operations

| Module | Topic | Focus |
|---|---|---|
| [22](modules/22-threat-intelligence-adversary-emulation/) | Threat Intelligence & Adversary Emulation | Intelligence-driven hypotheses and authorized emulation planning |
| [23](modules/23-command-control-concepts/) | Command & Control Concepts | C2 architecture concepts, telemetry, lab-safe communication models |
| [24](modules/24-opsec-detection-aware-operations/) | OPSEC & Detection-Aware Operations | Operational discipline, telemetry awareness, cleanup and validation |
| [25](modules/25-professional-reporting/) | Professional Reporting | Evidence indexing, severity, findings, executive/technical reporting |

### Phase 6 — Capstone

| Module | Topic | Focus |
|---|---|---|
| [26](modules/26-end-to-end-red-team-capstone/) | End-to-End Red Team Capstone | Scope → hypothesis → validation → attack-path reasoning → detection → evidence → cleanup → reporting |

---

## Repository Structure

Struktur tiap module dibuat konsisten agar materi mudah dipelajari dan di-maintain.

```text
red-teaming/
└── modules/
    ├── 00-red-team-lab-ethics/
    ├── 01-linux-fundamentals/
    ├── ...
    ├── 25-professional-reporting/
    └── 26-end-to-end-red-team-capstone/
        ├── README.md
        ├── docx/
        │   └── Red-Team-Module-26-....docx
        ├── pdf/
        │   └── Red-Team-Module-26-....pdf
        └── labs/
            └── ...
```

Tergantung modulnya, sebuah directory dapat berisi:

- **`README.md`** — overview module dan cara memakai materialnya.
- **`docx/`** — versi modul yang editable.
- **`pdf/`** — versi modul untuk dibaca/distribusikan.
- **`labs/`** — helper scripts, synthetic evidence, templates, atau isolated lab assets bila relevan.

---

## Recommended Environment

Learning path ini berpusat pada **Omarchy / Arch Linux** sebagai workstation utama. Beberapa module membutuhkan environment tambahan agar konsep dapat dipelajari secara realistis dan aman.

### Core workstation

```text
Omarchy / Arch Linux
├── Bash / Zsh
├── Python 3
├── Git
├── curl
├── jq
├── OpenSSH
└── container runtime (Docker/Podman, jika dibutuhkan module)
```

### Additional lab systems

Gunakan VM atau container terisolasi untuk environment yang berbeda dari host utama, misalnya:

- Windows workstation/server lab untuk Windows dan Active Directory modules.
- Browser + Burp Suite untuk web-security modules.
- Container networks atau private VM networks untuk networking/pivoting labs.
- Disposable snapshots agar setiap lab dapat dikembalikan ke kondisi awal.

> [!TIP]
> Untuk lab yang berpotensi mengubah konfigurasi sistem, gunakan **snapshot VM**, isolated network, dan disposable credentials. Hindari menggunakan credential pribadi atau production secrets.

---

## Getting Started

Clone repository:

```bash
git clone https://github.com/VaxXinE/red-teaming.git
cd red-teaming
```

Mulai dari Module 00 dan ikuti urutan module secara bertahap:

```bash
cd modules/00-red-team-lab-ethics
```

Baca `README.md` module terlebih dahulu, kemudian gunakan dokumen PDF/DOCX dan lab yang tersedia di module tersebut.

Untuk melihat seluruh module:

```bash
find modules -maxdepth 1 -mindepth 1 -type d | sort
```

---

## How to Study Each Module

Workflow yang direkomendasikan:

1. **Pelajari konsep** — pahami arsitektur dan security boundary sebelum menyentuh tools.
2. **Definisikan scope** — tentukan host, service, account, dan aktivitas yang memang diizinkan.
3. **Bangun isolated lab** — gunakan VM/container dan snapshot bila dibutuhkan.
4. **Jalankan observasi terkontrol** — fokus pada validasi hipotesis, bukan sekadar output tools.
5. **Catat evidence** — simpan command, timestamp, output relevan, dan konteks pengujian.
6. **Analisis detection & impact** — pahami apa yang terlihat dari sisi defender dan apa dampak sebenarnya.
7. **Cleanup** — hentikan service lab, hapus artefak sementara, dan verifikasi environment kembali bersih.
8. **Tulis finding/report** — dokumentasikan root cause, evidence, impact, dan remediation.

---

## Lab Safety Rules

Selalu perlakukan setiap aktivitas offensive-security seperti engagement profesional.

- Hanya uji aset yang **secara eksplisit berada di dalam scope**.
- Gunakan **lab, CTF, VM, container, atau sistem milik sendiri**.
- Jangan melakukan scanning atau testing terhadap public IP/domain yang tidak memberikan izin.
- Jangan menyimpan password, token, API key, private key, atau credential asli di repository.
- Gunakan synthetic/test credentials untuk lab.
- Simpan evidence secukupnya dan hindari mengumpulkan data sensitif yang tidak diperlukan.
- Catat aktivitas penting sehingga pengujian dapat diaudit dan direproduksi.
- Lakukan cleanup setelah lab selesai.
- Jika sebuah teknik memiliki potensi mengganggu availability, lakukan hanya pada disposable environment.

---

## Security Mindset

Repository ini menggunakan pendekatan **secure-by-design dan detection-aware**. Tujuan akhir setiap exercise bukan hanya mengetahui bahwa sebuah weakness dapat terjadi, tetapi mampu menjawab:

```text
What is exposed?
       ↓
Why is it exposed?
       ↓
What security boundary failed?
       ↓
What is the realistic impact?
       ↓
What evidence proves it?
       ↓
What telemetry should detect it?
       ↓
How should it be fixed?
       ↓
How do we verify the remediation?
```

Dengan pola tersebut, offensive testing menjadi sarana untuk meningkatkan defensive engineering, bukan sekadar menjalankan exploit atau tools.

---

## Capstone

Module 26 menyatukan seluruh learning path menjadi sebuah **end-to-end red-team engagement simulation** di environment lab.

Capstone berfokus pada lifecycle:

```text
Authorization & Scope
        ↓
Threat / Attack Hypothesis
        ↓
Discovery & Validation
        ↓
Attack-Path Reasoning
        ↓
Controlled Lab Testing
        ↓
Detection & Telemetry Review
        ↓
Evidence Collection
        ↓
Cleanup Verification
        ↓
Professional Reporting
```

Lihat: [`modules/26-end-to-end-red-team-capstone/`](modules/26-end-to-end-red-team-capstone/)

---

## Current Curriculum Status

Saat ini repository mencakup **27 module**, dari **Module 00 sampai Module 26**, dan sudah mencapai tahap **end-to-end capstone**.

```text
Foundations                     ✅
Discovery & Assessment          ✅
Web & API Security              ✅
Exploitation Fundamentals       ✅
Privilege Escalation            ✅
Active Directory                ✅
Internal Movement Concepts      ✅
Threat-Informed Operations      ✅
Detection-Aware Operations      ✅
Professional Reporting          ✅
End-to-End Capstone             ✅
```

Learning path dapat terus dikembangkan dengan advanced labs, blue-team validation, purple-team exercises, cloud security, container/Kubernetes security, malware-analysis fundamentals, atau specialized adversary-emulation scenarios.

---

## Disclaimer

This repository is provided **for educational, defensive-security, authorized penetration-testing, and controlled laboratory purposes only**.

You are responsible for ensuring that every system, network, application, identity, or environment you test is owned by you or covered by explicit authorization. The repository is not intended to encourage unauthorized access, disruption, credential theft, persistence, or misuse of third-party systems.

---

## Author

Maintained by **VaxXinE**.

GitHub repository: **VaxXinE/red-teaming**

---

> Learn the system. Understand the boundary. Validate the risk. Preserve the evidence. Improve the defense.
