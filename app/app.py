"""Servicio HTTP sin dependencias externas para el examen final de DGITI."""

import json
import os
import socket
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


def response_for(path: str, query: dict[str, list[str]]) -> tuple[int, dict]:
    """Devuelve el codigo HTTP y el cuerpo JSON de cada endpoint."""
    common = {
        "service": "dgiti-final",
        "student": "Erick Emanuel Tamayo Diaz",
        "instance": socket.gethostname(),
    }

    if path == "/health":
        return 200, {"status": "ok", **common}

    if path in ("/status", "/api/test"):
        return 200, {
            "status": "running",
            "database_architecture": "RDS PostgreSQL primary + read replica",
            **common,
        }

    if path == "/work":
        iterations = min(int(query.get("iterations", ["30000"])[0]), 200000)
        checksum = 0
        started = time.perf_counter()
        for value in range(iterations):
            checksum = (checksum + value * value) % 1_000_003
        return 200, {
            "status": "completed",
            "iterations": iterations,
            "checksum": checksum,
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
            **common,
        }

    return 404, {"status": "not_found", "path": path, **common}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - firma requerida por BaseHTTPRequestHandler
        parsed = urlparse(self.path)
        status, body = response_for(parsed.path, parse_qs(parsed.query))
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.client_address[0]} - {format % args}")


def run() -> None:
    port = int(os.getenv("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Servicio dgiti-final escuchando en el puerto {port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
