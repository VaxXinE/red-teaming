#!/usr/bin/env python3
"""Fetch a loopback HTTP URL and emit a small JSON summary."""
from __future__ import annotations

import argparse
import ipaddress
import json
import socket
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def validate_local_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme != "http" or not parsed.hostname:
        raise argparse.ArgumentTypeError("URL must use http:// and contain a host")
    try:
        resolved = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
    except OSError as exc:
        raise argparse.ArgumentTypeError("host cannot be resolved") from exc
    if not resolved.is_loopback:
        raise argparse.ArgumentTypeError("only loopback URLs are allowed")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=validate_local_url)
    args = parser.parse_args()

    req = Request(args.url, headers={"User-Agent": "module05-local-inspector/1.0"})
    with urlopen(req, timeout=3) as response:
        body = response.read(512)
        payload = {
            "url": args.url,
            "status": response.status,
            "content_type": response.headers.get("Content-Type"),
            "server": response.headers.get("Server"),
            "sample_bytes": len(body),
        }
    json.dump(payload, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
