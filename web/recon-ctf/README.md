# SKYDAYS26 - Recon CTF

## Kurulum

1. **Klasöre Gir:**
   ```sh
   cd recon-ctf 
   ```

2. **Ayağa Kaldır:**
   ```sh
   docker compose up --build -d
   ```

## Çözüm

1. **Ana Sayfa'ya git:**
   ```sh
   http://recon.ctf
   ```

2. **Gobuster ile tara:**
   ```text
   /657768-rules
   ```

3. **ASCII tablosuna kullanarak çöz:**
   ```text
   AMD
   ```

5. **Secret URL'e git:**
   ```link
   https://hub.docker.com/r/amahird/reckon-mock-backend/tags
   ```

6. **Docker Image'i İncele:**
   ```text
   - "docker pull amahird/reckon-mock-backend:latest"
   - Windows: "docker inspect amahird/reckon-mock-backend --format='{{json .Config.Env}}' | ConvertFrom-Json"
   - Linux: "docker inspect amahird/reckon-mock-backend --format='{{json .Config.Env}}' | jq"
   ```

7. **Youtube Kanalını İncele:**
   ```sh
   February 8, 2014
   ```
