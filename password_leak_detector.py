#!/usr/bin/env python3
"""Yetkili PCAP'ta olası açık metin sır alanlarını maskeli raporlar."""
import argparse, re
from scapy.all import Raw, IP, TCP, rdpcap

PATTERN = re.compile(rb"(?i)\b(user(?:name)?|login|pass(?:word)?|token|session(?:_?key)?)\s*[:=]\s*([^&\s]{1,80})")
parser = argparse.ArgumentParser(description="Parola sızıntısı göstergesi denetimi")
parser.add_argument("--pcap", required=True)
args = parser.parse_args()
hits = 0
for number, packet in enumerate(rdpcap(args.pcap), 1):
    if Raw not in packet:
        continue
    for match in PATTERN.finditer(bytes(packet[Raw].load)):
        hits += 1
        field = match.group(1).decode(errors="replace")
        endpoint = "bilinmiyor"
        if IP in packet and TCP in packet:
            endpoint = f"{packet[IP].src}:{packet[TCP].sport}->{packet[IP].dst}:{packet[TCP].dport}"
        print(f"[UYARI] paket={number} alan={field} değer=<MASKELENDİ> akış={endpoint}")
print(f"[BİLGİ] Toplam gösterge: {hits}")
