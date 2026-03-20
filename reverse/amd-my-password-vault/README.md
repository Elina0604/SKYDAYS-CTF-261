# Password Vault

### Yarışmacıya Verilecek Dosyalar
    * /Executables altındaki dosya

### Soru Açıklaması
	* Windows'da çözülmesi tavsiye edilir

### Yarışmacıya Verilebilecek İpuçları
    * .exe içeriğine ulaşmak için SingleFileExtractor kullan (Maliyet: ~%35)
    * Elde ettiğin .dll dosyasını DnSpy ile incele (Maliyet: ~%35)

### Çözüm

	* Yarışmacı DIE ile .NET Framework olduğunu keşfeder
    * Yarışmacı SingleFileExtractor ile exe dosyasını açar
    * .Çıktılar arasından amd-my-password-vault.dll dosyasını DnSpy ile inceler
    * .exe içindeki "encryptedPassword" değişkenini ve kullanıcının girdiği şifre verisinin ToBase64 ile şifrelendiğini görür. (Compile/Decompile durumuna göre değişken olarak değil direk if koşulu içinde olabilir)
    * CyberChef'de FromBase64 ile "encryptedPassword" içeriğini çözer.
    * .exe'yi çalıştırıp FromBase64 çıktısını girerek flag'e ulaşır.
