# Brooklyn Nine Nine CTF - Cheat Sheet

## 🚀 Hızlı Komutlar

### PCAP Oluştur
```bash
sudo python3 b99_pcap_generator.py
```

### Çözücüyü Çalıştır
```bash
python3 b99_solver.py b99_challenge.pcap
```

### Wireshark'ta Aç
```bash
wireshark b99_challenge.pcap
```

## 🎯 Flag Konumları

| # | Protokol | Lokasyon | Encoding | Flag Formatı |
|---|----------|----------|----------|--------------|
| 1 | DNS      | TXT record | Base64 |  |
| 2 | HTTP     | POST data - secret_note | Base64 |  |
| 3 | ICMP     | Ping payload (ID:9999, Seq:99) | Base64 |  |
| 4 | FTP      | PASS command | Plaintext |  |
| 5 | Telnet   | cat flag.txt output | Plaintext |  |

## 🔍 Wireshark Filtreleri

```
dns                                    # Tüm DNS trafiği
dns.qry.name contains "gina"          # Gina'nın DNS sorgusu
http.request.method == "POST"         # POST istekleri
icmp && icmp.ident == 9999            # Özel ICMP paketi
ftp                                    # FTP trafiği
ftp.request.command == "PASS"         # FTP şifreleri
tcp.port == 23                        # Telnet trafiği
tcp.stream eq 0                       # İlk TCP stream
frame contains "B99"                  # B99 içeren paketler
```

## 🛠️ Decode Komutları

### Base64 Decode
```bash
# Linux/Mac
echo "BASE64_STRING" | base64 -d

# Python
python3 -c "import base64; print(base64.b64decode('BASE64_STRING').decode())"
```

### Hex to ASCII
```bash
echo "48656c6c6f" | xxd -r -p
```

## 📊 tshark Komutları

### DNS Flag
```bash
tshark -r b99_challenge.pcap -Y "dns.qry.name contains 'gina'" -T fields -e dns.txt
```

### HTTP Flag
```bash
tshark -r b99_challenge.pcap -Y "http.request.method == POST" -T fields -e http.file_data
```

### ICMP Flag
```bash
tshark -r b99_challenge.pcap -Y "icmp.ident == 9999" -T fields -e data.data
```

### FTP Flag
```bash
tshark -r b99_challenge.pcap -Y "ftp.request.command == PASS" -T fields -e ftp.request.arg
```

### Telnet Flag
```bash
tshark -r b99_challenge.pcap -Y "tcp.port == 23 && tcp.payload" -T fields -e tcp.payload | xxd -r -p
```

## 🐍 Python One-Liners

### DNS Analysis
```python
from scapy.all import *; import base64; [print(base64.b64decode(p[DNS].an.rdata).decode()) for p in rdpcap("b99_challenge.pcap") if p.haslayer(DNS) and p[DNS].qr and p[DNS].an and p[DNS].an.type == 16]
```

### HTTP Analysis
```python
from scapy.all import *; import re; [print(re.search(r'secret_note=([^&]+)', p[Raw].load.decode('utf-8', errors='ignore')).group(1)) for p in rdpcap("b99_challenge.pcap") if p.haslayer(Raw) and b'secret_note=' in p[Raw].load]
```

### ICMP Analysis
```python
from scapy.all import *; [print(p[Raw].load.decode()) for p in rdpcap("b99_challenge.pcap") if p.haslayer(ICMP) and p.haslayer(Raw) and p[ICMP].id == 9999]
```

## 💡 İpuçları

### Wireshark Kullanımı
- **Sağ Tık → Follow → TCP/HTTP Stream**: Stream'i takip et
- **Ctrl+F**: Paket içinde ara
- **Statistics → Protocol Hierarchy**: Protokol dağılımını gör
- **Statistics → Conversations**: IP konuşmalarını gör

### Base64 Tanıma
- Sadece `A-Z`, `a-z`, `0-9`, `+`, `/`, `=` karakterleri içerir
- Uzunluk 4'ün katıdır (padding ile)
- `=` veya `==` ile bitebilir

### TCP Stream Numarası Bulma
1. Pakete sağ tık
2. "Conversation Filter → TCP" seç
3. Stream ID `tcp.stream eq X` olarak görünür

## 🔑 Cevap Anahtarı

```
Flag 1 (DNS):    
Flag 2 (HTTP):   
Flag 3 (ICMP):   
Flag 4 (FTP):    
Flag 5 (Telnet): 
```

## 📝 Karakter → IP Eşleşmesi

```
Jake:     192.168.99.1
Amy:      192.168.99.2
Holt:     192.168.99.3
Gina:     192.168.99.4
Charles:  192.168.99.5
Rosa:     192.168.99.6
Terry:    192.168.99.7
Server:   192.168.99.100
Evidence: 192.168.99.101
```

## 🎓 Öğrenme Yolu

1. ✅ DNS trafiğini analiz et (Kolay)
2. ✅ FTP şifrelerini bul (Kolay)
3. ✅ HTTP POST verilerini incele (Orta)
4. ✅ ICMP payload'unu keşfet (Orta)
5. ✅ Telnet stream'i reconstruct et (Orta)

## 🚨 Sık Yapılan Hatalar

❌ Base64 padding'i unutmak
✅ Online decoder kullan veya padding ekle

❌ Display filter yerine capture filter kullanmak
✅ Üstteki arama çubuğunu kullan (display filter)

❌ TCP stream'i follow etmemek
✅ Sağ tık → Follow → TCP Stream

❌ Hex değerleri decode etmemek
✅ CyberChef veya `xxd -r -p` kullan

## 🎬 Brooklyn Nine Nine Referansları

- **NINE-NINE!**: Captain Holt'un war cry'ı
- **Title of your sex tape**: Jake ve Amy'nin içten esprileri
- **Cool cool cool no doubt**: Jake'in ağız alışkanlığı
- **HOT DAMN!**: Captain Holt'un heyecan ifadesi
- **VINDICATION!**: Holt'un haklı çıkma anları
- **Cheddar**: Holt'un köpeği

NINE-NINE! 🚔
