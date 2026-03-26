FROM node:18-slim

WORKDIR /app

# 1. Önce paket listelerini kopyala
COPY package*.json ./

# 2. Root olarak kurulumu yap (Hızlı olur)
RUN npm install

# 3. Tüm proje dosyalarını içeri al
COPY . .

# 4. KRİTİK ADIM: Klasörlerin sahipliğini 'node' kullanıcısına devret
# Bunu COPY . . komutundan SONRA yapmalısın ki içeri giren dosyalar da node'un olsun
RUN chown -R node:node /app

# 5. Artık root yetkisini bırakıp güvenli kullanıcıya geçiyoruz
USER node

EXPOSE 3000

CMD ["node", "server.js"]
