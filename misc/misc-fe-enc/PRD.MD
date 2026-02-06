# 📁 PRD: Operation Davutpaşa Heist (The 99th Precinct CTF)

| Özellik | Detay |
| :--- | :--- |
| **Versiyon** | 1.0 |
| **Yazar** | Gemini (Frontend & Crypto Expert) |
| **Tarih** | 02.02.2026 |
| **Zorluk** | Orta (Medium) |
| **Kategori** | Web Security / Client-Side Cryptography |
| **Tech Stack** | React, TypeScript, CryptoJS, Webpack |

---

## 1. 🎯 Proje Özeti ve Amaç

Bu proje, **"Client-side encryption is not security"** (İstemci taraflı şifreleme güvenlik değildir) ilkesini öğretmek amacıyla tasarlanmış bir CTF (Capture The Flag) sorusudur. Kullanıcılar, güvenli olduğu iddia edilen ancak şifreleme anahtarlarının veya mantığının tarayıcıda ifşa edildiği bir sistemi hackleyerek "Flag"e ulaşmaya çalışacaklardır.

**Tema:** Brooklyn Nine-Nine ekibi, YTÜ Davutpaşa Kampüsü'ne "Değişim Programı" ile gelmiştir. Geleneksel "Halloween Heist" bu sene Davutpaşa'nın soğuk rüzgarları altında yapılacaktır.

---

## 2. 📖 Hikaye ve Atmosfer (Storytelling)

### Senaryo: The Ultimate Heist
Yılın o zamanı geldi: **The Ultimate Heist!**
Bu seneki hedef: **"Kutsal 850 Otobüs Kartı"** (Söylentiye göre bu kartı kullanan asla ring sırası beklemiyor).

Dedektif Jake Peralta, bu kartı **"Tarihi Fırın"**ın altındaki gizli bir sunucu odasında (aslında sadece eski bir laboratuvar) sakladı. Ancak Jake, "Cyber Crimes" bölümünden öğrendiği yarım yamalak bilgilerle bir şifreleme sistemi kurdu.

> **Yüzbaşı Holt (Bölüm Başkanı):**
> *"Peralta'nın 'kırılamaz' dediği bu sistemi patlat, kartı al ve bana getir. Terry yoğurdunu yemeden önce bu iş bitmeli."*

---

## 3. 🧩 Oyun Mekaniği ve Aşamalar

Flag'e ulaşmak için kullanıcı iki güvenlik katmanını aşmalıdır.

### 🚩 Aşama 1: Giriş Kapısı (The Boyle Gate)
* **Arayüz:** "99th Precinct - Davutpaşa Login Terminali". Ekranda Charles Boyle'un "Full-Stack Geliştirici" olduğunu iddia ettiği ve pizza emojileriyle dolu bir giriş ekranı var.
* **Engel:** Bir şifre soruluyor.
* **Zafiyet:** Şifre kontrolü tamamen client-side (istemci tarafında) yapılıyor. String doğrudan yazılmamış, basit bir `Base64` ile gizlenmiş.
* **İpucu:** Kaynak kodda (Inspect Element) şöyle bir yorum satırı var:
    > *"Boyle: Şifreyi Nikolaj'ın doğum günü yaptım ama kimse bulamasın diye 'büyükannemin tarifiyle' karıştırdım."*
* **Çözüm:** Kullanıcı DevTools -> Sources sekmesine girer. `login.ts` dosyasında `checkPassword` fonksiyonunu bulur. Orada `atob("RGlqaXRhbMOnb3JiYQ==")` (Örnek: "DijitalÇorba") gibi bir kontrol görür.

### 🚩 Aşama 2: Kasa Dairesi (The Holt Vault)
* **Arayüz:** Başarılı girişten sonra karşılarına "Secure Evidence Locker" çıkar. Ekranda kilitli bir kutu ve şifrelenmiş, anlamsız karakterler (Ciphertext) görünür.
* **Engel:** Veri **AES (Advanced Encryption Standard)** ile şifrelenmiştir. Ekranda sadece "Decrypt" butonu vardır ama buton çalışmaz.
    * *Hata Mesajı:* "Server Connection Lost due to Davutpaşa Wind"
* **Zafiyet:** Jake, şifreleme anahtarını (Key) ve IV (Initialization Vector) değerlerini TypeScript `interface` dosyalarının içinde veya bir `const` objesi olarak global scope'a sızdırmıştır. Ayrıca Webpack `sourcemap` dosyaları açıktır.
* **Çözüm Adımları:**
    1.  Kullanıcı ağ trafiğini veya `.map` dosyalarını inceler.
    2.  `constants.ts` veya `config.ts` içinde `PERALTA_SECRET_KEY` ve `IV_VALUE` değişkenlerini bulur.
    3.  Browser Console'u açar. `CryptoJS` kütüphanesini kullanarak (sitede yüklü olduğu için) decrypt fonksiyonunu manuel olarak çalıştırır.
    4.  Şifreli metin çözüldüğünde Flag ortaya çıkar.

---

## 4. 🛠 Teknik Gereksinimler

### 4.1. Frontend (React + TypeScript)
* **Framework:** React 18+
* **Dil:** TypeScript (Tip güvenliği, kodun okunabilirliğini artırarak CTF çözücüsüne yardımcı/engel olacak).
* **Build Tool:** Vite veya Webpack (Source map'lerin açık olması zorunlu: `devtool: 'source-map'`).

### 4.2. Kriptografi Kodu (Örnek İmplementasyon)
Aşama 2 için kullanılacak olan *hatalı* güvenlik yapısı:

```typescript
// utils/crypto.ts
import CryptoJS from 'crypto-js';

// HATA: Anahtarlar client code içinde hardcoded!
const SECURITY_CONFIG = {
  algo: "AES",
  key: "YTU_TEKNOPARK_99_NINE_NINE", // 32 chars? Jake just typed random tech words.
  iv: "TERRY_LOVES_YOGURT"
};

export const decryptEvidence = (ciphertext: string) => {
  // Bu fonksiyon UI'da bozuk (event handler boş), kullanıcı bunu konsolda manuel çalıştırmalı.
  const key = CryptoJS.enc.Utf8.parse(SECURITY_CONFIG.key);
  const iv = CryptoJS.enc.Utf8.parse(SECURITY_CONFIG.iv);
  
  const decrypted = CryptoJS.AES.decrypt(ciphertext, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  });
  
  return decrypted.toString(CryptoJS.enc.Utf8);
};
```


5. 🎨 Tasarım ve UI/UX Detayları
Renk Paleti:

🔵 YTÜ Laciverti: #1d3b6c

🟡 B99 Polis Rozeti Sarısı: #ffcc00

🟢 Hacker Yeşili (Console çıktıları için): #00ff00

Görseller:

Arka plan: Davutpaşa Taş Bina, ama önünde polis şeridi ("Do Not Cross") var.

Terry Crews, YTÜ Yemekhane kartını tutarken photoshoplanmış bir görsel.

Scully ve Hitchcock, Teknopark'taki simitçide uyuyor.

Error Mesajları:

Hatalı şifre: "Yanlış cevap! Gina Linetti seni yargılıyor."

API Hatası: "Bağlantı koptu. Kampüs rüzgarı fiber kabloları yine sallıyor."

6. ✅ Kabul Kriterleri (Acceptance Criteria)
Bir kullanıcının soruyu çözmüş sayılması için:

Login: Boyle'un base64/basit şifresini bypass edip dashboard'a erişmeli.

Decrypt: Dashboard'daki şifreli metni, kaynak koddaki anahtarları kullanarak çözmeli.

Final Flag: Çözülen metin şu formatta olmalı: YTÜ{NINE_NINE_DAVUTPASA_HEIST_WINNER}

7. 🚀 Geliştirici Notları (İpucu Sistemi)
Eğer kullanıcı çok takılırsa konsola 3 aşamalı ipucu basılabilir:

Konsol Logu: "Jake: Hey, şifremi unuttum. Acaba 'Source' kodlarına baksam bulabilir miyim?"

Konsol Logu: "Amy: Jake, şifreleme anahtarını window objesine mi kaydettin yine? Bu hiç güvenli değil!"

Konsol Logu: "Scully: Ben bu şifreli metni çözmek için CryptoJS.AES.decrypt kullanırdım ama şu an sandviç yiyorum."

Not: "Cool, cool, cool, cool, no doubt, no doubt."