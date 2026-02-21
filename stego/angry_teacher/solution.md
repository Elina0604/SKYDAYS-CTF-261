🕵️ Solution:  Final Grade Recovery
Bu döküman, "Kızgın Öğretmen" steganografi sorusunun adım adım çözümünü içermektedir.

🛠 Kullanılan Araçlar
exiftool (Metadata analizi)

base64 (Şifre çözme)

foremost veya binwalk (Dosya ayıklama)

steghide (Veri çıkartma)

unzip (Arşiv açma)

👣 Adım Adım Çözüm
1. Metadata Analizi
İlk olarak dosyanın genel özelliklerine ve içine hoca tarafından bırakılan notlara bakıyoruz:


exiftool final_sonuclari.jpg
Bulgular:

Artist: 1911

Comment: b3RhZ2lodW1heXVu

2. Şifre Çözme (Decoding)
Comment kısmındaki metnin Base64 formatında olduğu anlaşılıyor. Bu metni çözüyoruz:


echo "b3RhZ2lodW1heXVu" | base64 -d
Sonuç: otagihumayun

3. Dosya Ayıklama (Carving)
Dosyanın içinde başka bir veri gömülü olup olmadığını kontrol etmek için foremost kullanıyoruz:


foremost -i final_sonuclari.jpg
Bu işlem sonucunda output/jpg klasörü içinde iki adet görsel oluşuyor. İkinci görsel (00000159.jpg), asıl veriyi barındıran katmandır.

4. Steghide ile Veriyi Çıkartma
Ayıkladığımız ikinci görsel üzerinde, Base64 ile bulduğumuz şifreyi kullanarak gizli dosyayı çıkartıyoruz:


steghide extract -sf output/jpg/00000159.jpg
# Passphrase: otagihumayun
Sonuç: finalnotu.zip dosyası dışarı aktarıldı.

5. ZIP Kilidini Açma
Metadata'da Artist kısmında bulduğumuz 1911 bilgisini ZIP şifresi olarak deniyoruz:


unzip finalnotu.zip
# Password: 1911
6. Bayrağı Okuma
Son adımda ortaya çıkan metin dosyasını okuyoruz:


cat finalnotu.txt
Flag: SKYDAYS{y0u_p4ss3d_th3_3x4m}
