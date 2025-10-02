import os
from pathlib import Path

# Создаем полную структуру проекта
base_dir = Path("photo_geolocation")
base_dir.mkdir(exist_ok=True)

# Основные директории
dirs = [
    "app",
    "app/models",
    "app/services", 
    "app/api",
    "app/utils",
    "app/core",
    "tests",
    "tests/unit",
    "tests/integration", 
    "docker",
    "requirements",
    "docs",
    "scripts",
    "static",
    "templates",
    "uploads"
]

for dir_path in dirs:
    (base_dir / dir_path).mkdir(parents=True, exist_ok=True)

print("✅ Структура проекта создана")

# Создаем __init__.py файлы
init_files = [
    "app/__init__.py",
    "app/models/__init__.py", 
    "app/services/__init__.py",
    "app/api/__init__.py",
    "app/utils/__init__.py",
    "app/core/__init__.py",
    "tests/__init__.py",
    "tests/unit/__init__.py",
    "tests/integration/__init__.py"
]

for init_file in init_files:
    (base_dir / init_file).touch()

print("✅ __init__.py файлы созданы")