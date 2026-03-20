# Recon

### Çözüm

1. **Ana Sayfa'ya git:**
   ```sh
   http://recon.ctf
   ```

2. **Gobuster ile tara:**
   ```text
   /hitcount
   ```

3. **Secret URL'e git:**
   ```link
   https://hub.docker.com/r/amahird/reckon-mock-backend/tags
   ```

4. **Docker Image'i İncele:**
   ```text
   - "docker pull amahird/reckon-mock-backend:latest"
   - Windows: "docker inspect amahird/reckon-mock-backend --format='{{json .Config.Env}}' | ConvertFrom-Json"
   - Linux: "docker inspect amahird/reckon-mock-backend --format='{{json .Config.Env}}' | jq"
   ```

5. **Youtube Kanalını İncele:**
   ```sh
   February 8, 2014
   ```
