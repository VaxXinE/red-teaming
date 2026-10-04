# Module 10 - Burp Suite Fundamentals

Manual web-testing workflow for Burp Suite on Omarchy / Arch Linux.

## Safety boundary

All included labs are intended for loopback services (`127.0.0.1`) and deliberately vulnerable training applications you own/control. Do not add third-party systems to Burp scope without explicit authorization.

## Files

- `docx/` editable source
- `pdf/` final learning module
- `labs/workspace-init.sh` private workspace helper
- `labs/scope-guard.py` loopback URL guardrail
- `labs/burp-lab-server.py` local HTTP training server
- `labs/juice-shop-lab.sh` optional Juice Shop lifecycle wrapper
- `labs/observation-log.py` structured observation log

## Quick start

```bash
./labs/workspace-init.sh module10-burp
python labs/burp-lab-server.py --port 8090
```

Then use Burp's built-in browser against `http://127.0.0.1:8090/`.
