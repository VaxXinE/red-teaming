# Module 26 Labs

The core capstone is a deliberately vulnerable, local-only Docker micro-enterprise. Run it only on a machine you control. No service is published to the host; assessment happens from the `capstone26-attacker` container.

## Quick start

```bash
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

Training credentials in Docker images are dummy values only.
