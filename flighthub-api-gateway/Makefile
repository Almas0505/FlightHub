.PHONY: help install run test lint format clean docker-build docker-run

help:
	@echo "FlightHub API Gateway - Available Commands:"
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

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

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
	docker build -t flighthub-api-gateway:latest .

docker-run:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f api-gateway
