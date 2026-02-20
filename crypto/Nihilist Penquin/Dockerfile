FROM python:3.11-slim

# Çalışma dizini
WORKDIR /app

# Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY app.py .
COPY templates ./templates
COPY static ./static

# Port
EXPOSE 8080

# Çalıştır
CMD ["python", "app.py"]
