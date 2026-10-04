#!/usr/bin/env python3
"""Minimal RDAP client for learning.
Uses IANA's official DNS RDAP bootstrap, then queries the authoritative RDAP service.
This retrieves public registration data; it does not grant authorization to test the domain.
"""
from __future__ import annotations
import argparse, json, re, sys, urllib.parse, urllib.request
from pathlib import Path

BOOTSTRAP = "https://data.iana.org/rdap/dns.json"
DOMAIN_RE = re.compile(r"^(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$")
MAX_BYTES = 5 * 1024 * 1024
UA = "red-team-learning-module07/1.0"

def get_json(url: str, timeout: float = 10.0):
    if not url.startswith("https://"):
        raise ValueError("refusing non-HTTPS RDAP URL")
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rdap+json, application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("response exceeded 5 MiB safety limit")
        return json.loads(data.decode("utf-8"))

def find_service(bootstrap: dict, tld: str) -> str:
    for entry in bootstrap.get("services", []):
        if len(entry) != 2:
            continue
        suffixes, urls = entry
        if tld.lower() in {s.lower() for s in suffixes} and urls:
            base = urls[0]
            if not base.startswith("https://"):
                raise ValueError("bootstrap returned non-HTTPS service")
            return base if base.endswith("/") else base + "/"
    raise ValueError(f"no RDAP service found for .{tld}")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("domain", nargs="?", default="example.com")
    ap.add_argument("--output", type=Path)
    ap.add_argument("--timeout", type=float, default=10.0)
    args = ap.parse_args()
    domain = args.domain.rstrip(".").lower()
    if not DOMAIN_RE.fullmatch(domain):
        print("invalid domain", file=sys.stderr); return 2
    try:
        bootstrap = get_json(BOOTSTRAP, args.timeout)
        base = find_service(bootstrap, domain.rsplit(".", 1)[1])
        url = urllib.parse.urljoin(base, "domain/" + urllib.parse.quote(domain, safe=".-"))
        data = get_json(url, args.timeout)
    except Exception as exc:
        print(f"RDAP error: {exc}", file=sys.stderr); return 1
    rendered = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        try: args.output.chmod(0o600)
        except OSError: pass
        print(f"wrote {args.output}")
    else:
        print(rendered)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
