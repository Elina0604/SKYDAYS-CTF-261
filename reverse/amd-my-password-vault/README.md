### Yarışmacıya Verilecek Bilgiler/Dosyalar

    * /Executables altındaki 2 adet dosya

### Yarışmacıya Verilebilecek İpuçları
    * exe tipini anlamak için DIE-engine'i binary ayarda kullan (Maliyet: ~%10)
    * exe içeriğine bakmak için ILSpy kullan (Maliyet: ~%20)

### Çözüm

    * Yarışmacı DIE-engine ile .exe'nin hangi C#/.Net ile yazıldığını öğrenir.
    * .Net için Reverse Engineering tool'u olan ILSpy'ı kullanarak .exe içeriğine bakar.
    * .exe içindeki "encryptedPassword" değişkenini ve kullanıcının girdiği şifre verisinin ToBase64 ile şifrelendiğini görür. (Compile/Decompile durumuna göre değişken olarak değil direk if koşulu içinde olabilir)
    * CyberChef'de FromBase64 ile "encryptedPassword" içeriğini çözer.
    * .exe'yi çalıştırıp FromBase64 çıktısını girerek flag'e ulaşır.
