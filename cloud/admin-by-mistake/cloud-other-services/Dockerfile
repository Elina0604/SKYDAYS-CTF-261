FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y redis-server curl && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 myuser
RUN chown -R myuser:myuser /app
RUN chmod 777 /app

USER myuser

CMD ["./start.sh"]
