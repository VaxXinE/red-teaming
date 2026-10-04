# Module 16 - Linux Privilege Escalation

Omarchy / Arch Linux edition of the Red Team Learning Path.

## Learning goals

This module builds a repeatable Linux privilege-escalation methodology: manual enumeration first, hypothesis-driven validation, minimum sufficient proof, evidence, cleanup, remediation, and retest.

Core topics include:

- identity, users/groups, effective privilege and environment
- `sudo` policy analysis
- SUID/SGID and custom privileged helpers
- Linux file capabilities
- systemd services/timers and writable execution paths
- cron / scheduled jobs and process observation
- PATH/environment trust boundaries
- credential/configuration exposure
- Docker socket/group security on Omarchy
- kernel-exploit decision gates
- pspy and LinPEAS as post-manual-enumeration assistants
- Blue Team telemetry and remediation

## Safety boundary

All exploitation labs are designed for the bundled disposable Docker container. The launcher uses no host bind mounts, no Docker socket and `--network none`. It does not provide a root-shell shortcut. Do not practice privilege escalation on systems outside your own lab or an explicitly authorized engagement.

## Layout

This module intentionally uses a **denser A4 layout** than earlier modules: smaller margins, tighter paragraph spacing, compact tables/callouts, and fewer forced page breaks. The goal is to avoid half-empty pages while retaining readability.

## Lab quick start

```bash
cd modules/16-linux-privilege-escalation/labs
./workspace-init.sh
./linux-privesc-lab.sh build
./linux-privesc-lab.sh create
./linux-privesc-lab.sh shell
```

Reset before a new scenario:

```bash
./linux-privesc-lab.sh reset
```

Cleanup:

```bash
./linux-privesc-lab.sh cleanup
```

## Notes

- `no-new-privileges` is intentionally not set on the training container because the SUID/file-capability exercises require those kernel mechanisms to function. Isolation is provided through a disposable container, no network, no host mounts, no Docker socket, and resource limits.
- Keep Omarchy's default Docker posture where the normal user is not permanently in the `docker` group unless you explicitly accept root-equivalent access.
- LinPEAS/pspy are optional. Acquire them from official project releases and verify provenance before execution.
