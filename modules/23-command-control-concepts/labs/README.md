# Module 23 labs

All networked helpers are designed for localhost-only training. The training agent does not expose arbitrary shell execution.

## Quick start

```bash
./workspace-init.sh module23-c2
python c2-controller.py --workspace module23-c2
# second terminal
python c2-agent.py --workspace module23-c2 --agent-id lab-agent-01
# third terminal
python operator.py state
python operator.py system_info --agent lab-agent-01
```
