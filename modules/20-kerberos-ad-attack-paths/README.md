# Module 20 — Kerberos & Active Directory Attack Paths

Module ini melanjutkan [Active Directory Fundamentals (18)](../18-active-directory-fundamentals/) dan [AD Enumeration (19)](../19-active-directory-enumeration/) dengan fokus pada **attack-path reasoning**: Kerberos ticket flow, SPN/service identities, delegation, ACL relationships, trusts, AD CS, BloodHound graph interpretation, controlled validation, telemetry, evidence, dan remediation.

> [!IMPORTANT]
> Authorized-lab rule. Semua hands-on memakai **synthetic dataset**, read-only inventory, GOAD/MINILAB yang terisolasi, atau platform training yang secara eksplisit mengizinkan teknik ofensif. Jangan mencoba ticket extraction, credential attack, delegation abuse, ACL modification, atau certificate abuse pada domain pihak lain.

| Field | Value |
|---|---|
| Prerequisite | [Module 18](../18-active-directory-fundamentals/), [Module 19](../19-active-directory-enumeration/) |
| Learning path | Kerberos flow → SPN/service identities → delegation → ACL relationships → trusts → AD CS → BloodHound path reasoning → controlled validation → detection-aware reporting |
| Safety model | Synthetic datasets, read-only PowerShell inventory, authorized isolated AD lab — **tidak ada** automation untuk ticket extraction, credential cracking, ACL/delegation modification, certificate impersonation, persistence, atau remote execution |
| Recommended lab | GOAD/MINILAB **hanya** dalam jaringan terisolasi — project GOAD sendiri memperingatkan environment-nya sangat vulnerable dan tidak boleh dipublish ke internet |

### Exit criteria

- [ ] Bisa menjelaskan TGT, service ticket, KDC, SPN, PAC, dan hubungan authentication vs authorization tanpa menghafal tool output.
- [ ] Bisa mengidentifikasi kandidat attack path dari service account, delegation, ACL, trust, dan certificate template secara read-only.
- [ ] Bisa membedakan relationship evidence dari exploitability — sebuah BloodHound edge bukan bukti path pasti dapat dieksekusi.
- [ ] Bisa membuat hipotesis, precondition, impact, telemetry, dan remediation sebelum melakukan controlled validation pada lab yang authorized.

---

## 1. Mental Model: Identity → Ticket → Relationship → Path

AD attack path bukan daftar command. Sebuah path adalah rangkaian hubungan yang, bila **semua precondition benar**, dapat mengubah kontrol dari principal awal menuju objective yang lebih sensitif. Setiap edge harus dijawab dengan lima pertanyaan: siapa principal-nya, object mana yang dikontrol, permission apa yang membuat hubungan itu relevan, precondition apa yang diperlukan, dan telemetry apa yang akan muncul.

| Layer | Pertanyaan utama | Contoh evidence |
|---|---|---|
| Identity | Siapa principal yang sedang kita punya? | SID, group membership, token |
| Authentication | Bagaimana principal membuktikan identitas? | TGT, service ticket, certificate |
| Authorization | Apa yang boleh dilakukan principal? | ACL, group, local admin, GPO |
| Relationship | Object mana yang dipengaruhi? | SPN owner, delegation target, trust |
| Path | Apakah beberapa relationship dapat dirangkai? | BloodHound/graph hypothesis |

### Lab 01 — Workspace & Scope

```bash
cd modules/20-kerberos-ad-attack-paths/labs
./workspace-init.sh module20-ad-paths
# isi 00-scope/README.txt dengan domain lab, permitted hosts, testing window, dan stop conditions
```

---

## 2. Kerberos: Ticket Flow yang Harus Benar-benar Dipahami

Dalam AD DS, KDC berjalan pada domain controller dan memakai database AD sebagai security account database. Client pertama-tama mendapatkan **Ticket Granting Ticket (TGT)**, lalu memakai TGT itu untuk meminta **service ticket** untuk SPN tertentu. Server memvalidasi service ticket dan bisa memakai authorization data di **PAC** untuk membuat access decision.

```text
User/Computer
   | AS-REQ / AS-REP
   v
KDC (DC) ----> TGT
   ^            |
   | TGS-REQ    | request service ticket for SPN
   +------------+
   | TGS-REP
   v
Service Ticket -> Target Service
```

> **Key distinction.** TGT membuktikan principal sudah diautentikasi ke KDC. Service ticket membuktikan permintaan akses ke service tertentu. **Keduanya tidak otomatis berarti caller punya authorization terhadap resource aplikasi** — itu keputusan terpisah di level aplikasi/PAC.

### Apa yang perlu dibaca dari sebuah ticket

| Field/concept | Kenapa penting |
|---|---|
| Client principal | identitas yang ticket-nya mewakili |
| Server principal/SPN | service mana yang jadi audience ticket |
| Validity window | membantu memahami lifetime, renewal, stale evidence |
| Encryption type | menunjukkan crypto yang benar-benar dinegosiasikan/dipakai |
| Ticket flags | forwardable/renewable/delegation semantics tertentu |
| PAC/authorization data | membawa authorization context yang dipakai Windows services |

### Kerberos troubleshooting sebelum membuat attack hypothesis

| Symptom | Kemungkinan penyebab | Check |
|---|---|---|
| Kerberos gagal dan NTLM muncul | SPN/DNS/service-name mismatch | DNS, SPN registration, target name |
| `KRB_AP_ERR_SKEW`/auth intermittent | clock skew | client/DC time + NTP hierarchy |
| `KDC_ERR_ETYPE_NOTSUPP` | encryption-type mismatch | account/domain crypto policy |
| Service ticket salah audience | duplicate/missing SPN | `setspn` query/read-only inventory |

### Lab 02 — Inspect Ticket Cache, Bukan Membuat Ticket Baru

```powershell
.\ticket-cache.ps1
klist
```

- Catat client principal, service name/SPN, encryption type, start/end time, dan ticket flags yang terlihat.
- **Jangan** purge ticket atau inject ticket pada module fundamental ini — objective-nya memahami state normal terlebih dahulu.

---

## 3. SPN dan Service Account Attack-Path Reasoning

SPN (Service Principal Name) adalah identifier unik service instance yang menghubungkan service dengan account yang menjalankannya. Dari perspektif assessment, SPN membantu memetakan service identities. **Risiko meningkat** ketika service identity memakai password lama, encryption legacy, privilege tinggi, atau lifecycle yang lemah.

```powershell
# Read-only live inventory (authorized domain)
Get-ADUser -LDAPFilter '(servicePrincipalName=*)' `
  -Properties servicePrincipalName,PasswordLastSet,msDS-SupportedEncryptionTypes,MemberOf |
  Select-Object SamAccountName,PasswordLastSet,msDS-SupportedEncryptionTypes,servicePrincipalName,MemberOf |
  Export-Csv -NoTypeInformation .\module20-ad-paths\02-spn\spns.csv
```

### Lab 03 — Synthetic SPN Risk Review

```bash
python spn-risk-review.py sample-spns.csv --output module20-ad-paths/02-spn/spn-review.json
```

Script ini scoring sederhana — `+2` kalau password age ≥365 hari, `+2` kalau encryption masih RC4, `+3` kalau akun privileged, `+1` kalau user-backed (bukan computer account `$`). Script hanya membuat **prioritization candidates**. Score tinggi **bukan bukti** account dapat dikompromikan.

> **Roastability concept.** Kerberoasting dan AS-REP roasting penting dipahami sebagai kondisi yang memungkinkan material autentikasi diverifikasi secara offline. Di module ini kita **tidak mengajarkan ticket extraction** terhadap domain nyata. Actual extraction/cracking hanya dilakukan di deliberately-vulnerable lab yang authorized dan memakai credential fixture/training.

| Signal | Kenapa relevan | Bukan berarti |
|---|---|---|
| User-backed SPN | service key terkait password user account | password pasti lemah |
| Password age tinggi | rotation mungkin lemah | hash pasti crackable |
| RC4/legacy crypto | legacy exposure/hardening gap | langsung exploitable |
| Privilege tinggi | impact lebih besar bila identity hilang | path sudah terbukti |

### Service-account lifecycle matters

Akun service tradisional sering punya password rotation lebih lambat karena takut merusak dependency. **gMSA** dirancang supaya password service bisa dikelola/dirotasi oleh domain dan dibatasi ke host yang berhak mengambil managed password.

| Account pattern | Review focus |
|---|---|
| Human-style service user | password lifecycle, interactive logon, group privilege, stale ownership |
| Computer account | host control, delegation, local-admin relationships |
| gMSA | host mana yang boleh retrieve managed password + privilege scope + SPNs |

> **AS-REP pre-auth concept.** Account yang dikonfigurasi tanpa Kerberos pre-authentication mengurangi bukti awal yang harus diberikan client sebelum KDC merespons. Treat flag ini sebagai hardening finding/candidate — jangan melakukan mass account probing di luar authorized lab.

---

## 4. Delegation: Unconstrained, Constrained, dan RBCD

Delegation memungkinkan service bertindak atas nama user ketika mengakses service lain. Security question-nya bukan hanya *"delegation enabled?"* tapi **"siapa boleh mendelegasikan ke mana, siapa mengontrol delegating principal, siapa mengontrol resource object, dan apakah impersonated identity menghasilkan privilege tambahan?"**

| Mode | Boundary | Assessment question |
|---|---|---|
| Unconstrained | broad delegation context | mengapa host/service ini perlu trust seluas itu? |
| Constrained (KCD) | dibatasi ke backend SPN tertentu | siapa mengontrol delegating account + allowed targets? |
| Resource-based constrained delegation | resource object menentukan delegator yang dipercaya | siapa punya write/control atas resource object? |

### S4U2Self & S4U2Proxy — conceptual map

```text
User identity
   |
   v
Front-end service -- S4U2Self --> service ticket to itself for user
   |
   +-- S4U2Proxy --> backend service ticket (when delegation policy permits)
              |
              v
            Back-end service
```

Kuncinya adalah **policy boundary**: account mana yang dipercaya, backend SPN mana yang diizinkan, apakah protocol transition relevan, dan siapa yang bisa mengubah delegation attributes/resource ACL. Jangan menyamakan kemampuan protocol dengan authorization aplikasi di backend.

### Lab 04 — Read-only Delegation Inventory

```powershell
.\delegation-inventory.ps1
```

### Lab 05 — Explain Relationship, Jangan Abuse

```bash
python delegation-path.py sample-delegation.json
```

`delegation-path.py` membaca mode (`unconstrained`/`constrained`/`rbcd*`) tiap principal dan mencetak review note-nya masing-masing (broad impersonation boundary / verifikasi backend SPN / inspeksi ACL resource object).

> **Security note.** Delegation path sering menjadi kombinasi beberapa control relationship. Jangan mengubah `msDS-AllowedToDelegateTo`, `PrincipalsAllowedToDelegateToAccount`, atau delegation flags hanya untuk "membuktikan" finding. Gunakan evidence + deliberately-vulnerable lab.

---

## 5. ACL Relationships: Control atas Object Lebih Penting dari Nama Group

AD object punya security descriptor dan DACL. Relationship seperti `GenericAll`, `GenericWrite`, `WriteDacl`, `WriteOwner`, `AddMember`, atau permission spesifik bisa mengubah siapa yang akhirnya mengontrol object. Red teamer harus membaca edge sebagai **capability**, bukan tombol exploit.

| Relationship | Capability concept | Validation question |
|---|---|---|
| `GenericAll` | kontrol luas atas object | apakah target object memang membawa path ke objective? |
| `GenericWrite` | dapat mengubah subset attribute | attribute mana yang writable dan security-sensitive? |
| `WriteDacl` | dapat mengubah DACL | apakah caller boleh memberi rights tambahan? |
| `WriteOwner` | dapat mengambil ownership | apakah ownership memberi jalan untuk ubah DACL? |
| `AddMember` | dapat menambah member ke group | seberapa sensitif effective privilege group itu? |

### Edge validation rubric

| Question | Evidence yang dicari |
|---|---|
| Does the edge exist now? | raw ACL/group/session/delegation data + timestamp |
| Can our principal exercise it? | effective group/token + deny/protection conditions |
| Does target lead somewhere useful? | next relationship/object privilege |
| Is it reversible? | original owner/DACL/member/config snapshot |
| What will defenders see? | directory change events, logon/ticket/process/network artifact |

### Lab 06 — Synthetic Attack Path Graph

```bash
python attack-path-model.py sample-acl.json --from-node STUDENT --to-node 'DOMAIN ADMINS'
```

`attack-path-model.py` melakukan BFS sederhana di graph JSON (`nodes`/`edges`) dan mencetak relationship chain dari `--from-node` ke `--to-node`. Expected output **hanya** menjelaskan relationship chain. Untuk setiap edge tulis: required privilege, object owner, expected change, rollback, dan telemetry. **Jangan mengubah ACL di production** untuk membuktikan graph.

---

## 6. BloodHound: Graph Evidence, Bukan Exploit Button

BloodHound sangat berguna untuk menghubungkan principals, groups, computers, sessions, ACLs, trusts, dan delegation menjadi graph. Tapi *shortest path* hanyalah **hypothesis generator**. Stale session, deny ACL, host offline, hardening, selective authentication, protected users, atau perubahan topology bisa memutus path yang terlihat valid.

### Lab 07 — Attack-Path Triage Worksheet

- Pilih satu path dari synthetic graph atau BloodHound CE di GOAD/MINILAB.
- Untuk setiap edge tulis: evidence source, required privilege, target object, expected impact, dan uncertainty.
- Beri label edge: `confirmed`, `likely`, `stale/unknown`, atau `not-applicable`.
- Jangan menjalankan abuse action sebelum semua precondition dan scope gate terpenuhi (lihat §9).

> **Think like an operator.** Path yang lebih pendek belum tentu lebih aman atau lebih reliable. Pilih path berdasarkan evidence quality, blast radius, detectability, reversibility, dan Rules of Engagement.

### Evidence-quality scoring untuk graph triage

| Level | Meaning |
|---|---|
| A — confirmed | raw current evidence + principal context + target state terverifikasi |
| B — strong | current relationship terverifikasi; satu operational precondition tersisa |
| C — candidate | collector/synthetic edge ada, tapi freshness/effective control belum diketahui |
| D — stale/invalid | relationship sudah tidak ada atau policy memblokir path |

---

## 7. Trusts dan Cross-Domain Attack Paths

AD trusts menentukan authentication path antar-domain/forest. Direction, transitivity, trust type, selective authentication, dan SID filtering memengaruhi apa yang mungkin dilakukan. **Forest adalah security boundary penting** — forest trust tidak otomatis membuat semua privilege menyeberang.

```text
One-way example:
ACCOUNT domain A ---> RESOURCE domain B
Authentication path allowed only if trust direction supports it,
then resource B still performs authorization.

Forest trust: transitive across the two participating forests,
but it does not implicitly create trust to a third forest.
```

### Lab 08 — Read-only Trust Inventory

```powershell
.\trust-inventory.ps1
```

### Lab 09 — Synthetic Trust Reasoning

```bash
python trust-path.py sample-trust.json
```

`trust-path.py` mencetak tiap trust sebagai `source -> target | direction | type | transitive=... | selectiveAuth=...`, dengan catatan tambahan kalau selective authentication aktif.

- Direction menjawab **arah authentication path**, bukan otomatis arah privilege escalation.
- Transitive trust memperluas namespace yang bisa di-resolve/authenticate, tapi resource authorization tetap harus lolos.
- Selective authentication dan SID filtering adalah control yang harus dicatat ketika menilai cross-domain hypothesis.

---

## 8. AD CS: Certificate Identity sebagai Attack-Path Surface

Active Directory Certificate Services (AD CS) menghubungkan PKI dengan AD. Enterprise CA memakai certificate template yang tersimpan di AD. Dari perspektif security assessment, fokus utamanya: siapa boleh enroll, subject/identity berasal dari mana, EKU apa yang diizinkan, apakah approval/signature diperlukan, dan apakah certificate bisa dipakai untuk authentication.

| Template property | Review question | Risk signal |
|---|---|---|
| Enrollment rights | siapa boleh enroll? | broad low-priv enrollment |
| Subject/SAN control | siapa menentukan identity pada certificate? | requester bisa memasukkan identity sensitif |
| EKU | certificate dipakai untuk apa? | client authentication/smartcard-like auth |
| Manager approval | ada human gate? | tidak ada approval pada template sensitif |
| Authorized signatures | butuh enrollment agent/signature? | tidak ada signature requirement |

```text
Certificate identity flow:
Requester -> Certificate Template policy -> Enterprise CA -> Certificate
   |         |               |      |
   |         + rights / name / EKU  + issuance + may later be used
   + authenticated identity                      for TLS or AD auth
```

Risk muncul dari **kombinasi controls**, bukan satu flag. Contoh: broad enrollment + requester-controlled subject/SAN + authentication-capable EKU + tanpa approval/signature gate adalah kombinasi yang harus diprioritaskan untuk review. Template ownership/DACL dan CA publication juga masuk attack-path reasoning.

### Lab 10 — Read-only AD CS Inventory

```powershell
.\adcs-inventory.ps1
# hasil: 06-adcs/cas.csv dan templates.csv
```

> **Important.** Risky template combination adalah **hypothesis**, bukan license untuk meminta certificate sebagai identity lain. Controlled issuance/abuse hanya di dedicated AD CS training lab yang memang menyediakan skenario tersebut.

---

## 9. Controlled Validation Gate

Sebelum mengubah object, meminta ticket khusus, melakukan certificate enrollment, atau mengeksekusi path, isi gate berikut. **Kalau satu jawaban belum jelas, kembali ke enumeration.**

| Gate | Pertanyaan |
|---|---|
| Authorization | Apakah teknik ini explicitly permitted oleh RoE? |
| Precondition | Apakah privilege/relationship sudah dikonfirmasi, bukan hanya diasumsikan? |
| Blast radius | Apakah perubahan bisa memengaruhi user/service lain? |
| Rollback | Bagaimana mengembalikan ACL, delegation, certificate, group, atau service state? |
| Evidence | Apa minimum proof yang cukup tanpa menambah impact? |
| Telemetry | Log/event/process/network artifact apa yang kemungkinan muncul? |

### Lab 11 — Finding Hypothesis Note

```bash
python finding-note.py module20-ad-paths/09-findings/path-01.md \
  --title "Delegation path hypothesis" \
  --evidence "Read-only inventory shows delegating principal and backend target." \
  --assumptions "Caller must control the delegating principal; backend authorization remains required." \
  --impact "Potential impersonation path if all preconditions hold." \
  --remediation "Remove unnecessary delegation and reduce control over service/resource objects."
```

---

## 10. Detection-Aware Kerberos & AD Paths

Red teamer yang bagus memahami jejak yang dibuat workflow-nya. Windows Security auditing bisa mencatat ticket activity pada DC dan perubahan directory pada object tertentu. AD CS juga punya audit event bila auditing diaktifkan.

| Event/source | Makna umum | Correlation idea |
|---|---|---|
| 4768 | TGT requested | principal, source, encryption type, result |
| 4769 | Kerberos service ticket requested | service/SPN, account, encryption type |
| 4771 | Kerberos pre-authentication failed | principal + source + failure pattern |
| 5136 | Directory object modified | ACL/delegation/template object changes |
| 4886/4887 | certificate request received/issued | requester, template, CA, subject |

Volume saja tidak cukup — banyak 4769 bisa normal pada service-heavy environment. Detection yang baik menggabungkan baseline, service name, account type, encryption, source host, privilege context, dan perubahan relationship yang terjadi sebelum/sesudah activity.

### Hardening/remediation map

| Area | Defensive direction |
|---|---|
| Service identities | managed rotation/gMSA bila sesuai, least privilege, disable interactive use kalau tidak perlu |
| Kerberos crypto | prefer supported modern encryption; retire legacy dependency secara sistematis |
| Delegation | remove unused delegation, constrain target, protect sensitive principal/resource |
| ACLs | remove unnecessary write/control edge; tier administrative principal |
| Trusts | gunakan selective authentication/SID filtering bila sesuai; minimalkan cross-boundary admin path |
| AD CS | least-privilege enrollment, secure subject rules/EKU, approval/signature untuk template sensitif, monitor CA |

---

## 11. Capstone — Build 3 Attack-Path Hypotheses

Gunakan GOAD/MINILAB yang terisolasi atau synthetic dataset module ini. **Objective capstone bukan mendapatkan Domain Admin**, tapi menghasilkan tiga path hypothesis yang bisa diaudit:

- **Path A** — service identity/SPN related.
- **Path B** — delegation atau ACL relationship.
- **Path C** — trust atau AD CS related.

Untuk setiap path, deliverable wajib:

- Start principal dan target objective.
- Relationship chain lengkap beserta evidence source.
- Required privileges/preconditions per edge.
- Apa yang bisa membuat path ini invalid.
- Minimum-impact validation plan + rollback.
- Likely telemetry dan detection opportunities.
- Remediation yang menghilangkan root cause — bukan hanya block tool.

### Lab 12 — Evidence Manifest & Closure

```bash
./evidence-manifest.sh module20-ad-paths
sha256sum -c module20-ad-paths/08-evidence/evidence-manifest.sha256
```

### Worked example — hypothesis, bukan exploit plan

| Step | Observation | Interpretation |
|---|---|---|
| 1 | `STUDENT` MemberOf `HELPDESK` | principal inherits helpdesk group rights |
| 2 | `HELPDESK` `GenericWrite` `SVC_APP` | verify which service-account attributes are actually writable |
| 3 | `SVC_APP` controls `APP01` service context | confirm host/service ownership and effective authorization |
| 4 | `APP01` has privileged reach to `FILE01` | network reachability + local/service authorization still required |

Kesimpulan yang benar: ada candidate relationship chain yang layak ditriage. **Kesimpulan yang belum boleh dibuat:** "STUDENT pasti bisa menjadi Domain Admin". Gap antar-edge harus divalidasi satu per satu, dan minimum-impact proof harus dipilih berdasarkan RoE.

---

## 12. Common Mistakes & Troubleshooting

| Symptom | Check first |
|---|---|
| `klist` hampir kosong | pastikan session domain-authenticated dan service domain memang sudah diakses |
| SPN inventory kosong | cek `ActiveDirectory` module, domain connectivity, dan search scope |
| BloodHound path tidak bisa direproduce | cek session freshness, host state, deny ACL, protected users, trust controls |
| AD CS inventory kosong | pastikan enterprise CA/template memang ada dan `configurationNamingContext` terbaca |

---

## 13. Knowledge Check

1. Apa perbedaan TGT dan service ticket dalam Kerberos?
2. Kenapa SPN adalah mapping identity/service, bukan vulnerability dengan sendirinya?
3. Apa perbedaan security boundary unconstrained, constrained, dan RBCD?
4. Kenapa `GenericWrite` harus dianalisis per attribute/object, bukan dianggap setara `GenericAll`?
5. Apa tiga alasan BloodHound shortest path bisa stale atau not-applicable?
6. Bagaimana direction dan selective authentication mengubah analisis trust?

### Self-review answer cues

- TGT dipakai untuk meminta service ticket; service ticket ditujukan ke SPN/service tertentu.
- SPN memetakan service instance ke sign-in account; risk baru muncul dari lifecycle, crypto, privilege, dan relationship lain.
- Delegation harus dibaca sebagai policy boundary: siapa boleh bertindak untuk siapa dan ke backend mana.
- `GenericWrite` tidak selalu memberi capability yang sama; attribute yang writable menentukan impact.
- BloodHound path bisa stale karena session, ACL, topology, host state, trust controls, atau protection mechanism berubah.
- Trust memperluas authentication path; authorization resource dan boundary controls tetap menentukan access akhir.

---

## 14. Attack-Path Worksheet Template

| Step | Principal | Relationship | Target | Evidence/uncertainty |
|---|---|---|---|---|
| 1 | ________ | ________ | ________ | ________ |
| 2 | ________ | ________ | ________ | ________ |
| 3 | ________ | ________ | ________ | ________ |
| 4 | ________ | ________ | ________ | ________ |

---

## 15. Completion Checklist

- [ ] 12 guided labs selesai dan evidence tersimpan di workspace dengan permission terbatas.
- [ ] Minimal tiga attack-path hypothesis mempunyai evidence, precondition, uncertainty, telemetry, rollback, dan remediation.
- [ ] Tidak ada domain production yang dimodifikasi untuk sekadar membuktikan graph relationship.
- [ ] Evidence manifest SHA-256 berhasil diverifikasi sebelum module ditutup.

---

## 16. Deliverables

```text
20-kerberos-ad-attack-paths/
├── README.md
├── docx/
├── pdf/
└── labs/
    ├── workspace-init.sh          — scaffold workspace (00-scope … 10-summary)
    ├── spn-risk-review.py         — scoring candidate SPN risk dari CSV
    ├── attack-path-model.py       — BFS synthetic graph JSON --from-node/--to-node
    ├── delegation-path.py         — penjelasan mode delegation dari JSON
    ├── trust-path.py              — ringkasan direction/transitivity trust dari JSON
    ├── finding-note.py            — generate hypothesis note (evidence/assumptions/impact/remediation)
    ├── evidence-manifest.sh       — SHA-256 manifest seluruh workspace
    ├── ticket-cache.ps1           — read-only klist/ticket inventory
    ├── delegation-inventory.ps1   — read-only delegation inventory
    ├── trust-inventory.ps1        — Get-ADTrust read-only
    ├── adcs-inventory.ps1         — enterprise CA + template inventory
    ├── sample-spns.csv, sample-acl.json, sample-delegation.json, sample-trust.json — synthetic fixtures
```

---

## 17. Compact Cheat Sheet

| Area | Read-only question/command |
|---|---|
| Ticket cache | `klist` |
| SPNs | `Get-ADUser -LDAPFilter '(servicePrincipalName=*)' ...` |
| Delegation | `TrustedForDelegation` / `msDS-AllowedToDelegateTo` / `PrincipalsAllowedToDelegateToAccount` |
| ACL | Who controls this object, attribute, DACL, or owner? |
| Trust | `Get-ADTrust -Filter *` |
| AD CS | Inventory enterprise CA + template + EKU/name/enrollment flags |
| Graph | Path = relationship hypothesis; validate every edge |
| Evidence | Timestamp + raw export + notes + SHA-256 + cleanup status |

---

## 18. References

- Microsoft Learn — Kerberos authentication overview
- Microsoft Learn — Service principal names
- Microsoft Learn — Kerberos constrained delegation overview
- Microsoft Learn — Active Directory trusts/key AD DS terms
- Microsoft Learn — Certificate template concepts
- Microsoft Learn — Events to monitor (4768/4769/4771)
- SpecterOps — BloodHound documentation
- Orange Cyberdefense — GOAD

> **Next module:** [21-pivoting-lateral-movement](../21-pivoting-lateral-movement/) — identity, authorization, network reachability, segmentation, dan session evidence untuk memahami bagaimana akses berpindah antar-host/subnet tanpa kehilangan scope discipline.
