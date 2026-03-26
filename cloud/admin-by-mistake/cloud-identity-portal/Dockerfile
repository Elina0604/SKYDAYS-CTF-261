FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 myuser
RUN chown -R 1000:1000 /app
USER myuser

CMD ["python", "app.py"]
