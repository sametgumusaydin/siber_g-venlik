# SYN-Flooder Bölüm Özeti ve Güvenli Laboratuvar Kılavuzu

## 1. Kitaptaki bölümün ana fikri

Kitabın 5.7 numaralı **SYN-Flooder** bölümü, TCP bağlantısının kurulmasında kullanılan üçlü el sıkışmanın kötüye kullanılmasını anlatır. Normal süreç şöyledir:

1. İstemci, sunucuya `SYN` gönderir.
2. Sunucu, `SYN/ACK` ile cevap verir ve bağlantı için geçici kaynak ayırır.
3. İstemci, `ACK` göndererek bağlantıyı tamamlar.

Üçüncü adım gerçekleşmezse bağlantı bir süre **yarı açık (half-open)** durumda kalır. Çok sayıda yarı açık bağlantı, sunucunun bağlantı kuyruğunu ve diğer kaynaklarını tüketebilir. Sonuçta gerçek kullanıcıların yeni bağlantıları gecikebilir veya reddedilebilir. Bu durum **SYN flooding**, yani SYN taşması olarak adlandırılan bir **DoS (Denial of Service - Hizmet Engelleme)** tekniğinin temelidir.

Kitaptaki özgün örnek, Scapy ile sahte kaynak IP adresli TCP SYN paketleri oluşturur; hedefteki 1-1023 port aralığını kullanır ve `srflood()` ile sınırsız biçimde gönderir. Kaynak IP sahteciliği, cevapların başka bir sisteme gitmesine ve o sistemin de istemeden trafik üretmesine yol açabilir. Bu nedenle özgün kod gerçek veya kurumsal ağda çalıştırılmamalıdır.

## 2. Düzeltilmiş kod neden farklıdır?

`syn_flood_lab_demo.py`, bölümdeki paket oluşturma mantığını öğretir ancak kesinti oluşturan sınırsız gönderimi tekrar etmez:

- Varsayılan olarak ağa paket göndermez; paketleri `syn_lab_demo.pcap` dosyasına yazar.
- Canlı gönderim yalnızca özel, loopback veya link-local laboratuvar IP adreslerine izinlidir.
- Tek bir hedef port kullanır.
- Paket sayısı en fazla 200'dür.
- Paketler arasında en az 0,05 saniye bekler.
- Canlı gönderim için açık bir `IZINLI-LAB` onayı ister.
- Kaynak IP sahteciliği yapmaz.

Bu sınırlar nedeniyle uygulama gerçek bir SYN flood aracı değil, SYN paketlerini ve savunma gözlemlerini öğretmeye yönelik kontrollü bir gösterimdir.

## 3. Kurulum

Yalnızca size ait veya yazılı izin verilmiş, internetten ayrılmış bir laboratuvar ağı kullanın.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install scapy
```

Kali Linux üzerinde ağ arayüzlerini görmek için:

```bash
ip -br address
```

## 4. Önce çevrimdışı PCAP üretin

Aşağıdaki komut 20 adet SYN paketi oluşturur; hiçbirini ağa göndermez:

```bash
python syn_flood_lab_demo.py 192.168.56.20 -p 80 -c 20 --pcap syn_lab_demo.pcap
```

PCAP dosyasını Wireshark ile açın:

```bash
wireshark syn_lab_demo.pcap
```

Kullanılabilecek görüntüleme filtreleri:

```text
tcp.flags.syn == 1 && tcp.flags.ack == 0
```

```text
ip.dst == 192.168.56.20 && tcp.dstport == 80
```

İncelenecek alanlar:

- `Internet Protocol Version 4 > Destination Address`
- `Transmission Control Protocol > Source Port`
- `Transmission Control Protocol > Destination Port`
- `Transmission Control Protocol > Sequence Number`
- `Transmission Control Protocol > Flags > Syn`

## 5. İzinli kapalı laboratuvarda canlı gözlem

Hedef makine yalnızca eğitim laboratuvarına aitse ve öğretim elemanı izin verdiyse:

```bash
sudo .venv/bin/python syn_flood_lab_demo.py 192.168.56.20 \
  -p 80 -c 20 --delay 0.20 --send --confirm IZINLI-LAB
```

Hedefte Wireshark veya `tcpdump` ile trafiği gözlemleyin:

```bash
sudo tcpdump -ni any 'tcp[tcpflags] & tcp-syn != 0 and port 80'
```

Sunucuda 80 numaralı port kapalıysa genellikle `RST/ACK`; açıksa `SYN/ACK` cevabı görülür. Bu sınırlı uygulamada gönderen işletim sistemi gelen `SYN/ACK` cevabına `RST` üretebilir. Bu yüzden amaç bağlantı kuyruğunu doldurmak değil, paket akışını gözlemlemektir.

## 6. Kitaptaki kodun satır mantığı

Kitaptaki örnekte:

- `IP(src=..., dst=...)`: Kaynak ve hedef IP alanlarını belirler.
- `TCP(dport=range(1,1024), flags="S")`: 1-1023 hedef portları için SYN bayrağı işaretli TCP katmanı oluşturur.
- `/` operatörü: Scapy'de IP ve TCP katmanlarını üst üste ekler.
- `srflood(packet)`: Paketleri sürekli gönderir ve cevapları almaya çalışır.

Son satır sınırsız trafik oluşturabildiğinden öğrenci laboratuvarı için uygun değildir. Verilen güvenli sürüm, aynı kavramları `wrpcap()` ve adet/hız sınırlarıyla gösterir.

## 7. Savunma yöntemleri

### SYN cookies

Sunucu, ilk SYN geldiğinde tam bağlantı durumunu hemen bellekte tutmak yerine gerekli bilgiyi ürettiği başlangıç sıra numarasına kodlayabilir. Geçerli ACK dönerse bağlantı durumu oluşturulur. Linux'ta güncel değeri görmek için:

```bash
sysctl net.ipv4.tcp_syncookies
```

Yetkili sistem yöneticisi tarafından etkinleştirmek için:

```bash
sudo sysctl -w net.ipv4.tcp_syncookies=1
```

### Diğer önlemler

- Güvenlik duvarında bağlantı ve SYN hız sınırlaması uygulamak
- Yarı açık bağlantı kuyruğunu, zaman aşımını ve sunucu kapasitesini uygun biçimde ayarlamak
- IDS/IPS üzerinde anormal SYN oranı ve düşük ACK tamamlama oranı için alarm üretmek
- Kaynak ağlarda sahte IP çıkışını azaltmak için ingress/egress filtreleme kullanmak
- İnternete açık hizmetlerde DDoS koruma ve upstream filtreleme hizmetlerinden yararlanmak

Tek bir ayar bütün saldırıları engellemez; ağ, işletim sistemi ve uygulama katmanındaki önlemler birlikte kullanılmalıdır.

## 8. Öğrenci değerlendirme soruları

1. TCP üçlü el sıkışmasının üç adımını yazınız.
2. Yarı açık bağlantı hangi durumda oluşur?
3. SYN taşması erişilebilirliği nasıl etkiler?
4. Kaynak IP sahteciliği neden üçüncü bir sisteme zarar verebilir?
5. SYN cookies bağlantı kuyruğundaki yükü nasıl azaltır?
6. Wireshark'ta yalnızca ilk SYN paketlerini gösteren filtre nedir?
7. Bu laboratuvar kodu neden gerçek bir SYN flood aracı değildir?

## 9. Etik ve yasal sınır

Bu uygulama yalnızca size ait ya da açıkça izin verilmiş, yalıtılmış eğitim sistemlerinde kullanılmalıdır. Üniversite ağı, internet üzerindeki sistemler veya izin kapsamı belirsiz cihazlar hedef olarak seçilmemelidir. Küçük miktarda trafik bile üretim hizmetlerinde beklenmeyen kesintilere veya güvenlik alarmına neden olabilir.
