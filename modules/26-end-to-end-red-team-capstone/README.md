# Module 26 - End-to-End Red Team Capstone

Final capstone untuk Red Team Learning Path berbasis Omarchy / Arch Linux. Module ini menggabungkan planning, scope/RoE, attack-path reasoning, evidence, detection-aware validation, cleanup, finding quality, reporting, dan operator debrief menjadi satu workflow engagement yang repeatable.

## Contents

- `docx/` - editable source document
- `pdf/` - final learning module
- `labs/` - offline-first capstone utilities + synthetic Northstar Labs dataset

## Safety

Default lab path sepenuhnya offline. Script yang disertakan tidak melakukan scanning, exploitation, credential attack, persistence, tunneling, atau lateral movement. Optional live-lab lane hanya untuk environment milik sendiri atau platform yang memberikan authorization eksplisit.

`scope-guard.py` menolak public IP dan hostname di luar suffix `.test`, `.lab`, atau `.local` sebagai guardrail tambahan. Ia bukan pengganti authorization atau Rules of Engagement.

## Lab utilities

- `workspace-init.sh` - private capstone workspace
- `scope-guard.py` - private/test-only target validation
- `scenario.json` - synthetic Northstar Labs engagement definition
- `sample-evidence/` - synthetic web, AD, service, and detection evidence
- `objective-tracker.py` - objective status tracking
- `timeline.py` - sanitized UTC event timeline
- `finding-stub.py` - professional finding skeleton
- `attack-path-map.py` - render synthetic JSON path into Mermaid/Markdown
- `evidence-manifest.sh` - SHA-256 evidence manifest
- `engagement-qa.py` - final structure / placeholder / basic secret-pattern QA
- `report-template.md` - final report skeleton

## Capstone pass target

Recommended score: 80/100 with mandatory pass on Scope & Safety. High technical score never compensates for an out-of-scope action.
