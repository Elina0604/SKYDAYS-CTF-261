## SKYDAYS26 - FileVault

### Çözüm

1. **Kayıt Ol:**
   ```sh
   Standart hesap oluştur
   ```

2. **Zararlı Dosya Yükle:**
   ```text
    İzin verilmeyen dosya tiplerinden birini yükle
   ```

3. **Tmp Dosya Yolunu Keşfet:**
   ```text
    Zararlı dosya yükleme cevabından zararlı dosyayının /Storage/tmp/file_name altında saklandığını gör
   ```

4. **Dosya Yolu İsimlendirmesini Çöz:**
   ```text
    - İsimlendirmenin MD5 olduğunu 32 karakter HEX olmasından anla
    - Deneme yolu ile dosya adının MD5(userName_fileNameWithoutExtension) olduğunu anlar 
   ```

5. **API Yolu Keşfi:**
   ```text
    - FUZZ ile /storage/tmp/file_name ucunu keşfeder 
   ```

6. **POST Scripti:**
   ```text
    - Kullanıcı zararlı dosyaya istediği içeri yazıp sürekli yükleme isteği atan bir script yazar ve çalıştırır
   ```

7. **Run File Scripti:**
   ```text
    - Sürekli /storage/tmp/file_name ucuna istek atarak zararlı kodun sonucunu görür
   ```

8. **Çalıştırılacak Kodlar:**
   ```sh
    ls
    ls -R Storage
    ls -R Storage/VIP
    ls -R Storage/VIP/admin
    cat Storage/VIP/admin/flag.txt

    Flag içeriğinin şifreli olduğunu görür

    ls -R Logs
    cat Logs/logs.txt

    Flag içeriğinin nasıl şifrelendiğini ve araması gereken dosyanın ismini görür
   
    base64 FileVault.Server.dll
   ```

9. **FileVault.Server.dll dosyasını oluşturma (Windows):**
   ```sh
    $b64content = Get-Content "base64.txt" -Raw
    $cleanB64 = $b64content.Trim().Trim('"').Replace('\n', '').Replace("`r", "").Replace("`n", "").Replace(" ", "")

    try {
        [System.Convert]::FromBase64String($cleanB64) | Set-Content "FileVault.Server.dll" -Encoding Byte
        Write-Host "Başarılı! Dosya boyutu:" (Get-Item "FileVault.Server.dll").Length "byte"
    }
    catch {
        Write-Error "Hata: Base64 verisi hala geçersiz. Mesaj: $_"
    }
   ```

9. **FileVault.Server.dll dosyasını oluşturma (Linux):**
   ```sh
    
   ```

10. **FileVault.Server.dll dosyasını okuma:**
   ```sh
    - DnSpy ile FileVault.Server.dll içeriğine bakar
    - Helpers altında EncryptionHelper.cs içeriğini bulur
   ```

11. **Flag Decryption:**
   ```sh
    - EncryptionHelper.cs içeriğine bakarak UnlockVault ve DecryptWithAesGcm fonksiyonlarını yazar
    - logs.txt içeriğinde bulduğu parametreler ve şifreli flag içeriği ile kodu çalıştırarak flag içeriğine ulaşır
   ```
