# Çift VLAN Etiketli ARP PCAP Öğrenci Kılavuzu

Bu uygulamada Scapy kullanılarak iki adet IEEE 802.1Q VLAN etiketi ve bir ARP Reply içeren örnek Ethernet çerçevesi oluşturulur. Paket gerçek ağa gönderilmez; yalnızca PCAP dosyasına yazılır ve Wireshark üzerinde incelenir. Böylece VLAN double tagging ve ARP spoofing kavramları güvenli biçimde öğrenilir.

```mermaid
flowchart LR
    A["Python ve Scapy"] --> B["Ethernet ve iki 802.1Q etiketi"]
    B --> C["ARP Reply"]
    C --> D["PCAP dosyası"]
    D --> E["Wireshark incelemesi"]
```

# Öğrenme hedefleri

- Ethernet, 802.1Q ve ARP katmanlarının paket içindeki sırasını açıklamak

- Dış ve iç VLAN etiketlerini Wireshark’ta bulmak

- DTP abusing ile double tagging arasındaki farkı açıklamak

- PCAP üretimi ile gerçek ağ paket gönderimi arasındaki farkı kavramak

- Double tagging saldırısına karşı temel switch savunmalarını sıralamak

# Laboratuvar ön koşulları

| **Gereksinim**  | **Açıklama**                                                         |
|-----------------|----------------------------------------------------------------------|
| İşletim sistemi | Kali Linux veya Ubuntu tabanlı laboratuvar sistemi                   |
| Python          | Python 3 ve proje sanal ortamı                                       |
| Scapy           | Paket oluşturma veya yakalama kütüphanesi                            |
| Wireshark       | Paket ve PCAP inceleme aracı                                         |
| Yetki           | Yalnızca kendinize ait veya öğretim elemanının yetkilendirdiği ortam |

## Kurulum kontrolü

> python3 --version  
> python3 -m venv .venv  
> source .venv/bin/activate  
> python -m pip install scapy  
> python -c "import scapy; print(scapy.__version__)"

# Dosyanın güvenlik özelliği

**Önemli:** Dosyada `sendp()` veya ağ arayüzü bulunmaz. `wrpcap()` yalnızca oluşturulan paket nesnesini diskteki PCAP dosyasına yazar. Bu nedenle uygulama, ağdaki başka cihazlara trafik göndermez.

| **Kod bileşeni** | **Görevi**                                                          |
|------------------|---------------------------------------------------------------------|
| Ether            | Kaynak ve hedef MAC adreslerini içeren Ethernet başlığını oluşturur |
| Dot1Q vlan 10    | Dış IEEE 802.1Q etiketini oluşturur                                 |
| Dot1Q vlan 20    | İç IEEE 802.1Q etiketini oluşturur                                  |
| ARP op 2         | ARP Reply mesajını temsil eder                                      |
| wrpcap           | Paket listesini PCAP dosyasına kaydeder                             |

# Uygulama adımları

1.  Terminalde Python dosyasının bulunduğu dizine geçin.

2.  Sanal ortamı etkinleştirin.

3.  Dosyanın sözdizimini kontrol edin.

4.  Python dosyasını çalıştırarak PCAP üretin.

5.  PCAP dosyasını Wireshark ile açın.

> cd ~/PycharmProjects/siberler  
> source .venv/bin/activate  
> python -m py_compile arp_spoofing_vlan.py  
> python arp_spoofing_vlan.py  
> ls -lh double_tagged_vlan_example.pcap  
> wireshark double_tagged_vlan_example.pcap

## Beklenen terminal çıktısı

> [BİLGİ] Örnek PCAP oluşturuldu: double_tagged_vlan_example.pcap  
> [BİLGİ] Dış VLAN etiketi : 10  
> [BİLGİ] İç VLAN etiketi : 20  
> [BİLGİ] Ağ arayüzünden hiçbir paket gönderilmedi.

# Wireshark incelemesi

| **Amaç**               | **Görüntüleme filtresi** |
|------------------------|--------------------------|
| VLAN etiketli paketler | vlan                     |
| ARP içeren VLAN paketi | vlan && arp              |
| VLAN 10 etiketi        | vlan.id == 10            |
| VLAN 20 etiketi        | vlan.id == 20            |
| ARP cevapları          | arp.opcode == 2          |

Paket ayrıntılarında Ethernet II başlığının altında iki ayrı 802.1Q başlığı görülmelidir. İlk etiket dış VLAN 10’u, ikinci etiket iç VLAN 20’yi gösterir. Son katmanda ARP Reply bulunur.

# Kavramsal açıklama

Double tagging, iki VLAN etiketi kullanarak bir çerçevenin başka VLAN’a taşınmasını amaçlayan VLAN hopping yaklaşımıdır. Başarı için native VLAN ve trunk yapılandırmasının elverişli olması gerekir. DTP abusing ise cihazın switch gibi davranarak trunk görüşmesi yapmaya çalışmasıdır; bu dosya DTP paketi üretmez.

| **Kavram**       | **Bu uygulamadaki karşılığı** |
|------------------|-------------------------------|
| Dış VLAN         | 10                            |
| İç VLAN          | 20                            |
| Sahte kaynak MAC | 02:00:00:00:00:10             |
| İddia edilen IP  | 192.168.20.1                  |
| Hedef IP         | 192.168.20.50                 |
| Ağdan gönderim   | Yok                           |

# Savunma yöntemleri

- Kullanıcı portlarını statik access moda almak

- DTP görüşmesini gerekmeyen portlarda kapatmak

- Native VLAN’ı kullanıcı VLAN’larından ayırmak

- Native VLAN trafiğini desteklenen cihazlarda etiketlemek

- Trunk üzerinde izin verilen VLAN listesini sınırlandırmak

- VLAN’lar arası erişimi ACL veya güvenlik duvarıyla kontrol etmek

# Sorun giderme

| **Sorun**                       | **Çözüm**                                                           |
|---------------------------------|---------------------------------------------------------------------|
| ModuleNotFoundError scapy       | Etkin sanal ortamda python -m pip install scapy çalıştırın          |
| PCAP oluşmuyor                  | Dosya dizinini ve yazma iznini kontrol edin                         |
| Wireshark vlan göstermiyor      | Paket ağacını genişletin ve dosyanın doğru PCAP olduğunu doğrulayın |
| Permission denied bekleniyor mu | Hayır; dosya ağdan paket göndermediği için sudo gerekmez            |

# Değerlendirme soruları

1. Paket içinde kaç adet 802.1Q etiketi vardır?

2. Dış ve iç VLAN kimlikleri nelerdir?

3. ARP op=2 ne anlama gelir?

4. Bu dosya neden gerçek ağa zarar vermez?

5. DTP abusing ile double tagging arasındaki temel fark nedir?
