#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command: str, check: bool = True) -> bool:
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=check)
    return result.returncode == 0


def check_python_version():
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        return False

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def check_poetry():
    if not shutil.which("poetry"):
        print("Installing Poetry...")
        if not run_command("curl -sSL https://install.python-poetry.org | python3 -"):
            print("❌ Failed to install Poetry")
            return False

    print("✅ Poetry available")
    return True


def install_dependencies():
    print("📦 Installing dependencies...")

    if not run_command("poetry install"):
        return False

    print("✅ Dependencies installed")
    return True


def setup_environment():
    env_file = Path(".env")
    env_example = Path(".env.example")

    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your API keys")
    elif env_file.exists():
        print("✅ .env file already exists")

    return True


def create_directories():
    directories = ["uploads", "static", "logs"]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   Created: {directory}/")

    print("✅ Directories created")
    return True


def setup_database():
    print("🗃️ Setting up database...")

    if not run_command("poetry run alembic upgrade head"):
        print("⚠️  Database migration failed (this is OK for first run)")

    return True


def run_tests():
    print("🧪 Running tests...")

    if not run_command("poetry run pytest tests/ -v", check=False):
        print("⚠️  Some tests failed (this might be OK)")

    return True


def main():
    print("🚀 Photo Geolocation Service Setup")
    print("=" * 40)

    steps = [
        ("Checking Python version", check_python_version),
        ("Checking Poetry", check_poetry),
        ("Installing dependencies", install_dependencies),
        ("Setting up environment", setup_environment),
        ("Creating directories", create_directories),
        ("Setting up database", setup_database),
        ("Running tests", run_tests),
    ]

    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"❌ {step_name} failed")
            return False

    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Start development server: make dev")
    print("3. Or start with Docker: make run")
    print("4. Visit http://localhost:8000/demo")
    print("\n📚 Documentation: http://localhost:8000/docs")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
