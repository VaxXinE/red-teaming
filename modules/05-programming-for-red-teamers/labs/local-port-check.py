#!/usr/bin/env python3
"""Check explicitly supplied TCP ports on loopback only.

This training utility refuses non-loopback targets by design.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import socket
import sys
from datetime import datetime, timezone


def parse_port(value: str) -> int:
    port = int(value)
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be 1..65535")
    return port


def ensure_loopback(host: str) -> str:
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(host))
    except OSError as exc:
        raise ValueError(f"cannot resolve host: {host}") from exc
    if not ip.is_loopback:
        raise ValueError("training utility only permits loopback targets")
    return str(ip)


def check(host: str, port: int, timeout: float) -> dict[str, object]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
    return {"host": host, "port": port, "open": result == 0}


def main() -> int:
    parser = argparse.ArgumentParser(description="Loopback-only TCP port checker")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", action="append", required=True, type=parse_port)
    parser.add_argument("--timeout", type=float, default=0.4)
    args = parser.parse_args()

    if not 0.05 <= args.timeout <= 5.0:
        parser.error("timeout must be between 0.05 and 5 seconds")

    try:
        host = ensure_loopback(args.host)
    except ValueError as exc:
        parser.error(str(exc))

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": host,
        "results": [check(host, port, args.timeout) for port in sorted(set(args.port))],
    }
    json.dump(payload, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
