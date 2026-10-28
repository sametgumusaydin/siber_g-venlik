# Paket Dinleyici Tespiti Öğrenci Uygulama Kılavuzu

**Kitaptaki başlık:** Sniffer Detection  
**Bölüm:** 5.5  
**Basılı sayfalar:** 53-54  
**Bölüm:** Bilgisayar Mühendisliği

## Amaç ve kapsam

Kitap, yerel tespitte arayüzlerin promiscuous mode durumunun ve çekirdek günlüklerinin kontrolünü; uzaktan tespitte ise yük gecikmesi ve özel ARP denemelerini anlatır. Uzaktan yöntemlerin güvenilir olmayabileceği ve gereksiz trafik üretebileceği belirtilir. Güvenli kod yalnızca yerel arayüz durumunu denetler.

Bu paketteki `sniffer_detection_audit.py` dosyası saldırı üretmek için değil, kavramı yalıtılmış veya çevrimdışı laboratuvarda savunma açısından incelemek için hazırlanmıştır. Yalnızca size ait ya da açıkça izin verilmiş verileri ve sistemleri kullanın.

```mermaid
flowchart LR
    A["Yerel arayüzler"] --> B
    B["Bayrakları oku"] --> C
    C["PROMISC kontrolü"] --> D
    D["Yetki ve süreç incele"]
```

## Temel kavramlar

- Promiscuous mode tek başına kötü niyet kanıtı değildir.
- Wireshark, tcpdump ve IDS gibi meşru araçlar da bu modu kullanabilir.
- Rootkit veya sanallaştırma katmanı yerel görünürlüğü etkileyebilir.
- Tespit sonucu süreç, kullanıcı ve değişiklik kaydıyla ilişkilendirilmelidir.

## Güvenli laboratuvar görevi

Linux üzerindeki yerel ağ arayüzlerinde PROMISC bayrağını ve ilgili sistem bilgilerini salt okunur biçimde raporlamak.

### Kurulum

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Çalıştırma

```bash
python sniffer_detection_audit.py
```

## İncelenecek noktalar

- Arayüz adı
- UP veya DOWN durumu
- PROMISC bayrağı
- Kontrol zamanı

Kod önce sözdizimi açısından kontrol edilebilir:

```bash
python -m py_compile sniffer_detection_audit.py
```

Scapy kullanan uygulamalarda bir PCAP dosyası üretildiyse Wireshark ile açın. İlgili protokol katmanını genişletin; kaynak, hedef, bayrak ve yük alanlarını uygulamanın çıktısıyla karşılaştırın.

## Savunma yöntemleri

- Paket yakalama yetkilerini ayrı role vermek
- Arayüz bayrak değişikliklerini loglamak
- Yetkisiz capture araçlarını uygulama kontrolüyle engellemek
- EDR ve bütünlük denetimi kullanmak

## Sorun giderme

| Sorun | Kontrol |
|---|---|
| ModuleNotFoundError | Sanal ortamı etkinleştirip gerekli paketi kurun. |
| Dosya bulunamadı | PCAP veya çalışma dosyasının yolunu doğrulayın. |
| Permission denied | Canlı yakalama yapmayın; yetkili çevrimdışı PCAP kullanın. |
| Sonuç çıkmadı | Filtreyi, örnek veriyi ve beklenen protokolü kontrol edin. |

## Değerlendirme soruları

1. PROMISC bayrağı neyi gösterir?
2. Neden kesin saldırı kanıtı değildir?
3. Yerel ve uzaktan tespit arasındaki fark nedir?
4. Bir bulgu hangi loglarla doğrulanabilir?

## Etik ve yasal sınır

Bu uygulama üretim ağına, üniversite ağına veya internet üzerindeki üçüncü taraf sistemlere yöneltilmemelidir. Kimlik bilgileri, oturum verileri ve PCAP dosyaları hassas kabul edilmelidir. Laboratuvar sonucu yalnızca ders kapsamında ve yetkili kişilerle paylaşılmalıdır.

## Kaynak notu

Bu kılavuz, *Understanding Network Hacks Attack and Defense with Python 3* kitabındaki **5.5 Sniffer Detection** başlığının 53-54 numaralı basılı sayfalarındaki kavramlar temel alınarak, güncel ve güvenli laboratuvar yaklaşımıyla yeniden düzenlenmiştir.
