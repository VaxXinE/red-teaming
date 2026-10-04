#!/usr/bin/env python3
"""Safe subprocess example for Module 05.

Runs only a fixed allowlist of read-only local commands.
"""
from __future__ import annotations

import argparse
import subprocess
import sys

COMMANDS: dict[str, list[str]] = {
    "identity": ["id"],
    "kernel": ["uname", "-a"],
    "routes": ["ip", "route", "show"],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=sorted(COMMANDS))
    args = parser.parse_args()

    completed = subprocess.run(
        COMMANDS[args.command],
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if completed.returncode != 0:
        print(completed.stderr.strip(), file=sys.stderr)
        return completed.returncode or 1
    print(completed.stdout, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
