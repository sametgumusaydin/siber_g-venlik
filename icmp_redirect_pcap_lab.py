#!/usr/bin/env python3
"""ICMP Redirect paket yapısını yalnızca PCAP'a yazar."""
import argparse
from scapy.all import ICMP, IP, UDP, wrpcap

parser = argparse.ArgumentParser(description="Çevrimdışı ICMP Redirect laboratuvarı")
parser.add_argument("--output", default="icmp_redirect_demo.pcap")
args = parser.parse_args()
inner = IP(src="192.0.2.50", dst="198.51.100.25") / UDP(sport=50000, dport=53)
packet = IP(src="192.0.2.1", dst="192.0.2.50") / ICMP(type=5, code=1, gw="192.0.2.254") / inner
wrpcap(args.output, [packet])
print(f"[BİLGİ] PCAP yazıldı: {args.output}; ağa paket gönderilmedi.")
