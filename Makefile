SHELL := /bin/bash
.PHONY: help install dev test clean build run docker-up docker-down lint format

help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies with Poetry"
	@echo "  dev         - Run development server"
	@echo "  test        - Run tests with coverage"
	@echo "  clean       - Clean cache and temporary files"
	@echo "  build       - Build Docker image"
	@echo "  run         - Run with Docker Compose"
	@echo "  docker-up   - Start all services"
	@echo "  docker-down - Stop all services"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"

install:
	poetry install
	poetry run pre-commit install

dev:
	poetry run python -m app.main

test:
	poetry run pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf uploads/*.jpg uploads/*.png
	rm -rf *.db

build:
	docker build -t photo-geolocation .

run: build
	docker-compose up

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down -v

lint:
	poetry run flake8 app/ tests/
	poetry run mypy app/

format:
	poetry run black app/ tests/
	poetry run isort app/ tests/

setup-dev: install
	cp .env.example .env
	@echo "Please edit .env file with your API keys"

migrate:
	poetry run alembic upgrade head

seed-data:
	poetry run python scripts/seed_data.py
