Kategori: OSINT / Steganografi / Network Analizi
Zorluk Seviyesi: Hard

Bu challenge; yarışmacıların Unicode manipülasyonu, versiyon kontrol sistemleri (Git) istihbaratı, açık kaynak tarihi araştırması, steganografi, ağ trafiği analizi ve geolocation (API) becerilerini test eden çok adımlı bir senaryodur.

---

### Adım 1: Zero-Width Character (ZWC) ve Custom Binary Decode

Soru açıklamasında `platform934.jpg` isimli bir dosya ve sonunda ⚡ (High Voltage) emojisi bulunan bir metin verilmektedir. Resim dosyası üzerinde yapılan statik analizler ilk etapta sonuç vermemektedir.

Sıra dışı olan durum, verilen metnin içindeki emojidir. Metin veya sadece emoji CyberChef gibi bir araca alınıp **To Hex** filtresi uygulandığında, emojinin etrafında `E2 80 8B` (Zero Width Space) ve `E2 80 8C` (Zero Width Non-Joiner) gibi görünmez Unicode karakterlerinin yoğun bir şekilde bulunduğu görülür. Standart ZWC web toolları (330k, stegzero vb.) bu metni çözememektedir çünkü veriler standart bir şema ile değil, sadece iki farklı karakter kullanılarak custom bir Binary (0 ve 1) mantığıyla şifrelenmiştir.

Bu custom algoritmayı çözmek ve görünmez baytları saf metne (plaintext) çevirmek için aşağıdaki Python scripti (`decoder.py`) yazılır:

```python
# decoder.py
# Yazarın custom ZWC algoritmasını çözen script

import sys

# Görünmez karakterlerimiz (Encoding scriptimizle tamamen aynı olmalı)
ZWC_0 = '\u200B'  # 0'ı temsil eden karakter
ZWC_1 = '\u200C'  # 1'i temsil eden karakter

def binary_to_text(binary_str):
    # Binary string'i 8 bitlik (1 byte) parçalara böl
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    # Sadece 8 bit uzunluğunda olanları ASCII karaktere çevir (bozuk verileri atla)
    return ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)

def decode_file(file_path):
    try:
        # Dosyayı UTF-8 formatında oku
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Dosyanın içindeki normal harfleri/emojileri boşver, SADECE bizim ZWC'leri ayıkla
        zwc_only = [c for c in content if c in (ZWC_0, ZWC_1)]
        
        if not zwc_only:
            print("[-] Hedef dosyada bizim algoritmaya uygun gizli ZWC verisi bulunamadı!")
            return
        
        # ZWC'leri tekrar 0 ve 1'lere dönüştür
        binary_hidden = ''.join('0' if c == ZWC_0 else '1' for c in zwc_only)
        
        # Binary veriyi saf metne (plaintext) çevir
        decoded_text = binary_to_text(binary_hidden)
        
        print("\n[+] Analiz Tamamlandı! Görünmez baytlar çözüldü.")
        print("-" * 50)
        print(f"Bulan Gizli Mesaj: {decoded_text}")
        print("-" * 50 + "\n")
        
    except FileNotFoundError:
        print(f"[-] Hata: '{file_path}' adında bir dosya bulunamadı!")
    except Exception as e:
        print(f"[-] Decode işlemi sırasında beklenmeyen hata: {e}")

if __name__ == "__main__":
    # Kullanıcıdan terminal argümanı olarak dosya ismini bekle
    if len(sys.argv) < 2:
        print("Kullanım: python3 decoder.py <dosya_adi>")
        print("Örnek:    python3 decoder.py gizli_emoji.txt")
    else:
        hedef_dosya = sys.argv[1]
        print(f"[*] '{hedef_dosya}' dosyası analiz ediliyor...")
        decode_file(hedef_dosya)
```

Terminalde `python3 decoder.py gizli_emoji.txt` komutu çalıştırıldığında gizli mesaj başarıyla elde edilir:
**Çıktı:** `gh:marvolo-gaunt-1926`

---

### Adım 2: GitHub Üzerinde OSINT ve Versiyon Kontrolü

Elde edilen `gh:` ön ekinin GitHub'ı işaret ettiği anlaşılarak `github.com/marvolo-gaunt-1926` profiline gidilir. Hesapta **Horcrux-Tracking** isimli herkese açık bir depo (repository) bulunmaktadır.

Deponun ana dizini boştur. Ancak Git mimarisinin yapısı gereği, deponun **Commit History (İşlem Geçmişi)** bölümü incelendiğinde, `riddles_diary.txt` adında bir dosyanın commit edildiği ve ardından silindiği tespit edilir. Silinen bu dosyanın içeriğinde şu ipucu yer almaktadır:

> "Şifre, Edinburgh'da yatan o gerçek ismin mezar taşındaki ölüm yılı."

---

### Adım 3: Tarihi Açık Kaynak İstihbaratı

İpucu, Harry Potter serisindeki Voldemort (Tom Riddle) karakterine ilham veren tarihi şahsiyete işaret etmektedir. Arama motorlarında *"Thomas Riddell grave Edinburgh death year"* şeklinde yapılan bir OSINT araştırmasıyla, mezarın Greyfriars Kirkyard'da bulunduğu ve ölüm yılının **1806** olduğu bilgisine ulaşılır. Bu, bir sonraki adımın parolasıdır.

---

### Adım 4: Steganografi Çözümü

Başlangıçta verilen `platform934.jpg` dosyasının içine gizlenmiş veriyi çıkarmak için **steghide** aracı kullanılır. Terminal üzerinden aşağıdaki komut çalıştırılır ve şifre olarak `1806` girilir:

```bash
steghide extract -sf platform934.jpg
```

İşlem sonucunda, resmin içine gömülü olan `marauder.pcap` isimli ağ trafiği (packet capture) dosyası elde edilir.

---

### Adım 5: PCAP (Ağ Trafiği) Analizi

`marauder.pcap` dosyası Wireshark ile incelendiğinde, içerisinde çok sayıda DNS ve TCP paketinden oluşan bir gürültü (noise) trafiği olduğu görülür. Trafiği anlamlandırmak için filtre çubuğuna `http` yazılır.

Elde edilen sınırlı sayıdaki HTTP istekleri incelendiğinde, 7. sıradaki paketin `http://ministry-of-magic-api.local/auth` adresine bir GET isteği yaptığı fark edilir. Paketin detaylarında `"Authorization"` başlığı altında bir JSON Web Token (JWT) taşındığı tespit edilir.

---

### Adım 6: JSON Web Token (JWT) Dekodlama

Kopyalanan JWT, jwt.io aracı veya yerel bir base64 decode komutu ile çözümlendiğinde Payload kısmında şu verilere ulaşılır:

```json
{
  "agent": "padfoot",
  "target_location_id": "ChIJtaE4NcmzjkgR5z8-41V_s_c",
  "message": "Haritayı oraya bıraktım, Google Maps yorumlarına bak."
}
```

---

### Adım 7: Geolocation ve Place ID OSINT'i

Token içindeki `target_location_id` değeri, Google Haritalar API'sine ait eşsiz bir "Place ID"dir. Bu kod, "Google Maps Place ID Finder" aracı ile sorgulandığında hedef lokasyonun İskoçya'daki Glenfinnan Viaduct olduğu ortaya çıkar.

---

### Adım 8: Final - Google Haritalar Yorumları

Tespit edilen lokasyona Google Haritalar üzerinden gidilerek, token'daki ipucu doğrultusunda mekanın yorumları **"En Yeni" (Newest)** seçeneğine göre sıralanır.

Remus Lupin isimli kullanıcı tarafından bırakılan güncel yorumun içinde yarışma bayrağı (flag) bulunmaktadır:

**SKYDAYS{un1c0d3_t4gs_4nd_d34d_m3n_t4l3s}**
