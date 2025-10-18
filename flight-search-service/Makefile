.PHONY: help install run test lint format clean docker-build docker-run

help:
	@echo "Flight Search Service - Available Commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make run           - Run development server"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code"
	@echo "  make clean         - Clean cache and artifacts"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run with Docker Compose"
	@echo "  make docker-down   - Stop Docker containers"
	@echo "  make seed-data     - Seed sample airport data"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --port 8001

test:
	pytest -v

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term

lint:
	flake8 app/
	mypy app/

format:
	black app/
	isort app/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

docker-build:
	docker build -t flight-search-service:latest .

docker-run:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f flight-search

seed-data:
	curl -X POST http://localhost:8001/airports/seed

celery-worker:
	celery -A app.tasks.celery_app worker -l info

celery-beat:
	celery -A app.tasks.celery_app beat -l info
