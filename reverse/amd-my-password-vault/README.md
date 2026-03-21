# Password Vault - CTF Challenge Dokumantasyonu

## 1. Soru Meta Verileri

**Soru Adi:** Password Vault

**Soru Aciklamasi:** Windows'da çözülmesi tavsiye edilir

**Kategori:** Reverse

**Zorluk:** Easy-Medium

**Bayrak:** `SKYDAYS{5eluR-gnir3en1gn3-e5rev3R}`

---

## 2. Yarışmacıya Verilecek Dosyalar
    /Executables altındaki amd-my-password-vault.exe dosyası

## 3. Yarışmacıya Verilebilecek İpuçları
    * .exe içeriğine ulaşmak için SingleFileExtractor kullan (Maliyet: %35)
    * Elde ettiğin .dll dosyasını DnSpy ile incele (Maliyet: %30)

## 4. Çözüm Video
[Drive](https://drive.google.com/drive/folders/1UoWB8aE93xPvIwPt2QWSKykFjU_4g2FR?usp=sharing)

## 5. Çözüm
	* Video: https://drive.google.com/drive/folders/1UoWB8aE93xPvIwPt2QWSKykFjU_4g2FR?usp=sharing
	* Yarışmacı DIE ile .NET Framework olduğunu keşfeder
    * Yarışmacı SingleFileExtractor ile exe dosyasını açar
    * .Çıktılar arasından amd-my-password-vault.dll dosyasını DnSpy ile inceler
    * .exe içindeki "encryptedPassword" değişkenini ve kullanıcının girdiği şifre verisinin ToBase64 ile şifrelendiğini görür. (Compile/Decompile durumuna göre değişken olarak değil direk if koşulu içinde olabilir)
    * CyberChef'de FromBase64 ile "encryptedPassword" içeriğini çözer.
    * .exe'yi çalıştırıp FromBase64 çıktısını girerek flag'e ulaşır.
