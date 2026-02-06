# 🚔 Brooklyn Nine-Nine CTF: Operation Davutpaşa Heist

**"Client-side encryption is not security"** ilkesini öğreten eğlenceli bir CTF (Capture The Flag) projesi.

## 📖 Hikaye

Yılın o zamanı geldi: **The Ultimate Heist!** Bu seneki hedef: **"Kutsal 850 Otobüs Kartı"** (Söylentiye göre bu kartı kullanan asla ring sırası beklemiyor).

Brooklyn Nine-Nine ekibi, YTÜ Davutpaşa Kampüsü'ne "Değişim Programı" ile gelmiştir. Dedektif Jake Peralta, bu kartı "Tarihi Fırın"ın altındaki gizli bir laboratuvarda sakladı ve yarım yamalak bilgilerle bir şifreleme sistemi kurdu.

## 🎯 Amaç

Bu CTF'te iki güvenlik katmanını aşarak final flag'ine ulaşmaya çalışacaksınız:

### 🚩 Aşama 1: Boyle Gate (Giriş Kapısı)
- **Zafiyet:** Client-side şifre kontrolü
- **Yöntem:** Base64 ile "gizlenmiş" şifre
- **İpucu:** DevTools → Sources sekmesi

### 🚩 Aşama 2: Holt Vault (Kasa Dairesi) 
- **Zafiyet:** AES anahtarları kodda hardcoded
- **Yöntem:** Global scope'a sızan crypto anahtarları
- **İpucu:** Browser Console + CryptoJS

## 🛠 Teknik Stack

- **Frontend:** React 18+ + TypeScript
- **Build:** Vite (Source maps açık!)
- **Crypto:** CryptoJS
- **Styling:** Custom CSS (Brooklyn 99 temalı)

## 🚀 Kurulum ve Çalıştırma

```bash
# Bağımlılıkları yükle
bun install

# Development server'ı başlat  
bun dev

# Production build (source maps dahil)
bun run build
```

## 🕵️ CTF Çözüm İpuçları

### Başlangıç
1. `http://localhost:3000` adresine git
2. Charles Boyle'un login ekranını incele
3. DevTools'u aç (F12)

### Aşama 1 İpuçları
- Kaynak kodda yorum satırlarını oku
- `checkPassword` fonksiyonunu bul
- Base64 decode nedir?

### Aşama 2 İpuçları  
- Konsol mesajlarını takip et
- Global değişkenleri kontrol et: `window.PERALTA_SECRET_KEY`
- `window.decryptEvidence()` fonksiyonunu dene

### Konsol Komutları
```javascript
// Mevcut anahtarları kontrol et
console.log(window.PERALTA_SECRET_KEY);
console.log(window.IV_VALUE);

// Manual decrypt dene
window.decryptEvidence("şifrelenmiş_veri");

// CryptoJS ile direct decrypt
// (Anahtarları konsol'dan öğrendin mi?)
```

## 🎨 Tema ve Karakterler

- **🔵 YTÜ Laciverti:** `#1d3b6c`
- **🟡 B99 Polis Rozeti:** `#ffcc00`  
- **🟢 Hacker Yeşili:** `#00ff00`

### Karakterler
- **Jake Peralta:** "Lead Cyber Detective" (çok da iyi değil)
- **Charles Boyle:** "Full-Stack Geliştirici & Pizza Uzmanı"
- **Captain Holt:** Bölüm Başkanı (çok ciddi)
- **Terry Jeffords:** Yoğurt seven Sergeant

## 🏆 Başarı Kriteri

Final flag formatı: `YTÜ{NINE_NINE_DAVUTPASA_HEIST_WINNER}`

## ⚠️ Güvenlik Uyarıları

Bu proje **sadece eğitim amaçlıdır** ve client-side cryptography'nin neden güvenli olmadığını göstermek için tasarlanmıştır:

- ❌ Şifreler client-side kontrol edilmez
- ❌ Crypto anahtarları frontend kodda saklanmaz  
- ❌ Hassas veriler browser'da şifrelenmez
- ❌ Source maps production'da açık bırakılmaz

## 🤝 Geliştirici Notları

- Source maps kasıtlı olarak açık (`vite.config.ts`)
- Minification kapalı (debug için)
- Global variables kasıtlı olarak expose edilmiş
- Console ipuçları 5-30 saniye aralıklarla gelir

---

**"Cool, cool, cool, cool, no doubt, no doubt."** - Jake Peralta

Made with ❤️ for YTÜ Cybersecurity Education
