#!/usr/bin/env python3
"""Yetkili bir PCAP dosyasını çevrimdışı özetler."""
import argparse
from scapy.all import ARP, IP, TCP, UDP, rdpcap

def describe(packet):
    if ARP in packet:
        return f"ARP {packet[ARP].psrc} -> {packet[ARP].pdst} op={packet[ARP].op}"
    if IP in packet:
        proto = "IP"
        ports = ""
        if TCP in packet:
            proto, ports = "TCP", f" {packet[TCP].sport}->{packet[TCP].dport}"
        elif UDP in packet:
            proto, ports = "UDP", f" {packet[UDP].sport}->{packet[UDP].dport}"
        return f"{proto} {packet[IP].src} -> {packet[IP].dst}{ports}"
    return packet.summary()

parser = argparse.ArgumentParser(description="Çevrimdışı PCAP özetleyici")
parser.add_argument("--pcap", required=True)
parser.add_argument("--limit", type=int, default=25)
args = parser.parse_args()
if not 1 <= args.limit <= 500:
    raise SystemExit("limit 1-500 arasında olmalıdır")
for number, packet in enumerate(rdpcap(args.pcap)[:args.limit], 1):
    print(f"{number:04d} {describe(packet)}")
