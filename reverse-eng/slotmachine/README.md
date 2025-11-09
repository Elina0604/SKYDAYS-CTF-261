# 🎰 Hilekârın Slot Makinesi

Hoş geldin! Bu makinede gerçek şans, zeka ve biraz da "hile" birleşiyor.  

---

## Görev

Başlangıç bakiyen: **100$**  
Hedefin: **1000$'a ulaşmak**  
Ama herkes şanslı olamaz... Gerçek kazananlar, sistemin sırrını çözenlerdir.

---

## Oynanış

1. `slot.py` dosyasını yerel makinede çalıştır.
2. **Kullanıcı kodu**: İstediğin herhangi bir string gir.
3. Her turda **1-10$** arasında bahis yapabilirsin.
4. Slot makinesi senin girdiğin koda göre tamamen **deterministik** çalışır!
5. Eğer 1000$ bakiyeye ulaşırsan, flag'e de ulaşırsın.

---

## İpuçları & Notlar

- Şansına güvenerek oynayabilir veya kodu inceleyip *gerçek hileyi* keşfedebilirsin.
- Kasanın kilidini açmak için algoritmanın püf noktasını bulman gerekecek...

İyi şanslar!

## Çözüm (Açık Writeup)

### 1. Kodun sırrı nedir?

- Oyunda girilen "kullanıcı kodu" (herhangi bir string), karakterlerinin ASCII değerlerinin toplamı alınarak bir sayıya dönüştürülüyor.
- Bu toplam, 256'ya bölünüp kalan (mod 256) alınıyor ve `random.seed()` fonksiyonu ile Python'un rastgele sayı üreticisine "tohum" olarak veriliyor.
- Yani, aynı kullanıcı kodunu giren herkes için aynı oyun sonuçları oluşur. Bu da algoritmayı tamamen deterministik yapıyor.

### 2. Nasıl çözülür, hangi adımları uygulamalı?

- **Çözüm 1:** Kodda geçen seed algoritmasını anlayan bir script ile (veya elle) bir seed bulabilirsiniz ki, bu seed sayesinde slotta arka arkaya jackpot yapıp kısa sürede $1000'a ulaşırsınız.
- **Çözüm 2:** ASCII toplamı belirli bir seed üretecek şekilde basit bir string oluşturarsınız. Örneğin, bir seed direkt olarak `"A"` (ASCII 65) veya `"AZ"` (65+90=155) gibi.

#### **En hızlı çözüm yöntemi:**
Aşağıdaki örnek kodu, slot makinesinin algoritmasına göre kolayca jackpot yapan bir "kullanıcı kodu" bulmak için kullanabilirsiniz:

```python
import random

def test_seed(seed_degeri):
    bakiye = 100
    random.seed(seed_degeri)
    for t in range(100):
        bahis = 10  # maksimum bahis
        bakiye -= bahis
        sonuclar = [random.randint(1, 9) for _ in range(3)]
        if sonuclar == [7, 7, 7]:
            bakiye += bahis * 100
        elif sonuclar[0] == sonuclar[1] or sonuclar[1] == sonuclar[2]:
            bakiye += bahis * 2
        if bakiye >= 1000:
            return True
    return False

for seed in range(256):
    if test_seed(seed):
        print("Kazanan seed:", seed)
        break
```

> Örneğin kodun çıktısı `Kazanan seed: 47` ise, ASCII toplamı **47** olan bir kullanıcı kodu girerek flag'ı alabilirsin.  
> Örnek kullanıcı kodu: `'/'` (ASCII 47), `'AB'` (65+66=131; yani seed değeri 131), veya kendi hesapladığın başka kombinasyon.

### 3. Son adımlar

- Slot.py'yi aç ve kullanıcı kodu kısmına bulduğun seed'i getirecek bir karakter dizisi gir.
- Maksimum bahislerle oyna (hızlıca ilerlersin).
- $1000’a ulaşınca flag ekranda gösterilecek!

---
