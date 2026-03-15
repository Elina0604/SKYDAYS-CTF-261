# Product Requirements Document (PRD)

## Proje Adı: Sky-Sec İç Ağ Envanter Sistemi (CTF Sorusu)

### 1. Proje Özeti ve Hedefi

Bu proje, orta seviye (Medium) zorlukta bir Capture The Flag (CTF) sorusudur. Yarışmacılara derlenmiş bir istemci (client binary) verilecektir. Bu istemci, uzak bir sunucudaki (TCP Socket) özel bir protokolle haberleşen "sınırlı bir kabuk" (limited-shell) aracıdır. **Hedef:** Yarışmacıların istemciyi tersine mühendislik (Reverse Engineering) ile analiz edip ağ protokolünü (şifreleme/kodlama) çözmeleri, ardından kendi scriptlerini yazarak sunucudaki gizli SQL Injection (SQLi) zafiyetini sömürmeleri ve veri tabanından "Bayrak" (Flag) bilgisini okumalarıdır.

### 2. Mimari ve Bileşenler

Sistem 3 ana bileşenden oluşacaktır:

1. **Veritabanı (MySQL):** Sunucu tarafında (tercihen bir Docker container içerisinde veya ayrı bir serviste) çalışacak, envanter verilerini ve gizli bayrağı tutacaktır. **ÖNEMLİ:** Yarışmacılara veritabanı şemasını içeren herhangi bir `.sql` dosyası veya veritabanı yedeği kesinlikle verilmeyecektir. Keşfi tamamen zafiyet üzerinden yapmaları gerekmektedir.
    
2. **Sunucu (Python TCP Socket Server):** İstemciden gelen özel formatlı TCP paketlerini alacak, çözecek, komutları ayrıştıracak ve MySQL veritabanında (kasten zafiyetli bir şekilde) çalıştırıp sonucu geri dönecek.
    
3. **İstemci (Golang CLI Binary):** Yarışmacılara verilecek olan tek araç. Kullanıcıdan komut alan, bu komutları şifreleyip sunucuya ileten "Limited-Shell" arayüzü.
    

### 3. Teknik Gereksinimler ve Geliştirme Talimatları (Agent İçin)

#### 3.1. Veritabanı Yapısı (MySQL)

Aşağıdaki tablolar sunucu başlatıldığında veya bir kurulum betiği ile MySQL sunucusunda oluşturulmalıdır.

- **Tablo 1: `inventory`**
    
    - `id` (INT AUTO_INCREMENT PRIMARY KEY)
        
    - `item_name` (VARCHAR(255))
        
    - `details` (TEXT)
        
    - `status` (VARCHAR(50)) - 'public' veya 'private'
        
    - _Örnek Veriler:_
        
        - (1, 'Router-A', 'Cisco 2901 - IP: 10.0.0.1', 'public')
            
        - (2, 'Switch-Core', 'HP ProCurve - IP: 10.0.0.2', 'public')
            
        - (3, 'Firewall-Ext', 'Palo Alto - IP: 192.168.1.1', 'private')
            
- **Tablo 2: `secret_vault`**
    
    - `id` (INT AUTO_INCREMENT PRIMARY KEY)
        
    - `vault_key` (VARCHAR(255))
        
    - `flag_value` (TEXT)
        
    - _Örnek Veri:_ (1, 'master_key', 'FLAG{SkyS3c_L3g4cy_Syst3ms_4r3_D4ng3r0us}')
        

#### 3.2. Ağ Protokolü ve Kriptografi (ÖNEMLİ)

Sunucu ve istemci doğrudan düz metin (plaintext) konuşmayacaktır. İletişim aşağıdaki kurallara göre yapılmalıdır:

- **İşlem Sırası:** Mesaj -> XOR (Key: `SkY_S3c_P4ssW0rd_99`) -> Base64 Encode.
    
- **Paket Formatı:** Giden veri her zaman `\n` (newline) karakteri ile bitmelidir.
    
- _Not:_ Bu basit şifreleme, yarışmacının binary dosyasını decompile edip XOR anahtarını ve Base64 kullanıldığını bulması içindir.
    

#### 3.3. İstemci (Client - Golang)

- Komut satırı argümanı olarak IP ve Port almalıdır (`./skysec_client -h 127.0.0.1 -p 1337`).
    
- Bağlandıktan sonra kullanıcıya `EMS>` (Evidence Management System) promptu göstermelidir.
    
- Kullanıcının girdiği her metni 3.2'deki protokole göre şifreleyip TCP üzerinden göndermeli ve gelen cevabı çözüp ekrana basmalıdır.
    
- İçerisinde `SkY_S3c_P4ssW0rd_99` XOR anahtarı hardcoded (gömülü) olmalıdır.
    

#### 3.4. Sunucu (Server - Python TCP)

- Belirtilen portta (örn: 1337) dinlemelidir.
    
- Gelen Base64/XOR veriyi çözmeli, komutu okumalıdır.
    
- Desteklenen Komutlar:
    
    - `help`: Kullanılabilir komutları döner (`list`, `read <id>`, `whoami`).
        
    - `whoami`: `Current User: Guest (Privilege Level: 0)` döner.
        
    - `list`: `SELECT id, item_name FROM inventory WHERE status = 'public'` sorgusunu (güvenli bir şekilde) MySQL'de çalıştırır ve döner.
        
    - `read <id>`: **(ZAFİYET BURADA OLMALIDIR)**
        
- **ZAFİYET TASARIMI (AI DİKKATİNE):**
    
    - `read` komutundan sonra gelen `<id>` parametresi, MySQL sorgusuna **string birleştirme (concatenation)**yöntemiyle kasten güvensiz olarak eklenmelidir.
        
    - _Örnek Kötü Kod:_ `query = f"SELECT details FROM inventory WHERE id = '{user_input}' AND status = 'public'"`
        
    - **KESİNLİKLE** prepared statements (parametre bağlama) KULLANILMAMALIDIR.
        
- **WAF (Web Application Firewall) / Filtreleme:**
    
    - Zorluğu artırmak için sunucuya basit bir filtre eklenmelidir. Eğer `user_input` içinde şu karakterler/kelimeler varsa sunucu `EMS Error: Invalid characters detected in ID.` dönmelidir:
        
        - Boşluk karakteri (  ) (Bypass için `/**/` kullanılacak)
            
        - Büyük/küçük harf duyarsız (case-insensitive) olarak: `UNION`, `SELECT` kelimelerinin direkt kullanımı engellenebilir.
            
        - Bu projede **boşluk karakterini** ve **UNION** kelimesini tamamen engelleyin. Yarışmacı Boolean-Based Blind SQLi yapmak zorunda kalsın: (Örnek bypass: `1'/**/OR/**/(istediği_sorgu)/**/OR/**/'0`)
            
    - Eğer MySQL veritabanı syntax hatası verirse, kasten şu mesajı dönmelidir: `EMS Error: Internal processing failure (Code: 1064)` (1064, MySQL syntax hata kodudur. Bu, yarışmacıya arkada MySQL çalıştığının net bir ipucunu verecektir).
        

### 4. Çözüm Yolu (Intended Path)

Agent'ın sistemi doğru kurduğundan emin olmak için test edilecek çözüm senaryosu:

1. Yarışmacı `skysec_client` binary'sini alır, Ghidra/IDA ile inceler.
    
2. XOR anahtarını (`SkY_S3c_P4ssW0rd_99`) ve Base64 işlemini fark eder.
    
3. Python ile kendi istemcisini (TCP socket scripti) yazar.
    
4. `read 1'` komutunu yolladığında `Code: 1064` hatasını görür.
    
5. Boşlukların filtrelendiğini fark edip `read 1'/**/OR/**/(version())/**/OR/**/'0` gibi bir payload dener.
    
6. Kendi scriptini bir MySQL Blind SQLi scriptine dönüştürür. `secret_vault` tablosunu bulur ve `flag_value` sütununu karakter karakter (SUBSTRING ve ASCII fonksiyonları kullanarak) çeker.
    

### 5. Dizin Yapısı (Beklenen Çıktı)

Ajanın aşağıdaki yapıyı oluşturması beklenmektedir:

```
/skysec_ctf
├── server/
│   ├── requirements.txt
│   ├── server.py (TCP ve MySQL mantığı, WAF kuralları)
│   ├── setup_db.py (MySQL tablolarını oluşturan gizli betik)
│   └── docker-compose.yml (MySQL ve Server'ı kolayca ayağa kaldırmak için)
├── client/
│   ├── main.go (Golang CLI kodu)
│   └── go.mod
└── solution/
    └── solver.py (Zafiyeti çözen ve bayrağı alan örnek python scripti)

```

### 6. Kodlama Standartları

- Tüm kodlar temiz, yorum satırlı (Turkish/English) olmalıdır.
    
- Zafiyetli kısımlara kasten yapıldığına dair yorumlar eklenmelidir (`# INTENTIONAL VULNERABILITY`).
    
- Yarışmacılara verilecek dizin sadece "client" dizinindeki derlenmiş binary olmalıdır. Veritabanı dosyaları ve sunucu kodları asla dışarı sızmamalıdır.
