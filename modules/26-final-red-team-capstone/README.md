# Module 26 - Final Red Team Capstone

Final integrative module for the Red Team Learning Path (Omarchy / Arch Linux edition).

This module combines the complete workflow from Modules 00-25 into a controlled, local-only simulated engagement:

- scope / Rules of Engagement / stop conditions
- reconnaissance and enumeration
- web vulnerability validation
- initial access with dummy lab credentials
- constrained Linux privilege-boundary proof
- network pivoting and lateral movement
- internal API access
- objective handling
- detection-aware review
- evidence integrity and cleanup
- professional reporting
- optional Active Directory extension using a separately isolated authorized lab such as GOAD/MINILAB

## Safety

The packaged Docker lab is deliberately vulnerable. It is intended only for a machine you control. Services are not published to the host; assessment is performed from the dedicated `capstone26-attacker` container. Do not reuse the training passwords or tokens anywhere else.

## Quick Start

```bash
cd labs
./workspace-init.sh capstone26
python validate-scope.py scope.json
./capstone-lab.sh build
./capstone-lab.sh create
./capstone-lab.sh status
./segmentation-check.sh
./capstone-lab.sh shell
```

When finished:

```bash
./capstone-lab.sh cleanup
./cleanup-check.sh
```

## Files

```text
26-final-red-team-capstone/
├── README.md
├── docx/
├── pdf/
└── labs/
    ├── README.md
    ├── workspace-init.sh
    ├── scope.json
    ├── validate-scope.py
    ├── activity-log.py
    ├── hypothesis-note.py
    ├── evidence-manifest.sh
    ├── cleanup-check.sh
    ├── segmentation-check.sh
    ├── capstone-lab.sh
    ├── report-template.md
    └── capstone-lab/
        ├── compose.yml
        ├── attacker/
        ├── edge-web/
        ├── jump-host/
        ├── internal-api/
        └── internal-ssh/
```

The no-walkthrough capstone should be attempted without reading the application/container source code after completing the guided run once.
