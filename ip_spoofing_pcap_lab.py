#!/usr/bin/env python3
"""Sahte kaynak alanlı örnek ICMP paketini yalnızca PCAP'a yazar."""
import argparse
from scapy.all import ICMP, IP, wrpcap

parser = argparse.ArgumentParser(description="Çevrimdışı IP spoofing paket laboratuvarı")
parser.add_argument("--output", default="ip_spoofing_demo.pcap")
args = parser.parse_args()
packet = IP(src="192.0.2.10", dst="198.51.100.20") / ICMP(type=8) / b"OFFLINE-LAB"
wrpcap(args.output, [packet])
print(f"[BİLGİ] PCAP yazıldı: {args.output}; ağa paket gönderilmedi.")
