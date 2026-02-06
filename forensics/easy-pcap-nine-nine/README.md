# Brooklyn Nine Nine CTF - PCAP Analysis Challenge

## Genel Bakış

Bu proje, Brooklyn Nine Nine temalı bir CTF (Capture The Flag) PCAP analizi sorusu için traffic oluşturucu Python uygulamasıdır. Uygulama, gerçekçi network trafiği simüle eder ve içinde gizli flagler barındırır.

## Özellikler

### Network Protokolleri
- **DNS Traffic**: TXT kayıtlarında gizli mesajlar
- **HTTP Traffic**: POST verilerinde base64 kodlanmış flagler
- **ICMP Traffic**: Ping paketlerinin data kısmında gizli bilgiler
- **FTP Traffic**: Dosya transferi ve authentication bilgilerinde ipuçları
- **Telnet Traffic**: Komut geçmişinde flagler
- **Noise Traffic**: Zorluğu artırmak için rastgele paketler

### Brooklyn Nine Nine Teması
- Karakterlere özel IP adresleri ve hostname'ler
- Diziden referanslar (NINE-NINE!, Cool cool cool, Title of your sex tape, vb.)
- Gerçekçi senaryo: "The Case of the Missing Files"

## Kurulum

### Gereksinimler
```bash
pip install -r requirements.txt
```

veya manuel olarak:
```bash
pip install scapy
```

**Not**: Linux sistemlerde root/sudo yetkisi gerekebilir.

### Çalıştırma
```bash
# Root yetkisi ile çalıştırma (Linux)
sudo python3 b99_pcap_generator.py

# veya normal kullanıcı ile (bazı sistemlerde)
python3 b99_pcap_generator.py
```

## Çıktı

Uygulama `b99_challenge.pcap` dosyasını oluşturur ve bu dosya:
- 100+ network paketi içerir
- 5 farklı protokolde gizli flag barındırır
- Wireshark veya tshark ile analiz edilebilir

## Flag'leri Bulma

### Flag 1: DNS (Kolay)
- **İpucu**: Gina'nın secret backup DNS sorgusu
- **Filtre**: `dns.qry.name contains "gina"`
- **Protokol**: DNS TXT kaydı
- **Kodlama**: Base64

### Flag 2: HTTP (Orta)
- **İpucu**: Jake'in evidence upload'u
- **Filtre**: `http.request.method == "POST"`
- **Lokasyon**: POST data - secret_note parametresi
- **Kodlama**: Base64

### Flag 3: ICMP (Orta)
- **İpucu**: Jake'in Rosa'ya gönderdiği ping
- **Filtre**: `icmp && ip.src == 192.168.99.1 && ip.dst == 192.168.99.6`
- **Lokasyon**: ICMP payload
- **Kodlama**: Base64

### Flag 4: FTP (Kolay)
- **İpucu**: Charles'ın şifresi
- **Filtre**: `ftp`
- **Lokasyon**: PASS komutu
- **Kodlama**: Plaintext

### Flag 5: Telnet (Orta)
- **İpucu**: Holt'un terminal geçmişi
- **Filtre**: `telnet`
- **Teknik**: TCP stream follow
- **Kodlama**: Plaintext

## Analiz Araçları

### Wireshark
```bash
wireshark b99_challenge.pcap
```

Faydalı filtreler:
```
dns
http
icmp
ftp
telnet
tcp.stream eq 0
```

### tshark (CLI)
```bash
# Tüm DNS trafiğini göster
tshark -r b99_challenge.pcap -Y "dns"

# HTTP POST isteklerini göster
tshark -r b99_challenge.pcap -Y "http.request.method == POST" -T fields -e http.file_data

# ICMP payload'ları göster
tshark -r b99_challenge.pcap -Y "icmp" -T fields -e data.data

# FTP komutlarını göster
tshark -r b99_challenge.pcap -Y "ftp" -T fields -e ftp.request.command -e ftp.request.arg
```

### Python ile Analiz
```python
from scapy.all import *

# PCAP'i oku
packets = rdpcap("b99_challenge.pcap")

# DNS paketlerini filtrele
dns_packets = [p for p in packets if p.haslayer(DNS)]

# HTTP paketlerini analiz et
for p in packets:
    if p.haslayer(Raw):
        payload = p[Raw].load
        if b"POST" in payload:
            print(payload.decode(errors='ignore'))
```

## Özelleştirme

### Flag'leri Değiştirme
`b99_pcap_generator.py` dosyasında flag değerlerini değiştirebilirsiniz:

```python
# DNS flag
flag_encoded = base64.b64encode(b"B99{YENI_FLAG}").decode()

# HTTP flag
post_data = "secret_note=<base64_encoded_flag>"

# vb.
```

### Zorluk Seviyesini Artırma
1. **Daha fazla noise traffic ekleyin**:
```python
def add_noise_traffic(self):
    for _ in range(100):  # 20'den 100'e çıkarın
        # ...
```

2. **Şifreleme ekleyin**:
```python
# XOR, ROT13, vb. ekleyin
import codecs
flag = codecs.encode("B99{FLAG}", 'rot_13')
```

3. **Multi-step çözüm gerektirin**:
```python
# Flag'i parçalara bölün ve farklı protokollere dağıtın
```

## Çözüm Örneği

### Adım 1: PCAP'i Aç
```bash
wireshark b99_challenge.pcap
```

### Adım 2: DNS Trafiğini İncele
- Filtre: `dns`
- Gina'nın TXT sorgusunu bul
- Base64 string'i decode et

### Adım 3: HTTP POST'u İncele
- Filtre: `http.request.method == "POST"`
- secret_note parametresini bul
- Base64 decode

### Adım 4: ICMP Payload'unu Kontrol Et
- Filtre: `icmp`
- Jake->Rosa paketini bul (ID: 9999, Seq: 99)
- Payload'u base64 decode et

### Adım 5: FTP Trafiğini Takip Et
- Filtre: `ftp`
- PASS komutunu bul

### Adım 6: Telnet Stream'i Follow Et
- Telnet paketine sağ tık
- Follow -> TCP Stream
- cat flag.txt çıktısını bul

## Eğitim Amaçları

Bu proje şunları öğretir:
- ✅ PCAP dosyası analizi
- ✅ Wireshark kullanımı
- ✅ Network protokollerini anlama
- ✅ Base64 encoding/decoding
- ✅ TCP stream reconstruction
- ✅ Paket filtreleme teknikleri
- ✅ Forensics temelleri

## Lisans

Bu proje eğitim amaçlıdır. Kendi CTF yarışmalarınızda kullanabilirsiniz.

## Katkıda Bulunma

İyileştirme önerileri için pull request gönderin:
- Yeni protokol desteği
- Daha karmaşık flag gizleme teknikleri
- Ek Brooklyn Nine Nine referansları
- Otomatik çözüm script'i

## Yaratıcı: Anthropic Claude
NINE-NINE! 🚔
