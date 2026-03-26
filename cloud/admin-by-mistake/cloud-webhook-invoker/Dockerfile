FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/

RUN useradd -m appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 555 /app

USER appuser

EXPOSE 80

CMD ["python", "app.py"]
