#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinirli SYN paketi laboratuvar gosterimi.

Varsayilan davranis paketleri aga gondermez; PCAP dosyasina yazar.
Canli gonderim yalnizca ozel/yerel IP adreslerine, acik onayla ve
sinirli paket sayisiyla yapilabilir.
"""

import argparse
import ipaddress
import random
import sys
import time

MAX_PACKETS = 200
MIN_DELAY = 0.05
CONFIRMATION = "IZINLI-LAB"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Egitim amacli, hiz ve adet sinirli SYN paketi gosterimi."
    )
    parser.add_argument("target", help="Izinli laboratuvar hedefinin IPv4 adresi")
    parser.add_argument("-p", "--port", type=int, default=80,
                        help="Hedef TCP portu (varsayilan: 80)")
    parser.add_argument("-c", "--count", type=int, default=20,
                        help="Paket sayisi; en fazla 200 (varsayilan: 20)")
    parser.add_argument("--delay", type=float, default=0.20,
                        help="Paketler arasi bekleme; en az 0.05 saniye")
    parser.add_argument("--pcap", default="syn_lab_demo.pcap",
                        help="Olusturulacak PCAP dosyasi")
    parser.add_argument("--send", action="store_true",
                        help="PCAP yazmaya ek olarak paketleri canli gonder")
    parser.add_argument("--confirm", default="",
                        help=f"Canli gonderim onayi: {CONFIRMATION}")
    return parser.parse_args()


def validate(args):
    try:
        target = ipaddress.ip_address(args.target)
    except ValueError as error:
        raise SystemExit(f"[HATA] Gecersiz IPv4 adresi: {error}")

    if target.version != 4:
        raise SystemExit("[HATA] Bu uygulama yalnizca IPv4 icindir.")
    if not 1 <= args.port <= 65535:
        raise SystemExit("[HATA] Port 1-65535 araliginda olmalidir.")
    if not 1 <= args.count <= MAX_PACKETS:
        raise SystemExit(f"[HATA] Paket sayisi 1-{MAX_PACKETS} araliginda olmalidir.")
    if args.delay < MIN_DELAY:
        raise SystemExit(f"[HATA] Gecikme en az {MIN_DELAY} saniye olmalidir.")

    if args.send:
        allowed = target.is_private or target.is_loopback or target.is_link_local
        if not allowed:
            raise SystemExit("[HATA] Canli gonderim sadece ozel/yerel lab IP'lerine izinlidir.")
        if args.confirm != CONFIRMATION:
            raise SystemExit(
                f"[HATA] Canli gonderim icin --confirm {CONFIRMATION} gereklidir."
            )

    return str(target)


def build_packets(target, port, count):
    packets = []
    for sequence in range(count):
        source_port = random.randint(49152, 65535)
        initial_sequence = random.randint(0, 2**32 - 1)
        packet = IP(dst=target, id=(sequence + 1) % 65536) / TCP(
            sport=source_port,
            dport=port,
            flags="S",
            seq=initial_sequence,
        )
        packets.append(packet)
    return packets


def main():
    args = parse_args()

    global IP, TCP, send, wrpcap
    try:
        from scapy.all import IP, TCP, send, wrpcap
    except ModuleNotFoundError:
        print(
            "[HATA] Scapy bulunamadi. Kurulum: python -m pip install scapy",
            file=sys.stderr,
        )
        sys.exit(1)

    target = validate(args)
    packets = build_packets(target, args.port, args.count)

    wrpcap(args.pcap, packets)
    print(f"[BILGI] {len(packets)} SYN paketi PCAP dosyasina yazildi: {args.pcap}")

    if not args.send:
        print("[BILGI] Aga paket gonderilmedi. Wireshark ile PCAP dosyasini acabilirsiniz.")
        return

    print(f"[BILGI] Izinli lab hedefi: {target}:{args.port}")
    for number, packet in enumerate(packets, start=1):
        send(packet, verbose=False)
        print(f"[GONDERILDI] {number}/{len(packets)}")
        time.sleep(args.delay)

    print("[BILGI] Sinirli laboratuvar gosterimi tamamlandi.")


if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        print("[HATA] Canli paket gonderimi icin yetki gerekiyor.", file=sys.stderr)
        sys.exit(1)
