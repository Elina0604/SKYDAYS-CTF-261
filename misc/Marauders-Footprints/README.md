# Marauder’s Footprints

**Etkinlik:** SkyDays CTF
**Kategori:** OSINT / Steganography / Network Analysis
**Bayrak (Flag):** `SKYDAYS{un1c0d3_t4gs_4nd_d34d_m3n_t4l3s}`

## Genel Bakış

Bu CTF sorusu, katılımcıların çoklu siber güvenlik disiplinlerindeki pratik bilgi ve analiz yeteneklerini entegre bir senaryo üzerinden test etmek amacıyla hazırlanmıştır. Soru çözümü; açık kaynak istihbaratı (OSINT), ağ trafiği analizi ve gizli veri yapılarını tanımlama (Steganografi) süreçlerinin ardışık olarak uygulanmasını gerektirir.

## Test Edilen Yetenekler ve Teknolojiler

Bu senaryo kapsamında katılımcılardan aşağıdaki alanlarda yetkinlik göstermeleri beklenmektedir:

* **Unicode Anomalileri ve Steganografi:** Metin içerisine gizlenmiş Zero-Width Character (ZWC) formatındaki binary verilerin tespiti ve çözümlenmesi.
* **Versiyon Kontrol İstihbaratı (Git OSINT):** Açık kaynaklı depolardaki (repository) silinmiş commit geçmişlerinin ve dosya izlerinin incelenmesi.
* **Tarihi ve Coğrafi OSINT:** Verilen metinsel ipuçlarının gerçek dünya verileriyle (tarihi kayıtlar, ölüm yılları) eşleştirilerek parola olarak kullanılması.
* **Veri Çıkarma (Data Extraction):** `steghide` aracı kullanılarak JPEG formatındaki görselin içerisine gömülmüş ağ trafiği dosyasının elde edilmesi.
* **PCAP Analizi:** Gürültülü (noise) ağ paketleri arasından spesifik HTTP isteklerinin filtrelenmesi ve içerik analizi.
* **Kriptografik Veri Okuma:** JSON Web Token (JWT) standartlarının anlaşılması ve Payload içerisindeki şifrelenmemiş verinin decode edilmesi.
* **Geolocation / API Verisi İşleme:** Elde edilen Google Maps "Place ID" parametresinin çözümlenerek doğru coğrafi konuma ulaşılması.

## Başlangıç Dosyaları

* `platform934.jpg`
* Açıklama Metni (İçerisinde veri gizlenmiş ZWC barındıran UTF-8 dizesi)

## Kurallar ve Uyarılar

* **Brute-Force Yasaktır:** Sorunun çözüm adımlarında yer alan hiçbir şifreleme veya kilit mekanizması için kaba kuvvet (brute-force) saldırısı yapılmasına gerek yoktur. Gerekli parolalar bir önceki adımın OSINT analizi ile elde edilebilir formattadır. Sunuculara veya hedef platformlara yönelik tarama araçları (dirb, hydra vb.) kullanmak diskalifiye sebebidir.
* Tüm adımlar standart analiz araçları (Wireshark, CyberChef, Git CLI vb.) kullanılarak veya özel Python scriptleri yazılarak çözülebilir.
