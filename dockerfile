FROM python:3.10-slim

WORKDIR /app

# Skapa icke-root user för bättre säkerhet
RUN useradd --create-home appuser
COPY app.py .
# Om du lägger till externa libs: COPY requirements.txt . && pip install -r requirements.txt

RUN mkdir -p /data && chown appuser:appuser /data
USER appuser

CMD ["python", "app.py"]
