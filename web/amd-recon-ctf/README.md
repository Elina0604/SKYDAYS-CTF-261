# Recon - CTF Challenge Dokumantasyonu

## 1. Soru Meta Verileri

**Soru Adi:** Recon

**Kategori:** Web

**Zorluk:** Easy

**Bayrak:** `SKYDAYS{e587-b32f-3b72}`

---

## 2. Çözüm Video
[Drive](https://drive.google.com/drive/folders/1UoWB8aE93xPvIwPt2QWSKykFjU_4g2FR?usp=sharing)

## 3. Çözüm

1. **What is the secret route?:**
   ```sh
   ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt -u https://recon.skydays.ctf/FUZZ -c -v
   ```

2. **What is the secret url?:**
   ```text
   ffuf sonucunda bulunan yola git ve ordan url'i al
   ```

3. **What is the secret minecraft players name?:**
   ```link
   - docker pull amahird/reckon-mock-backend:latest
   - Windows --> docker inspect amahird/reckon-mock-backend --format='{{json .Config.Env}}' | ConvertFrom-Json
   - Linux --> docker inspect amahird/reckon-mock-backend --format='{{json .Config.Env}}' | jq
   ```

4. **This player has a Youtube channel, when was this channel started?:**
   ```text
   Oyuncunun youtube kanalına giderek ayrıntılara bak
   ```
