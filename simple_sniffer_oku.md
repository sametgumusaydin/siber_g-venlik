# Basit Paket Dinleyici Öğrenci Uygulama Kılavuzu

**Kitaptaki başlık:** A Simple Sniffer  
**Bölüm:** 5.2  
**Basılı sayfalar:** 47-49  
**Bölüm:** Bilgisayar Mühendisliği

## Amaç ve kapsam

Kitap, şifrelenmemiş ağ trafiğinin bir paket dinleyiciyle okunabildiğini ve bunun yalnızca açık yetkiyle gösterilmesi gerektiğini vurgular. Özgün örnek pcapy ve Impacket ile canlı arayüzden paket çözümler. Bu paket, aynı kavramı canlı dinleme yerine önceden kaydedilmiş PCAP üzerinde gösterir.

Bu paketteki `simple_sniffer_lab.py` dosyası saldırı üretmek için değil, kavramı yalıtılmış veya çevrimdışı laboratuvarda savunma açısından incelemek için hazırlanmıştır. Yalnızca size ait ya da açıkça izin verilmiş verileri ve sistemleri kullanın.

```mermaid
flowchart LR
    A["Yetkili PCAP"] --> B
    B["Paketleri çözümle"] --> C
    C["Başlıkları özetle"] --> D
    D["Hassas veriyi koru"]
```

## Temel kavramlar

- Sniffer, ağ çerçevelerini yakalayan veya kayıtlı trafiği çözümleyen araçtır.
- BPF filtreleri yalnızca ilgili paketlerin seçilmesini sağlar.
- Şifreleme yoksa uygulama verisi paket yükünde okunabilir olabilir.
- Promiscuous mode, arayüzün kendisine adreslenmeyen çerçeveleri de işletim sistemine iletmesine izin verebilir.

## Güvenli laboratuvar görevi

Öğrencinin kendisine ait bir PCAP dosyasını okuyarak paket zamanı, kaynak, hedef ve protokol özetini üretmek.

### Kurulum

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install scapy
```

### Çalıştırma

```bash
python simple_sniffer_lab.py --pcap ornek.pcap --limit 25
```

## İncelenecek noktalar

- Paket sayısı ve zaman damgası
- IP kaynak ve hedefleri
- TCP veya UDP portları
- ARP paketleri

Kod önce sözdizimi açısından kontrol edilebilir:

```bash
python -m py_compile simple_sniffer_lab.py
```

Scapy kullanan uygulamalarda bir PCAP dosyası üretildiyse Wireshark ile açın. İlgili protokol katmanını genişletin; kaynak, hedef, bayrak ve yük alanlarını uygulamanın çıktısıyla karşılaştırın.

## Savunma yöntemleri

- Hassas protokollerde TLS veya SSH kullanmak
- Anahtarlamalı ağ ve VLAN ayrımı uygulamak
- Paket yakalama yetkilerini sınırlandırmak
- PCAP dosyalarını hassas veri olarak korumak

## Sorun giderme

| Sorun | Kontrol |
|---|---|
| ModuleNotFoundError | Sanal ortamı etkinleştirip gerekli paketi kurun. |
| Dosya bulunamadı | PCAP veya çalışma dosyasının yolunu doğrulayın. |
| Permission denied | Canlı yakalama yapmayın; yetkili çevrimdışı PCAP kullanın. |
| Sonuç çıkmadı | Filtreyi, örnek veriyi ve beklenen protokolü kontrol edin. |

## Değerlendirme soruları

1. Sniffer ile port tarayıcı arasındaki fark nedir?
2. BPF filtresi ne sağlar?
3. Şifreleme paket yükünü nasıl etkiler?
4. PCAP neden hassas veri kabul edilmelidir?

## Etik ve yasal sınır

Bu uygulama üretim ağına, üniversite ağına veya internet üzerindeki üçüncü taraf sistemlere yöneltilmemelidir. Kimlik bilgileri, oturum verileri ve PCAP dosyaları hassas kabul edilmelidir. Laboratuvar sonucu yalnızca ders kapsamında ve yetkili kişilerle paylaşılmalıdır.

## Kaynak notu

Bu kılavuz, *Understanding Network Hacks Attack and Defense with Python 3* kitabındaki **5.2 A Simple Sniffer** başlığının 47-49 numaralı basılı sayfalarındaki kavramlar temel alınarak, güncel ve güvenli laboratuvar yaklaşımıyla yeniden düzenlenmiştir.
