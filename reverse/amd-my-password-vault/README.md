# Password Vault - CTF Challenge Dokumantasyonu

## 1. Soru Meta Verileri

**Soru Adi:** Password Vault

**Soru Aciklamasi:** Windows'da çözülmesi tavsiye edilir

**Kategori:** Reverse

**Zorluk:** Easy-Medium

**Bayrak:** `SKYDAYS{}`

---

## 2. Yarışmacıya Verilecek Dosyalar
    /Executables altındaki amd-my-password-vault.exe dosyası

## 3. Yarışmacıya Verilebilecek İpuçları
    * .exe içeriğine ulaşmak için SingleFileExtractor kullan (Maliyet: %35)
    * Elde ettiğin .dll dosyasını DnSpy ile incele (Maliyet: %30)

## 4. Çözüm
	* Video: Drive Linki eklenicek
	* Yarışmacı DIE ile .NET Framework olduğunu keşfeder
    * Yarışmacı SingleFileExtractor ile exe dosyasını açar
    * .Çıktılar arasından amd-my-password-vault.dll dosyasını DnSpy ile inceler
    * .exe içindeki "encryptedPassword" değişkenini ve kullanıcının girdiği şifre verisinin ToBase64 ile şifrelendiğini görür. (Compile/Decompile durumuna göre değişken olarak değil direk if koşulu içinde olabilir)
    * CyberChef'de FromBase64 ile "encryptedPassword" içeriğini çözer.
    * .exe'yi çalıştırıp FromBase64 çıktısını girerek flag'e ulaşır.