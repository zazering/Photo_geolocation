# Dockerfile
dockerfile_content = '''FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install poetry && \\
    poetry config virtualenvs.create false && \\
    poetry install --only=main --no-dev

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \\
    libpq5 \\
    libjpeg62-turbo \\
    libpng16-16 \\
    libwebp7 \\
    libtiff6 \\
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["python", "-m", "app.main"]
'''

with open("photo_geolocation/Dockerfile", "w") as f:
    f.write(dockerfile_content)

# docker-compose.yml
docker_compose_content = '''version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/geolocation
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=your-secret-key-here
    volumes:
      - ./uploads:/app/uploads
      - ./.env:/app/.env:ro
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=geolocation
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: photo-geolocation-network
'''

with open("photo_geolocation/docker-compose.yml", "w") as f:
    f.write(docker_compose_content)

print("✅ Docker конфигурация создана")