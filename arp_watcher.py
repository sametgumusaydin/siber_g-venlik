#!/usr/bin/env python3
import argparse
import json
import signal
import sys
import time
from pathlib import Path
from scapy.layers.l2 import ARP
from scapy.all import sniff

# çalıştırmak için  "sudo python3 arp_watcher.py -i eno1"   sonrada farklı pc den veya terminalden "sudo arping -I eno1 -c 3 172.16.21.1"

DEFAULT_DB_FILE = Path("./arp_watcher_db.json")

# IP adresi -> MAC adresi    # burayı kendinize uygun değiştirmeniz gerekir.
ip_mac = {
    "172.18.28.1": "aa:bb:sd:3d:cd:3a",
    "172.18.28.14": "a0:d8:b1:bd:24:25"
}


def normalize_mac(mac_address):
    """MAC adresini karşılaştırma için küçük harfe dönüştürür."""
    return mac_address.lower()


def load_database(database_file):
    """Önceden kaydedilmiş IP-MAC eşleşmelerini yükler."""

    if not database_file.exists():
        print(f"[BİLGİ] Veritabanı bulunamadı: {database_file}")
        print("[BİLGİ] Yeni ve boş bir veritabanı oluşturulacak.")
        return {}

    try:
        with database_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Veritabanı sözlük biçiminde değil.")

        normalized_data = {
            str(ip): normalize_mac(str(mac))
            for ip, mac in data.items()
        }

        print(
            f"[BİLGİ] {len(normalized_data)} IP-MAC eşleşmesi yüklendi."
        )

        return normalized_data

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"[HATA] Veritabanı okunamadı: {error}")
        print("[HATA] Güvenlik amacıyla program sonlandırılıyor.")
        sys.exit(1)


def save_database(database_file):
    """Öğrenilen IP-MAC eşleşmelerini dosyaya kaydeder."""

    try:
        database_file.parent.mkdir(parents=True, exist_ok=True)

        temporary_file = database_file.with_suffix(".tmp")

        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(
                ip_mac,
                file,
                indent=4,
                sort_keys=True
            )

        temporary_file.replace(database_file)

        print(
            f"[BİLGİ] {len(ip_mac)} eşleşme kaydedildi: "
            f"{database_file}"
        )

    except OSError as error:
        print(f"[HATA] Veritabanı kaydedilemedi: {error}")


def shutdown_handler(signum, frame):
    """Ctrl+C veya sonlandırma sinyali alındığında çalışır."""

    print("\n[BİLGİ] Program kapatılıyor.")
    save_database(args.database)
    sys.exit(0)


def watch_arp(packet):
    """Yakalanan ARP cevaplarını inceler."""

    if not packet.haslayer(ARP):
        return

    # op=2, ARP Reply yani ARP cevabıdır.
    if packet[ARP].op != 2:
        return

    source_ip = packet[ARP].psrc
    source_mac = normalize_mac(packet[ARP].hwsrc)
    old_mac = ip_mac.get(source_ip)

    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    print(
        f"[{current_time}] ARP cevabı: "
        f"{source_ip} -> {source_mac}"
    )

    # IP adresi daha önce görülmemişse yeni cihaz olarak kaydedilir.
    if old_mac is None:
        print(
            f"[YENİ CİHAZ] IP={source_ip}, MAC={source_mac}"
        )

        ip_mac[source_ip] = source_mac
        save_database(args.database)
        return

    # Aynı IP daha önce farklı bir MAC adresiyle biliniyorsa uyarı verilir.
    if old_mac != source_mac:
        print("=" * 70)
        print("[UYARI] IP-MAC eşleşmesi değişti!")
        print(f"[UYARI] IP adresi : {source_ip}")
        print(f"[UYARI] Eski MAC  : {old_mac}")
        print(f"[UYARI] Yeni MAC  : {source_mac}")
        print("[UYARI] ARP spoofing olasılığı araştırılmalıdır.")
        print("=" * 70)

        ip_mac[source_ip] = source_mac
        save_database(args.database)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "ARP cevaplarını izler, yeni cihazları bildirir ve "
            "IP-MAC değişiklikleri için uyarı üretir."
        )
    )

    parser.add_argument(
        "-i",
        "--interface",
        required=True,
        help="Dinlenecek ağ arayüzü; örneğin eth0"
    )

    parser.add_argument(
        "-d",
        "--database",
        type=Path,
        default=DEFAULT_DB_FILE,
        help=(
            "ARP eşleşmelerinin kaydedileceği JSON dosyası "
            "(varsayılan: ./arp_watcher_db.json)"
        )
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    ip_mac.update(load_database(args.database))

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    print(f"[BİLGİ] Dinlenen arayüz: {args.interface}")
    print(f"[BİLGİ] Veritabanı: {args.database}")
    print("[BİLGİ] ARP cevapları bekleniyor.")
    print("[BİLGİ] Durdurmak için Ctrl+C kullanın.")

    try:
        sniff(
            iface=args.interface,
            filter="arp",
            prn=watch_arp,
            store=False
        )

    except PermissionError:
        print(
            "[HATA] Paket yakalama yetkisi bulunamadı. "
            "Programı uygun yetkiyle çalıştırın."
        )
        sys.exit(1)

    except OSError as error:
        print(f"[HATA] Ağ arayüzü veya paket yakalama hatası: {error}")
        sys.exit(1)