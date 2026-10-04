#!/usr/bin/env python3
"""Small localhost-only HTTP lab for Module 03.

No third-party dependencies. The server binds to 127.0.0.1 by default and is
intentionally simple so students can inspect HTTP semantics safely.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import argparse
import json

class LabHandler(BaseHTTPRequestHandler):
    server_version = "RedTeamHTTP03/1.0"

    def _send(self, status=200, body=b"", content_type="text/plain; charset=utf-8", extra_headers=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Lab-Module", "03")
        for key, value in (extra_headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            body = b"Module 03 HTTP lab\nTry /api/profile, /redirect, /set-cookie, /search?q=hello\n"
            return self._send(200, body)
        if parsed.path == "/api/profile":
            body = json.dumps({"user":"student","role":"learner","module":3}, indent=2).encode()
            return self._send(200, body, "application/json; charset=utf-8")
        if parsed.path == "/redirect":
            return self._send(302, b"redirecting\n", extra_headers={"Location":"/"})
        if parsed.path == "/set-cookie":
            return self._send(
                200,
                b"demo cookie set\n",
                extra_headers={"Set-Cookie":"lab_session=demo-only; Path=/; HttpOnly; SameSite=Lax"},
            )
        if parsed.path == "/search":
            q = parse_qs(parsed.query).get("q", [""])[0]
            body = json.dumps({"query":q,"note":"echo only; no vulnerability exercise in this module"}).encode()
            return self._send(200, body, "application/json; charset=utf-8")
        return self._send(404, b"not found\n")

    def do_HEAD(self):
        return self._send(200, b"")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b""
        if self.path == "/echo":
            body = json.dumps({
                "method": self.command,
                "content_type": self.headers.get("Content-Type"),
                "received": raw.decode("utf-8", errors="replace")
            }, indent=2).encode()
            return self._send(200, body, "application/json; charset=utf-8")
        return self._send(404, b"not found\n")

    def do_OPTIONS(self):
        return self._send(204, b"", extra_headers={"Allow":"GET, HEAD, POST, OPTIONS"})

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1", help="Keep 127.0.0.1 for a local-only lab")
    parser.add_argument("--port", type=int, default=8083)
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "::1", "localhost"}:
        raise SystemExit("Refusing non-loopback bind. Use 127.0.0.1 for this training lab.")
    server = ThreadingHTTPServer((args.host, args.port), LabHandler)
    print(f"HTTP lab listening on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
