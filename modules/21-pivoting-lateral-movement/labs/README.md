# Module 21 Labs

All exercises are intentionally scoped to the Docker lab created by `pivot-lab.sh`.

Training credentials (dummy, disposable):
- jump: `pivot` / `Pivot21!`
- internal SSH target: `student` / `Student21!`

Do not reuse these passwords anywhere else.

Core flow:
1. `./pivot-lab.sh build`
2. `./pivot-lab.sh create`
3. `./segmentation-check.sh`
4. `./pivot-lab.sh shell`
5. Run the SSH forwarding exercises from inside the attacker container.
6. `./pivot-lab.sh cleanup`
