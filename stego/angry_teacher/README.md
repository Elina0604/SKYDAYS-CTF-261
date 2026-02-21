🎓 Operation: Final Grade Recovery 
"Client-side data leakage" ve "Steganography" tekniklerini kullanarak, bir görselin içine gizlenmiş sınav sonucuna ulaşma senaryosu.

📖 Hikaye
Yıldız Teknik Üniversitesi'nde final haftası bitmiş, herkes heyecanla sonuçları beklemektedir. Ancak bölümün en zor hocası, notları sisteme girmek yerine sınıfa bir mail atar:

"Notlarınızı merak ettiğinizi biliyorum. Ekli dosyaya final sonucunuzu bıraktım. Eğer dikkatli bir mühendis adayıysanız, o görselin içinde size bıraktığım ipuçlarını kullanarak sonucunuzu görebilirsiniz. Sırf işiniz kolaylaşsın diye bazı bilgileri görselin özelliklerine 'not' olarak iliştirdim. Ama biraz da olsa uğraşmanız için birini şifreledim. Çözemeyen dersten kalır."

Dersi geçip geçmediğiniz, hocanın attığı final_sonuclari.jpg dosyasının içinde bir yerlerde saklı.

🎯 Amaç
Bu challenge'da hocanın bıraktığı dijital izleri takip ederek üç katmanı aşmanız gerekiyor:

🚩 Aşama 1: Metadata Leakage (Özellikleri İncele)
Zafiyet: Hassas bilgilerin dosya metadatasında (Exif) açıkça bırakılması.
Yöntem: Görselin "Artist" ve "Comment" kısımlarını inceleme.
İpucu: Exiftool veya dosya özelliklerine sağ tıklayarak verilere ulaşılabilir.

🚩 Aşama 2: Base64 Decoding
Zafiyet: Zayıf şifreleme (Encoding vs Encryption).
Yöntem: Artist kısmında bulunan Base64 formatındaki metni (b3RhZ2lodW1heXVu) çözerek Steghide şifresine ulaşma.
Hedef: otagihumayun şifresini elde etmek.

🚩 Aşama 3: Extraction & Zip
Zafiyet: Dosya gizleme.
Yöntem: steghide ile dosyayı çıkartma ve yorum kısmında bulunan ZIP şifresini kullanma.
Anahtarlar:

Steghide Pass: Comment kısmındaki Base64 metni çözülerek bulunur.

ZIP Pass: Artist kısmında doğrudan yazan şifre.

🛠 Teknik Araçlar
Exiftool / Strings: Metadata analizi için.

Base64 Decoder: Şifreyi çözmek için.

Steghide: Görselin içindeki finalnotu.zip dosyasını çıkartmak için.

🚀 Başlangıç
final_sonuclari.jpg dosyasını indirin.

Metadata verilerini dökün: exiftool final_sonuclari.jpg

Bulduğunuz ipuçlarını kullanarak dosyaları ayıklayın!

🏆 Final Bayrağı (Flag)
Final flag formatı: SKYDAYS{y0u_p4ss3d_th3_3x4m}
