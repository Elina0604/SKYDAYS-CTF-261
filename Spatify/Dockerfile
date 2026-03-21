# 1. Aşama: Temel İmajı Seçiyoruz
FROM node:18-slim

# 2. Aşama: Çalışma Klasörünü Belirliyoruz
WORKDIR /app

# 3. Aşama: Paket Listesini Kopyalıyoruz
COPY package*.json ./

# 4. Aşama: Modülleri Kuruyoruz
RUN npm install

# 5. Aşama: Tüm Kodlarımızı İçeri Alıyoruz
COPY . .

# 6. Aşama: Kapıyı Aralıyoruz
EXPOSE 3000

# 7. Aşama: Motoru Çalıştırıyoruz
CMD ["node", "server.js"]