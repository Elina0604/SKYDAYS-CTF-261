### Yarışmacıya Verilecek Bilgiler/Dosyalar

    * /Executables altındaki 2 adet dosya

### Yarışmacıya Verilebilecek İpuçları
    * .exe içeriğine ulaşmak için SingleFileExtractor kullan (Maliyet: ~%10)
    * Elde ettiğin .dll dosyasını DnSpy ile incele (Maliyet: ~%10)

### Çözüm

	* Yarışmacı DIE ile .NET Framework olduğunu keşfeder
    * Yarışmacı SingleFileExtractor ile exe dosyasını açar
    * .Çıktılar arasından amd-my-password-vault.dll dosyasını DnSpy ile inceler
    * .exe içindeki "encryptedPassword" değişkenini ve kullanıcının girdiği şifre verisinin ToBase64 ile şifrelendiğini görür. (Compile/Decompile durumuna göre değişken olarak değil direk if koşulu içinde olabilir)
    * CyberChef'de FromBase64 ile "encryptedPassword" içeriğini çözer.
    * .exe'yi çalıştırıp FromBase64 çıktısını girerek flag'e ulaşır.
