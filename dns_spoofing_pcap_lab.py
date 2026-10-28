#!/usr/bin/env python3
"""DNS sorgu/sahte cevap çiftini yalnızca PCAP'a yazar."""
import argparse
from scapy.all import DNS, DNSQR, DNSRR, IP, UDP, wrpcap

parser = argparse.ArgumentParser(description="Çevrimdışı DNS spoofing laboratuvarı")
parser.add_argument("--output", default="dns_spoofing_demo.pcap")
args = parser.parse_args()
query = IP(src="192.0.2.50", dst="192.0.2.53")/UDP(sport=53000,dport=53)/DNS(id=0x1234,qd=DNSQR(qname="test.invalid"))
answer = IP(src="192.0.2.53", dst="192.0.2.50")/UDP(sport=53,dport=53000)/DNS(id=0x1234,qr=1,aa=1,qd=query[DNS].qd,an=DNSRR(rrname="test.invalid",ttl=60,rdata="198.51.100.77"))
wrpcap(args.output, [query, answer])
print(f"[BİLGİ] PCAP yazıldı: {args.output}; ağa paket gönderilmedi.")
