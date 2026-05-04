FROM python:3.11-slim

RUN apt-get update && apt-get install -y nginx redis-server && apt-get clean

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -e .

COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 80

CMD service redis-server start && \
    celery -A src.zad1.tasks worker --loglevel=info -P solo & \
    gunicorn src.zad1.app:app --bind 127.0.0.1:5000 & \
    uvicorn src.zad2.main:app --host 127.0.0.1:8000 & \
    nginx -g "daemon off;"