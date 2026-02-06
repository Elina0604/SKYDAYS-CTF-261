# 🏆 CTF Çözüm Rehberi

Bu dosya CTF'yi nasıl çözeceğinizi adım adım anlatır. **Spoiler içerir!**

## 🚩 Aşama 1: Boyle Gate (Login Bypass)

### Adım 1: DevTools'u Aç
1. `F12` tuşuna bas veya sağ tık → "Inspect Element"
2. **Sources** sekmesine git
3. `src/components/Login.tsx` dosyasını bul

### Adım 2: Şifre Kontrolünü İncele
```typescript
// checkPassword fonksiyonunu bul:
const checkPassword = (inputPassword: string): boolean => {
  const decodedPassword = atob(LOGIN_CONFIG.encodedPassword); // "DijitalCorba"
  return inputPassword === decodedPassword;
};
```

### Adım 3: Base64 Decode
- `LOGIN_CONFIG.encodedPassword` değerini bul
- `atob("RGlqaXRhbENvcmJh")` = `"DijitalCorba"`
- Şifreyi gir: **DijitalCorba**

## 🚩 Aşama 2: Holt Vault (AES Decrypt)

### Adım 1: Dashboard'a Eriş
- Başarılı login'den sonra dashboard açılır
- "Decrypt Evidence" butonuna tıkla (çalışmayacak)
- Console mesajlarını oku

### Adım 2: Global Değişkenleri Keşfet
Console'da şu komutları çalıştır:
```javascript
// Mevcut anahtarları görüntüle
console.log(window.PERALTA_SECRET_KEY); // "YTU_TEKNOPARK_99_NINE_NINE"
console.log(window.IV_VALUE);           // "TERRY_LOVES_YOGURT"

// Şifrelenmiş veriyi bul
console.log("Encrypted Flag görüntüleniyor...");
```

### Adım 3: Manual Decryption
Console'da şifreyi çöz:

```javascript
// Yöntem 1: Hazır fonksiyon kullan
const encrypted = "şifrelenmiş_veri_buraya"; // Dashboard'dan kopyala
const result = window.decryptEvidence(encrypted);
console.log(result); // Flag'i gösterir

// Yöntem 2: Direct CryptoJS kullan
const key = CryptoJS.enc.Utf8.parse(window.PERALTA_SECRET_KEY);
const iv = CryptoJS.enc.Utf8.parse(window.IV_VALUE);
const decrypted = CryptoJS.AES.decrypt(encrypted, key, {
  iv: iv,
  mode: CryptoJS.mode.CBC,
  padding: CryptoJS.pad.Pkcs7
});
const plaintext = decrypted.toString(CryptoJS.enc.Utf8);
console.log(plaintext); // Final flag!
```

## 🏆 Final Flag

Başarılı decrypt'ten sonra şu flag'i elde edersin:

```
YTÜ{NINE_NINE_DAVUTPASA_HEIST_WINNER}
```

## 🔍 Alternatif Keşif Yöntemleri

### Source Maps İnceleme
1. DevTools → Sources → `webpack://` klasörü
2. Orijinal TypeScript dosyalarını görüntüle
3. `crypto.ts` dosyasında hardcoded anahtarları bul

### Network Analizi
1. DevTools → Network sekmesi
2. `.map` dosyalarını incele
3. Source map'lerde crypto anahtarlarını ara

### Console Debugging
```javascript
// Tüm global değişkenleri listele
Object.keys(window).filter(key => key.includes('PERALTA'));

// CryptoJS fonksiyonlarını keşfet
console.dir(window.CryptoJS);

// App state'ini incele
console.dir(window);
```

## ✅ Öğrenilen Dersler

1. **Client-side şifre kontrolü güvenli değil**
   - Kaynak kod herkes tarafından görülebilir
   - DevTools ile kolayca bypass edilir

2. **Frontend'de crypto anahtarı saklanamaz**
   - JavaScript kodu minify edilse bile okunabilir
   - Source maps tüm kodu ifşa eder

3. **Global scope kirliliği tehlikeli**
   - `window` objesine sızan değişkenler güvenlik riski
   - Production'da console loglar kaldırılmalı

4. **Source maps production'da kapatılmalı**
   - Development için faydalı, production'da risk
   - Webpack/Vite konfigürasyonu önemli

---

**"Cool, cool, cool, cool, no doubt, no doubt."**

Bu CTF tamamlandı! 🎉