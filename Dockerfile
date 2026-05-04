FROM python:3.11-slim

RUN apt-get update && apt-get install -y nginx redis-server && apt-get clean

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -e .

COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 80

CMD service redis-server start && \
    celery -A src.zad1.tasks worker --loglevel=info -P solo & \
    gunicorn --bind 0.0.0.0:5000 src.zad1.app:app & \
    uvicorn src.zad2.main:app --host 0.0.0.0 --port 8000 & \
    nginx -g "daemon off;"