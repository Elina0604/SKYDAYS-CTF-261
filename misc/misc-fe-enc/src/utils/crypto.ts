import CryptoJS from 'crypto-js';

// Jake Peralta'nın güvenlik sistemi
const SECURITY_CONFIG = {
  algo: "AES",
  key: "YTU_TEKNOPARK_99_NINE_NINE",
  iv: "TERRY_LOVES_YOGURT"
};

export const decryptEvidence = (ciphertext: string) => {
  try {
    const key = CryptoJS.enc.Utf8.parse(SECURITY_CONFIG.key);
    const iv = CryptoJS.enc.Utf8.parse(SECURITY_CONFIG.iv);
    
    const decrypted = CryptoJS.AES.decrypt(ciphertext, key, {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });
    
    const result = decrypted.toString(CryptoJS.enc.Utf8);
    
    // Flag doğru decrypt edildiyse özel mesaj göster
    if (result && result.includes("SKYDAYS{") && result.includes("SIFRELENMIS_KASA_NINE")) {
      console.log("🎉 HEIST SUCCESSFUL!");
      console.log("🏆 Flag: " + result);
      console.log("✅ Tebrikler! 850 otobüs kartını başarıyla ele geçirdin!");
      console.log("🚔 Nine-Nine!");
    }
    
    return result;
  } catch (error) {
    console.error('Decryption failed:', error);
    return '';
  }
};

export const ENCRYPTED_FLAG = "0zhFrJXRebjn/KokmYkHy+47g4g/RSkv5Js6ul+NkYaxn4P75ymvsWdelFkj26YP";

// Console mesajları
export const logHints = () => {
  setTimeout(() => {
    console.log("🔍 Jake: Hmm, sistem biraz yavaş çalışıyor bugün.");
  }, 8000);
  
  setTimeout(() => {
    console.log("👩‍💻 Amy: Jake, kodunda bir şeyler eksik gibi görünüyor.");
  }, 20000);
};

// Global scope'a sızıran "hata"
if (typeof window !== 'undefined') {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (window as any).PERALTA_SECRET_KEY = SECURITY_CONFIG.key;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (window as any).IV_VALUE = SECURITY_CONFIG.iv;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (window as any).decryptEvidence = decryptEvidence;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (window as any).CryptoJS = CryptoJS;
}