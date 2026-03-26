## Soru Özeti

*   **Giriş Noktası**: `cloud-webhook-invoker` (Bulut Webhook Uygulaması) üzerinde 80. port
*   **Zafiyet 1**: `X-Cloud-Metadata-Endpoint` HTTP başlığı üzerinden Bilgi İfşası.
*   **Zafiyet 2**: Dahili uç noktaları sızdıran, kısmi kimlik bilgileri sağlayan ve aynı zamanda derin şaşırtmaca (deep archive) servisleri içeren Simüle Edilmiş AWS IMDS.
*   **Zafiyet 3**: Dahili Redis yapılandırma dosyasını okumak için Apache 2.4.49 Dizin Atlatma (CVE-2021-41773).
*   **Zafiyet 4**: Redis sunucusunda kimlik doğrulaması yapmak ve kalan kimlik bilgilerini almak için CRLF injection (basit bir WAF'ı çift URL kodlaması ile atlayarak) aracılığıyla SSRF.
*   **Zafiyet 5**: Kasa'ya erişmek için başlık eklenmesine olanak tanıyan, URL ayrıştırıcısındaki CRLF injection aracılığıyla SSRF (`X-Vault-Access-Key` ve `X-Vault-Secret-Key`).
*   **Zafiyet 6**: Büyük bir AWS altyapı dökümü içinde derinlere gizlenmiş veritabanı uç noktasını (cloud-user-db) bulmak için sağlanan IV ve Key'i kullanarak, döndürülen AES-256-CBC Terraform State dosyasının şifresini çözmek.
*   **Zafiyet 7**: Hedeflenen `cloud-user-db` arama uç noktasında SQLite üzerinden UNION-based SQL enjeksiyonu.
*   **Zafiyet 8**: `cloud-identity-portal` arayüzü üzerinden "Cloud Access" parolasının homoglyph saldırı mantığına uygun (Kiril alfabesi harfleri ve görünmez boşluk) girilerek kimlik atlatılması.
*   **Hedef (Zafiyet 9)**: `cloud-k8s-api` servisi üzerinden Kubernetes RBAC (Role-Based Access Control) zafiyetini sömürerek yüksek ayrıcalıklara sahip rolebinding oluşturmak ve Terraform State dosyasını (bayrağı) okumak.

## Bayraklar (Flags)

*   `SKYDAYS{th3r35_n0_cl0ud_1ts_jU5t_50m30n3_eL5e5_c0mPUt3R_8a9b}`
