# Module 22 - Threat Intelligence & Adversary Emulation

**Red Team Learning Path - Omarchy / Arch Linux Edition**

Module ini mengubah cyber threat intelligence menjadi adversary-emulation exercise yang terstruktur: source validation, ATT&CK mapping, adversary profiling, Navigator layer, Attack Flow, expected telemetry, controlled execution, result scoring, improvement, dan retest.

> **Authorized lab only.** Semua behavior execution di module ini dibatasi pada host/VM/container milik sendiri atau environment yang secara eksplisit mengizinkan testing. Sample intelligence bersifat sintetis dan tidak mengatribusikan behavior kepada actor nyata.

## Materi utama

- Threat-Informed Defense dan perbedaan IOC, procedure, TTP, dan attack flow
- CTI lifecycle, source quality, provenance, dan analytical confidence
- MITRE ATT&CK v19.2: tactic, technique, sub-technique, procedure, Group/Campaign/Software, Detection Strategy
- Behavior-first ATT&CK mapping dan mapping QA
- Adversary profiling dan prioritization
- Full vs micro adversary emulation
- ATT&CK Navigator layer workflow
- Attack Flow dan sequence reasoning
- Expected telemetry & detection hypothesis
- Manual discovery emulation pada Omarchy dan Windows VM
- Atomic Red Team review/execution workflow untuk low-risk lab tests
- Result states: blocked / detected / logged-only / missed / not-testable
- Improve -> retest -> evidence integrity
- Reusable CTI, mapping, emulation, Blue Team, dan AAR worksheets

## Lab helpers

```text
labs/
├── workspace-init.sh
├── source-score.py
├── attack-catalog.json
├── sample-intel.json
├── ttp-map.py
├── navigator-layer.py
├── attack-flow.py
├── emulation-plan.py
├── telemetry-matrix.py
├── discovery-sim.sh
├── windows-discovery-sim.ps1
├── result-score.py
└── evidence-manifest.sh
```

Semua helper ofensif di package ini bersifat **discovery-only/read-only** dan sample intel bersifat sintetis.

## Quick start - Omarchy

```bash
omarchy pkg add python jq graphviz git

cd modules/22-threat-intelligence-adversary-emulation/labs
./workspace-init.sh module22-threat-emulation

python ttp-map.py \
  sample-intel.json \
  --output module22-threat-emulation/02-mappings/mappings.csv

python navigator-layer.py \
  module22-threat-emulation/02-mappings/mappings.csv \
  --output module22-threat-emulation/03-navigator/threat-layer.json

python attack-flow.py \
  module22-threat-emulation/02-mappings/mappings.csv \
  --dot module22-threat-emulation/04-flow/discovery.dot \
  --svg module22-threat-emulation/04-flow/discovery.svg
```

## Current ATT&CK note

Module ini ditulis terhadap terminologi **MITRE ATT&CK v19.2** (current pada Oktober 2026). ATT&CK v19 memecah tactic lama Defense Evasion menjadi **Stealth** dan **Defense Impairment**, jadi selalu perhatikan versi ketika membandingkan materi lama.

## Primary references

- MITRE ATT&CK: https://attack.mitre.org/
- ATT&CK Version History: https://attack.mitre.org/resources/versions/
- Adversary Emulation Plans: https://attack.mitre.org/resources/adversary-emulation-plans/
- ATT&CK Navigator: https://github.com/mitre-attack/attack-navigator
- CTID Adversary Emulation Library: https://ctid.mitre.org/resources/adversary-emulation-library/
- CTID Attack Flow: https://ctid.mitre.org/projects/attack-flow
- Atomic Red Team: https://www.atomicredteam.io/docs/atomic-red-team
