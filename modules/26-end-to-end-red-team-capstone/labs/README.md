# Module 26 Labs - End-to-End Red Team Capstone

Default path is fully offline and uses synthetic evidence. None of the included scripts perform scanning, exploitation, credential attacks, persistence, tunneling, or lateral movement.

Recommended order:
1. `./workspace-init.sh module26-capstone`
2. `python scope-guard.py scenario.json`
3. Copy `sample-evidence/` into `module26-capstone/01-raw/`
4. Initialize `objective-tracker.py`
5. Add timeline events with `timeline.py`
6. Create findings with `finding-stub.py`
7. Render `attack-path.json` using `attack-path-map.py`
8. Generate `evidence-manifest.sh`
9. Run `engagement-qa.py`

For live labs, use only systems you own or platforms that explicitly authorize testing. The scope guard is an extra safety check, not a substitute for authorization.
