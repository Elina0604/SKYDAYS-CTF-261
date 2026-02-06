# Brooklyn Nine Nine CTF - Kullanım Kılavuzu

## Hızlı Başlangıç

### 1. Kurulum

```bash
# Repository'yi klonlayın veya dosyaları indirin
cd b99-ctf-challenge

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# veya
pip install scapy
```

**Not**: Linux sistemlerde scapy için root yetkisi gerekebilir.

### 2. PCAP Dosyası Oluşturma

```bash
# Root yetkisi ile (Linux)
sudo python3 b99_pcap_generator.py

# veya normal kullanıcı (bazı sistemlerde)
python3 b99_pcap_generator.py
```

**Çıktı**: `b99_challenge.pcap` dosyası oluşturulur.

### 3. Challenge'ı Çözme

#### Manuel Analiz (Önerilen - Öğrenme Amaçlı)

```bash
# Wireshark ile analiz
wireshark b99_challenge.pcap

# veya tshark ile (CLI)
tshark -r b99_challenge.pcap
```

#### Otomatik Çözücü (Kontrol Amaçlı)

```bash
python3 b99_solver.py b99_challenge.pcap
```

## Detaylı Analiz Adımları

### Flag 1: DNS - "Gina's Secret Backup"

**Amaç**: DNS TXT kaydında gizli mesajı bul

**Wireshark Adımları**:
1. Filtre uygula: `dns`
2. DNS query'leri incele
3. "gina-secret-backup.precinct99.local" içeren paketi bul
4. DNS Response paketini incele
5. TXT kaydındaki base64 string'i kopyala
6. Decode et:
   ```bash
   echo "Qjk5e05JTkVfTklORX0=" | base64 -d
   ```

**tshark ile**:
```bash
tshark -r b99_challenge.pcap -Y "dns.qry.name contains 'gina'" -T fields -e dns.txt
```

**Alternatif - Python**:
```python
from scapy.all import *
import base64

pkts = rdpcap("b99_challenge.pcap")
for pkt in pkts:
    if pkt.haslayer(DNS) and pkt[DNS].qr == 1:
        if pkt[DNS].an and pkt[DNS].an.type == 16:
            txt = pkt[DNS].an.rdata
            print(base64.b64decode(txt).decode())
```

### Flag 2: HTTP - "Jake's Evidence Upload"

**Amaç**: HTTP POST verilerinde secret_note parametresini bul

**Wireshark Adımları**:
1. Filtre: `http.request.method == "POST"`
2. POST request paketini bul
3. Packet Details → Hypertext Transfer Protocol → HTML Form URL Encoded
4. `secret_note` parametresini bul
5. Base64 decode et

**tshark ile**:
```bash
tshark -r b99_challenge.pcap -Y "http.request.method == POST" -T fields -e http.file_data | grep -o 'secret_note=[^&]*'
```

**Follow HTTP Stream**:
1. HTTP POST paketine sağ tık
2. Follow → HTTP Stream
3. secret_note değerini kopyala
4. Base64 decode:
   ```bash
   echo "Qjk5e1RJVExFX09GX1lPVVJfU0VYX1RBUEV9" | base64 -d
   ```

### Flag 3: ICMP - "Cool Cool Cool"

**Amaç**: ICMP ping paketinin data kısmında gizli mesaj

**Wireshark Adımları**:
1. Filtre: `icmp`
2. ICMP paketlerini incele
3. ID: 9999 ve Sequence: 99 olan paketi bul
4. Packet Details → Data → expand
5. Data payload'unu kopyala
6. Base64 decode et

**tshark ile**:
```bash
tshark -r b99_challenge.pcap -Y "icmp.ident == 9999 && icmp.seq == 99" -T fields -e data.data
```

**Hex to ASCII dönüşümü**:
```bash
# Eğer hex formatında ise
echo "Qjk5e0NPT0xfQ09PTF9DT09MX05PX0RPVUJUX30=" | xxd -r -p | base64 -d
```

### Flag 4: FTP - "Charles' Password"

**Amaç**: FTP authentication sırasında kullanılan şifreyi bul

**Wireshark Adımları**:
1. Filtre: `ftp`
2. FTP Request komutlarını incele
3. `PASS` komutunu bul
4. Password değeri direkt flag'dir (base64 yok)

**tshark ile**:
```bash
tshark -r b99_challenge.pcap -Y "ftp.request.command == PASS" -T fields -e ftp.request.arg
```

**Follow TCP Stream**:
1. FTP paketine sağ tık
2. Follow → TCP Stream
3. USER ve PASS komutlarını gör

### Flag 5: Telnet - "Holt's Vindication"

**Amaç**: Telnet oturumunda çalıştırılan komutları ve çıktıyı bul

**Wireshark Adımları**:
1. Filtre: `tcp.port == 23`
2. Telnet paketlerinden birine sağ tık
3. Follow → TCP Stream
4. Stream içeriğinde `cat flag.txt` komutunu ve çıktısını bul
5. Flag plaintext olarak görünür

**tshark ile**:
```bash
tshark -r b99_challenge.pcap -Y "tcp.port == 23" -T fields -e tcp.payload | xxd -r -p
```

**Python ile TCP Stream Reconstruction**:
```python
from scapy.all import *

pkts = rdpcap("b99_challenge.pcap")
telnet_data = b""

for pkt in pkts:
    if pkt.haslayer(TCP) and (pkt[TCP].dport == 23 or pkt[TCP].sport == 23):
        if pkt.haslayer(Raw):
            telnet_data += pkt[Raw].load

print(telnet_data.decode('utf-8', errors='ignore'))
```

## İpuçları ve Püf Noktaları

### Wireshark Faydalı Filtreler

```
# Tüm HTTP trafiği
http

# POST istekleri
http.request.method == "POST"

# Belirli IP'den gelen paketler
ip.src == 192.168.99.1

# DNS sorguları
dns.flags.response == 0

# DNS cevapları
dns.flags.response == 1

# TCP stream ID ile filtreleme
tcp.stream eq 5

# Belirli string içeren paketler
frame contains "B99"

# Paket boyutu filtresi
frame.len > 100
```

### Base64 Decode Araçları

**Linux/Mac**:
```bash
echo "BASE64_STRING" | base64 -d
```

**Python**:
```python
import base64
decoded = base64.b64decode("BASE64_STRING").decode()
print(decoded)
```

**Online**:
- https://www.base64decode.org/
- CyberChef (https://gchq.github.io/CyberChef/)

### CyberChef Kullanımı

1. https://gchq.github.io/CyberChef/ adresine git
2. Input kısmına base64 string'i yapıştır
3. Operations → "From Base64" sürükle
4. Output'ta decoded değer görünür

## Yaygın Hatalar ve Çözümleri

### Hata 1: "Permission denied"
**Çözüm**: Script'i sudo ile çalıştır
```bash
sudo python3 b99_pcap_generator.py
```

### Hata 2: "scapy module not found"
**Çözüm**: scapy'yi kur
```bash
pip install scapy
# veya
pip3 install scapy
```

### Hata 3: Base64 decode hatası
**Çözüm**: Padding ekle
```python
import base64
def decode_base64(s):
    # Padding ekle
    missing_padding = len(s) % 4
    if missing_padding:
        s += '=' * (4 - missing_padding)
    return base64.b64decode(s).decode()
```

### Hata 4: Wireshark'ta paketler görünmüyor
**Çözüm**: Display filter yerine capture filter kullanıyor olabilirsiniz
- Display filter (üstte): `http` yazın
- Capture filter değil, display filter kullanın

## Ekstra Bilgiler

### Character IP Mapping

| Karakter  | IP Adresi       | Hostname                    |
|-----------|-----------------|----------------------------|
| Jake      | 192.168.99.1    | jake.precinct99.local      |
| Amy       | 192.168.99.2    | amy.precinct99.local       |
| Holt      | 192.168.99.3    | holt.precinct99.local      |
| Gina      | 192.168.99.4    | gina.precinct99.local      |
| Charles   | 192.168.99.5    | charles.precinct99.local   |
| Rosa      | 192.168.99.6    | rosa.precinct99.local      |
| Terry     | 192.168.99.7    | terry.precinct99.local     |
| Server    | 192.168.99.100  | server.precinct99.local    |
| Evidence  | 192.168.99.101  | evidence.precinct99.local  |

### Port Numaraları

- **21**: FTP
- **23**: Telnet
- **53**: DNS
- **80**: HTTP
- **443**: HTTPS (kullanılmadı)

### Protocol Stack

```
Ethernet (Layer 2)
    ↓
IP (Layer 3)
    ↓
TCP/UDP/ICMP (Layer 4)
    ↓
DNS/HTTP/FTP/Telnet (Layer 7)
```

## Eğitim Hedefleri

Bu challenge'ı tamamladıktan sonra şunları öğrenmiş olacaksınız:

✅ **Network Protokolleri**: DNS, HTTP, FTP, Telnet, ICMP
✅ **Wireshark Kullanımı**: Filtreleme, stream takibi, paket analizi
✅ **Encoding**: Base64 encoding/decoding
✅ **PCAP Analizi**: Trafik analizi ve forensics
✅ **TCP/IP**: 3-way handshake, stream reconstruction
✅ **CTF Teknikleri**: Steganografi, data exfiltration

## İleri Seviye Modifikasyonlar

### 1. Şifreleme Ekle
```python
# XOR ile şifrele
def xor_encrypt(data, key):
    return bytes([b ^ key for b in data.encode()])

flag = xor_encrypt("B99{FLAG}", 0x42)
```

### 2. Multi-step Flag
```python
# Flag'i parçalara böl
flag_part1 = "B99{"
flag_part2 = "COMBINED_"
flag_part3 = "FLAG}"

# Her parçayı farklı protokole gizle
```

### 3. Steganografi
```python
# LSB steganografi ile PNG'ye gizle
# Sonra HTTP ile transfer et
```

### 4. Timing-based Challenge
```python
# Paket zamanlamalarında Morse code gizle
```

### 5. Evil Twin DNS
```python
# DNS spoofing/poisoning simülasyonu
```

## Kaynaklar

- **Wireshark Dokümantasyonu**: https://www.wireshark.org/docs/
- **Scapy Dokümantasyonu**: https://scapy.readthedocs.io/
- **CyberChef**: https://gchq.github.io/CyberChef/
- **CTF Time**: https://ctftime.org/

## Yardım ve Destek

Sorun yaşıyorsanız:

1. README.md dosyasını okuyun
2. Script'teki comment'leri inceleyin
3. Wireshark'ın help menüsünü kullanın
4. Scapy dökümanlarına başvurun

NINE-NINE! 🚔
