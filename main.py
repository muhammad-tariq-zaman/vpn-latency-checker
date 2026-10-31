"""Measure TCP connect latency to a host:port, repeated, with a verdict.

Usage: python3 main.py example.com 443 --count 5
Verdict bands: avg <50ms good, <150ms fair, otherwise poor.
"""
import argparse
import socket
import sys
import time


def measure(host, port, count=5, timeout=3.0):
    samples = []
    for _ in range(count):
        start = time.monotonic()
        try:
            with socket.create_connection((host, port), timeout=timeout):
                samples.append((time.monotonic() - start) * 1000)
        except OSError:
            samples.append(None)
    return samples


def verdict(samples):
    ok = [s for s in samples if s is not None]
    if not ok:
        return "unreachable", None
    avg = sum(ok) / len(ok)
    if avg < 50:
        return "good", avg
    if avg < 150:
        return "fair", avg
    return "poor", avg


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host")
    parser.add_argument("port", type=int)
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args(argv)
    samples = measure(args.host, args.port, args.count)
    label, avg = verdict(samples)
    failed = sum(1 for s in samples if s is None)
    if avg is None:
        print(f"{args.host}:{args.port}: unreachable ({failed}/{len(samples)} failed)")
    else:
        print(f"{args.host}:{args.port}: {label} (avg {avg:.1f}ms, {failed} failed of {len(samples)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
