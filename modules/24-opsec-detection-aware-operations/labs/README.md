# Module 24 Labs - OPSEC & Detection-Aware Operations

These labs are deliberately defensive/detection-aware. They do **not** disable security controls, tamper with logs, provide AV/EDR bypasses, persist on hosts, or target remote systems.

Recommended flow:

1. `./workspace-init.sh module24-opsec`
2. `python opsec-plan.py validate sample-opsec-plan.json`
3. `python benign-activity.py --workspace module24-opsec --marker RTLAB24_MARKER`
4. `python synthetic-events.py --output module24-opsec/telemetry/events.jsonl`
5. `python correlate-events.py module24-opsec/telemetry/events.jsonl`
6. `python sigma-structure.py sigma/training-process-marker.yml`
7. `python detection-evaluate.py sample-observations.json --output module24-opsec/results/evaluation.md`
8. `./cleanup-check.sh module24-opsec`
9. `./evidence-manifest.sh module24-opsec`

Windows helpers are read-only and only query existing logs.
