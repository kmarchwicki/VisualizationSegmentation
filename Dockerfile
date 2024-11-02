FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y redis-server

COPY scripts/redis_start.sh /app/redis_start.sh

RUN chmod +x /app/redis_start.sh

EXPOSE 6379

CMD ["sh", "redis_start.sh"]