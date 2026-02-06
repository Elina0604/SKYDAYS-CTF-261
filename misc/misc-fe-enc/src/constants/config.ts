// Charles Boyle'un "güvenli" login sistemi
export const LOGIN_CONFIG = {
  // Boyle: "Şifreyi çok gizli tuttum, kimse tahmin edemez."
  encodedPassword: "RGlqaXRhbENvcmJh"
};

// Brooklyn 99 karakterleri ve mesajları
export const CHARACTERS = {
  BOYLE: {
    name: "Charles Boyle",
    title: "Full-Stack Geliştirici & Pizza Uzmanı 🍕",
    quote: "Bu sistemin güvenliği pizza hamuru gibi katmanlı!"
  },
  JAKE: {
    name: "Jake Peralta",
    title: "Lead Cyber Detective",
    quote: "Cool, cool, cool, cool, no doubt, no doubt."
  },
  HOLT: {
    name: "Captain Raymond Holt",
    title: "Bölüm Başkanı",
    quote: "Peralta'nın 'kırılamaz' dediği bu sistemi patlat, kartı al ve bana getir."
  },
  TERRY: {
    name: "Terry Jeffords",
    title: "Sergeant",
    quote: "Terry yoğurdunu yemeden önce bu iş bitmeli!"
  }
};

// Error mesajları
export const ERROR_MESSAGES = {
  WRONG_PASSWORD: "❌ Yanlış cevap! Gina Linetti seni yargılıyor.",
  CONNECTION_ERROR: "📡 Bağlantı koptu. Kampüs rüzgarı fiber kabloları yine sallıyor.",
  DECRYPT_ERROR: "🔒 Server Connection Lost due to Davutpaşa Wind"
};

// Not: Final flag bu dosyada plaintext olarak bulunmaz!
// Sadece şifrelenmiş hali crypto.ts'de mevcuttur.

// YTÜ & Brooklyn 99 tema renkleri
export const THEME_COLORS = {
  YTU_NAVY: "#1d3b6c",
  B99_GOLD: "#ffcc00", 
  HACKER_GREEN: "#00ff00",
  ERROR_RED: "#ff4757",
  SUCCESS_GREEN: "#2ed573"
};