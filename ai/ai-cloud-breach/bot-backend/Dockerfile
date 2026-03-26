# Hafif bir Python imajı kullanıyoruz
FROM python:3.9-slim

# Çalışma dizinini ayarlıyoruz
WORKDIR /app

# Önce gereksinimleri kopyalayıp kuruyoruz (Docker cache avantajı için)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Gunicorn'u imaja dahil ediyoruz (requirements.txt'de yoksa diye garantiye alıyoruz)
RUN pip install --no-cache-dir gunicorn

# Uygulama kodunu ve .env dosyasını kopyalıyoruz
COPY . .

# Uygulamanın çalışacağı portu açıyoruz
EXPOSE 8080

# Geliştirici sunucusu yerine Gunicorn'u 4 iş parçacığı ile başlatıyoruz
CMD ["gunicorn", "-w", "1", "--threads", "4", "--timeout", "120", "-b", "0.0.0.0:8080", "app:app"]
