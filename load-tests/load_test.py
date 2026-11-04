"""Prueba de carga basica, reproducible y sin dependencias externas."""

import argparse
import concurrent.futures
import json
import statistics
import time
import urllib.error
import urllib.request


def request_once(url: str) -> tuple[bool, float, str]:
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            body = json.loads(response.read().decode("utf-8"))
            return response.status == 200, (time.perf_counter() - started) * 1000, body.get("instance", "unknown")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return False, (time.perf_counter() - started) * 1000, "error"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Ejemplo: http://ALB_DNS/work?iterations=100000")
    parser.add_argument("--requests", type=int, default=200)
    parser.add_argument("--concurrency", type=int, default=20)
    args = parser.parse_args()

    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        results = list(pool.map(lambda _: request_once(args.url), range(args.requests)))
    elapsed = time.perf_counter() - started

    latencies = [latency for _, latency, _ in results]
    successes = sum(1 for ok, _, _ in results if ok)
    instances = sorted({instance for ok, _, instance in results if ok})
    percentile_index = max(0, int(len(latencies) * 0.95) - 1)

    print("=== RESULTADO PRUEBA DE CARGA ===")
    print(f"URL: {args.url}")
    print(f"Solicitudes: {args.requests}")
    print(f"Usuarios concurrentes: {args.concurrency}")
    print(f"Exitosas: {successes}")
    print(f"Errores: {args.requests - successes} ({(args.requests - successes) / args.requests * 100:.2f}%)")
    print(f"Tiempo total: {elapsed:.2f} s")
    print(f"Rendimiento: {args.requests / elapsed:.2f} solicitudes/s")
    print(f"Latencia promedio: {statistics.mean(latencies):.2f} ms")
    print(f"Latencia p95: {sorted(latencies)[percentile_index]:.2f} ms")
    print(f"Instancias atendiendo: {', '.join(instances)}")


if __name__ == "__main__":
    main()
