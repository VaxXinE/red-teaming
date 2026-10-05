# Module 24 - OPSEC & Detection-Aware Operations

Module ini membahas operational security dari sudut engagement yang authorized: mengendalikan risiko, memprediksi footprint, memahami telemetry, menguji detection secara aman, melakukan cleanup, dan membuktikan hasil dengan evidence yang dapat diaudit.

## Learning objectives

- Membuat OPSEC plan dengan exposure budget, stop conditions, prohibited actions, dan cleanup owner.
- Memprediksi process/network/file/DNS/auth footprint sebelum menjalankan test.
- Memahami perubahan defensive model MITRE ATT&CK v18/v19: Detection Strategies/Analytics dan deprecation Data Sources.
- Membaca telemetry dasar Windows (Sysmon/4688) dan Linux (journal/process/socket/audit bila tersedia).
- Memahami Sigma fundamentals dan correlation tanpa bergantung pada satu SIEM vendor.
- Membedakan `blocked`, `detected`, `logged-only`, `missed`, dan `not-testable`.
- Melakukan review-first Atomic Red Team workflow pada disposable test machine.
- Melakukan cleanup + residual verification + evidence hashing.

## Safety boundary

Module ini **tidak** mengajarkan mematikan security controls, menghapus/tamper log, AMSI/ETW bypass, EDR bypass, unhooking, obfuscation untuk evasion, process injection, timestomping, persistence tersembunyi, atau teknik lain untuk menghindari pertahanan. Hands-on berfokus pada localhost, synthetic telemetry, read-only log review, dan low-risk authorized simulations.

## Files

```text
24-opsec-detection-aware-operations/
├── README.md
├── docx/
│   └── Red-Team-Module-24-OPSEC-Detection-Aware-Operations-Omarchy.docx
├── pdf/
│   └── Red-Team-Module-24-OPSEC-Detection-Aware-Operations-Omarchy.pdf
└── labs/
    ├── README.md
    ├── workspace-init.sh
    ├── sample-opsec-plan.json
    ├── opsec-plan.py
    ├── benign-activity.py
    ├── synthetic-events.py
    ├── correlate-events.py
    ├── linux-telemetry.sh
    ├── windows-telemetry.ps1
    ├── sigma-structure.py
    ├── sample-observations.json
    ├── detection-evaluate.py
    ├── cleanup-check.sh
    ├── evidence-manifest.sh
    └── sigma/
        └── training-process-marker.yml
```

## Quick start

```bash
cd labs
./workspace-init.sh module24-opsec
python opsec-plan.py validate sample-opsec-plan.json
python benign-activity.py --workspace module24-opsec --marker RTLAB24_MARKER
python synthetic-events.py --output module24-opsec/telemetry/events.jsonl
python correlate-events.py module24-opsec/telemetry/events.jsonl
python sigma-structure.py sigma/training-process-marker.yml
python detection-evaluate.py sample-observations.json --output module24-opsec/results/evaluation.md
./cleanup-check.sh module24-opsec
./evidence-manifest.sh module24-opsec
```

Referensi utama ada di PDF/DOCX module dan mencakup MITRE ATT&CK v19.2 Detection Strategies, Microsoft Sysmon/4688, systemd journalctl, Linux auditd, Sigma Specification 2.1.0, dan Atomic Red Team.
