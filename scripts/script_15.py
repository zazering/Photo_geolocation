# .env.example
env_example_content = '''# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/geolocation
# Alternative for development:
# DATABASE_URL=sqlite+aiosqlite:///./geolocation.db

# Redis Configuration  
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-super-secret-key-change-in-production

# Google Cloud Vision API
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json

# Google Maps API
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# LocationIQ API (Free tier: 5000 requests/day)
LOCATIONIQ_API_KEY=your-locationiq-api-key

# OpenCage Geocoding API (Free tier: 2500 requests/day)  
OPENCAGE_API_KEY=your-opencage-api-key

# Application Settings
DEBUG=false
HOST=0.0.0.0
PORT=8000
'''

with open("photo_geolocation/.env.example", "w") as f:
    f.write(env_example_content)

# Создаем nginx конфигурацию
nginx_content = '''events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    upstream app {
        server app:8000;
    }
    
    server {
        listen 80;
        server_name localhost;
        client_max_body_size 10M;
        
        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        location /static/ {
            proxy_pass http://app;
            expires 1d;
            add_header Cache-Control "public, immutable";
        }
    }
}
'''

Path("photo_geolocation/docker").mkdir(exist_ok=True)
with open("photo_geolocation/docker/nginx.conf", "w") as f:
    f.write(nginx_content)

print("✅ Конфигурационные файлы созданы")