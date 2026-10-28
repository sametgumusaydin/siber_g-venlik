#!/usr/bin/env python3
"""Yalnızca loopback üzerinde sınırlı TCP connect kontrolü yapar."""
import argparse, socket, time

parser = argparse.ArgumentParser(description="Yerel port kontrolü")
parser.add_argument("--ports", default="22,80,443,8000")
parser.add_argument("--timeout", type=float, default=0.3)
args = parser.parse_args()
ports = [int(x) for x in args.ports.split(",") if x.strip()]
if not ports or len(ports) > 20 or any(not 1 <= p <= 65535 for p in ports):
    raise SystemExit("1-20 geçerli port belirtin")
for port in ports:
    start = time.perf_counter()
    with socket.socket() as sock:
        sock.settimeout(min(max(args.timeout, 0.05), 2.0))
        code = sock.connect_ex(("127.0.0.1", port))
    elapsed = (time.perf_counter() - start) * 1000
    print(f"127.0.0.1:{port:<5} {'AÇIK' if code == 0 else 'KAPALI'} {elapsed:.1f} ms")
