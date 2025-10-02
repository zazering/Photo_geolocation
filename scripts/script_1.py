# pyproject.toml - современный конфиг для Python проекта
pyproject_content = '''[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "photo-geolocation"
version = "1.0.0"
description = "AI-powered photo geolocation service using landmark detection and geocoding"
authors = ["Hackathon Team <team@example.com>"]
license = "MIT"
readme = "README.md"
homepage = "https://github.com/username/photo-geolocation"
repository = "https://github.com/username/photo-geolocation"
keywords = ["geolocation", "ai", "computer-vision", "fastapi", "hackathon"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.1"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
pydantic = "^2.5.0"
sqlalchemy = "^2.0.23"
alembic = "^1.13.0"
asyncpg = "^0.29.0"
redis = "^5.0.1"
pillow = "^10.1.0"
google-cloud-vision = "^3.4.5"
googlemaps = "^4.10.0"
geopy = "^2.4.1"
httpx = "^0.25.2"
aiofiles = "^23.2.0"
python-multipart = "^0.0.6"
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
celery = "^5.3.4"
prometheus-client = "^0.19.0"
structlog = "^23.2.0"
pydantic-settings = "^2.1.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.3"
pytest-asyncio = "^0.21.1"
pytest-cov = "^4.1.0"
black = "^23.11.0"
isort = "^5.12.0"
flake8 = "^6.1.0"
mypy = "^1.7.1"
pre-commit = "^3.6.0"
httpx = "^0.25.2"

[tool.black]
line-length = 88
target-version = ['py311']
include = '\\.pyi?$'

[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
'''

with open("photo_geolocation/pyproject.toml", "w") as f:
    f.write(pyproject_content)

print("✅ pyproject.toml создан")