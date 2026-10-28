#!/usr/bin/env python3

import argparse
import time

from scapy.all import Raw, RandMAC, sendp
from scapy.layers.l2 import Ether

#sudo .venv/bin/python mac_flooding.py -i enp0s8 -c 20 --delay 0.2

def parse_arguments():
    parser = argparse.ArgumentParser( description=("İzole laboratuvarda switch MAC öğrenmesini ", "göstermek için sınırlı sayıda çerçeve gönderir."))

    parser.add_argument(
        "-i",
        "--interface",
        required=True,
        help="Laboratuvar switch'ine bağlı ağ arayüzü"
    )

    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=20,
        help="Gönderilecek çerçeve sayısı; en fazla 100"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="Çerçeveler arasındaki bekleme süresi"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.count < 1 or args.count > 100:
        raise SystemExit(
            "[HATA] Paket sayısı 1 ile 100 arasında olmalıdır."
        )

    if args.delay < 0.05:
        raise SystemExit(
            "[HATA] Bekleme süresi en az 0.05 saniye olmalıdır."
        )

    destination_mac = "ff:ff:ff:ff:ff:ff"

    print(f"[BİLGİ] Arayüz      : {args.interface}")
    print(f"[BİLGİ] Çerçeve sayısı: {args.count}")
    print(f"[BİLGİ] Gecikme       : {args.delay} saniye")

    for sequence in range(1, args.count + 1):
        source_mac = str(RandMAC("02:*:*:*:*:*"))

        frame = (
            Ether(
                src=source_mac,
                dst=destination_mac
            )
            / Raw(
                load=f"LAB-MAC-LEARNING-{sequence}".encode()
            )
        )

        sendp(
            frame,
            iface=args.interface,
            verbose=False
        )

        print(
            f"[{sequence:03d}] "
            f"Kaynak MAC={source_mac} gönderildi."
        )

        time.sleep(args.delay)

    print("[BİLGİ] Sınırlı laboratuvar gönderimi tamamlandı.")


if __name__ == "__main__":
    main()