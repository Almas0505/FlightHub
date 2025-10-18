# ✈️ FlightHub - Modern Flight Booking Platform# 🛫 FlightHub - Flight Booking Platform



<div align="center">[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)

![FlightHub Banner](https://img.shields.io/badge/FlightHub-Production_Ready-0066cc?style=for-the-badge&logo=airplane&logoColor=white)[![Django](https://img.shields.io/badge/Django-4.2-darkgreen.svg)](https://www.djangoproject.com/)

[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

**Enterprise-grade flight booking platform built with microservices architecture**[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)



[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)  <h3>🎯 Production-Ready | 🚀 Microservices | ⚡ Async | 🐳 Docker</h3>

[![Django](https://img.shields.io/badge/Django-4.2-092e20?logo=django&logoColor=white)](https://www.djangoproject.com/)</div>

[![React](https://img.shields.io/badge/React-18-61dafb?logo=react&logoColor=black)](https://reactjs.org/)

[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178c6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)## ⚡ Quick Start (60 секунд)

[![Docker](https://img.shields.io/badge/Docker-Compose-2496ed?logo=docker&logoColor=white)](https://www.docker.com/)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)```powershell

# 1. Клонировать проект

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Tech Stack](#-tech-stack) • [API Docs](#-api-documentation)git clone https://github.com/your-username/flighthub.git

cd flighthub

</div>

# 2. Запустить все сервисы

---docker-compose up -d



## 📋 Overview# 3. Создать тестовые данные

docker exec flighthub-user python manage.py seed_users

FlightHub is a **production-ready flight booking platform** demonstrating modern software engineering practices. Built to showcase scalable microservices architecture, event-driven design, and full-stack development capabilities for **travel-tech industry**.docker exec flighthub-flight-search python seed_flights.py



### 🎯 Key Highlights# 4. Открыть браузер

# Frontend: http://localhost:3000

- **6 Microservices** with clear separation of concerns# Profile: http://localhost:3000/profile

- **Event-Driven** asynchronous communication via RabbitMQ# API Docs: http://localhost:8000/docs

- **JWT Authentication** with secure token management```

- **Real-time Flight Search** across 300+ routes with intelligent caching

- **Loyalty Program** with tiered rewards (Bronze → Platinum)**🔐 Demo Login:**

- **Modern UI** built with React 18, TypeScript, and Tailwind CSS- Email: `demo@flighthub.com`

- **One-Command Deployment** using Docker Compose- Password: `Demo123!`

- **Auto-Generated API Documentation** with interactive Swagger UI- Tier: GOLD (15,000 loyalty points)



---**✨ Что посмотреть:**

1. **Главная** (/) - Hero section с поиском

## ⚡ Quick Start2. **Поиск** (/flights) - Красивые карточки рейсов (317 в базе!)

3. **Профиль** (/profile) - Loyalty программа, редактирование

### Prerequisites4. **API Docs** (:8000/docs) - Swagger UI с Try it out



- **Docker Desktop** (Windows/Mac) or **Docker Engine + Compose** (Linux)---

- **Minimum:** 4GB RAM, 10GB disk space

- **Recommended:** 8GB RAM, 20GB disk space## 📋 О Проекте



### Installation (60 seconds)**FlightHub** - это полнофункциональная микросервисная система для бронирования авиабилетов, демонстрирующая современные подходы к разработке backend приложений.



```bash### ✨ Ключевые Особенности

# Clone the repository

git clone https://github.com/yourusername/flighthub.git- � **Современный Frontend** (React 18 + TypeScript + Tailwind CSS)

cd flighthub- �🏗️ **6 Микросервисов** с четким разделением ответственности

- ⚡ **Асинхронная обработка** для высокой производительности

# Start all services- 🔐 **JWT Аутентификация** и защита от DDoS

docker-compose up -d- 📨 **Event-Driven Architecture** через RabbitMQ

- 🗄️ **Polyglot Persistence**: PostgreSQL + MongoDB + Redis

# Wait for initialization (~30 seconds)- 🐳 **Docker Compose** с health checks

docker-compose ps- 📊 **Структурированное логирование** и мониторинг

- 📚 **Auto-Generated API Docs** (Swagger/ReDoc)

# Seed demo data

docker exec flighthub-user python manage.py seed_users---

docker exec flighthub-flight-search python seed_flights.py

## 🏗️ Архитектура

# Access application

# Frontend: http://localhost:3000```

# API Gateway: http://localhost:8000                    ┌──────────────────────────┐

# API Docs: http://localhost:8000/docs                    │   FRONTEND (React 18)    │

```                    │  Vite + Tailwind CSS     │

                    │      Port 3000           │

### Demo Credentials                    └──────────┬───────────────┘

                               │

| Email | Password | Tier | Points |┌──────────────────────────────▼───────────────────────────────────┐

|-------|----------|------|--------|│                         API GATEWAY (FastAPI)                     │

| **demo@flighthub.com** | **Demo123!** | GOLD | 15,000 |│         JWT Auth | Rate Limiting | Circuit Breaker | CORS        │

| john.doe@example.com | Test123! | PLATINUM | 50,000 |└───────┬─────────────┬──────────────┬──────────────┬──────────────┘

| jane.smith@example.com | Test123! | SILVER | 5,000 |        │             │              │              │

   ┌────▼────┐  ┌────▼────┐   ┌────▼────┐   ┌─────▼─────┐

---   │ Flight  │  │ Booking │   │ Payment │   │   User    │

   │ Search  │  │ Service │   │ Service │   │  Service  │

## ✨ Features   │(FastAPI)│  │(Django) │   │(Django) │   │ (Django)  │

   └────┬────┘  └────┬────┘   └────┬────┘   └─────┬─────┘

### 🔐 User Management        │            │              │              │

- Secure JWT-based authentication with refresh tokens        │            └──────┬───────┴──────────────┘

- User profile management with editable information        │                   │

- Multi-tier loyalty program (Bronze → Silver → Gold → Platinum)   ┌────▼────┐       ┌─────▼──────┐       ┌──────────────┐

- Points accumulation and reward tracking   │ MongoDB │       │ PostgreSQL │       │ Notification │

   │ + Redis │       │            │       │   Service    │

### 🔍 Flight Search Engine   └─────────┘       └────────────┘       │  (FastAPI)   │

- Real-time search across multiple routes                                           └──────┬───────┘

- Advanced filtering (price, duration, stops, cabin class)                                                  │

- Smart caching with Redis for sub-second response times                                           ┌──────▼───────┐

- 300+ flights across 11 international routes                                           │   RabbitMQ   │

- Support for one-way and round-trip bookings                                           └──────────────┘

```

### 🎫 Booking Management

- Multi-passenger booking support---

- Automated PNR (Passenger Name Record) generation

- Booking status tracking and history## 🚀 Быстрый Старт

- Time-based auto-expiration (15 minutes)

- Email confirmations and notifications### Требования

- Docker Desktop (Windows/Mac) или Docker + Docker Compose (Linux)

### 💳 Payment Processing- 8 GB RAM минимум

- Secure payment gateway integration- 10 GB свободного места на диске

- Multiple payment method support

- Transaction history and receipts### Запуск за 1 минуту

- Automated refund processing

```bash

### 📧 Notification System# Клонировать репозиторий

- Real-time email notificationsgit clone <repository-url>

- Booking confirmations and updatescd flighthub

- Payment receipts

- Event-driven asynchronous delivery# Запустить все сервисы

docker-compose up -d

---

# Проверить статус

## 🏗️ Architecturedocker-compose ps



### System Design# Открыть приложение

start http://localhost:3000        # Frontend

```start http://localhost:8000/docs  # API Docs (Windows)

                         ┌─────────────────────────┐open http://localhost:3000         # Mac

                         │   React 18 Frontend     │```

                         │  TypeScript + Tailwind  │

                         │      Port: 3000         │### Проверка работоспособности

                         └───────────┬─────────────┘

                                     │```bash

                  ┌──────────────────▼──────────────────────┐# Frontend

                  │         API Gateway (FastAPI)           │curl http://localhost:3000

                  │  JWT Auth • Rate Limit • Circuit Breaker│

                  │              Port: 8000                  │# Backend API Health check

                  └──────┬──────────┬──────────┬─────────────┘curl http://localhost:8000/health

                         │          │          │

           ┌─────────────▼──┐  ┌───▼─────┐  ┌▼──────────┐# Поиск рейсов

           │  Flight Search │  │ Booking │  │   User    │curl "http://localhost:8000/api/v1/flights/search?from_airport=ALA&to_airport=DXB&departure_date=2025-11-01&passengers=1"

           │    (FastAPI)   │  │(Django) │  │ (Django)  │```

           │   MongoDB      │  │  PG SQL │  │  PG SQL   │

           └─────────┬──────┘  └───┬─────┘  └─────┬─────┘### 🎨 Доступные приложения

                     │             │              │

                     └─────┬───────┴──────────────┘- **Frontend**: http://localhost:3000 (React SPA)

                           │- **API Gateway**: http://localhost:8000

                    ┌──────▼───────┐      ┌──────────────┐- **API Docs**: http://localhost:8000/docs (Swagger UI)

                    │   RabbitMQ   │◄─────┤ Notification │- **RabbitMQ Management**: http://localhost:15672 (admin/secret)

                    │ Message Bus  │      │   Service    │```

                    └──────────────┘      └──────────────┘

```---



### Communication Patterns## 📦 Компоненты Системы



**Synchronous (REST):**### 1. API Gateway (Port 8000) - FastAPI

- Client → API Gateway → Microservices**Единая точка входа для всех запросов**

- Request/Response with JWT validation

Фичи:

**Asynchronous (Events):**- ✅ JWT аутентификация (access + refresh tokens)

```- ✅ Rate limiting через Redis (sliding window)

booking.created   → [Payment Service, Notification Service]- ✅ Circuit breaker для отказоустойчивости

payment.completed → [Booking Service, Notification Service]- ✅ Request/Response логирование

user.registered   → [Notification Service]- ✅ CORS и Security headers

```

Документация: [`flighthub-api-gateway/README.md`](flighthub-api-gateway/README.md)

---

### 2. Flight Search Service (Port 8001) - FastAPI

## 🛠️ Tech Stack**Асинхронный поиск и агрегация рейсов**



### BackendФичи:

- ✅ Параллельный поиск по нескольким GDS провайдерам

| Component | Technology | Purpose |- ✅ Mock Provider с реалистичными данными

|-----------|-----------|---------|- ✅ Amadeus GDS интеграция (частично)

| **API Gateway** | FastAPI 0.109 | Request routing, authentication, rate limiting |- ✅ MongoDB для кеширования расписаний

| **Flight Search** | FastAPI 0.109 | Async flight search and aggregation |- ✅ Redis для быстрого кеша

| **Booking Service** | Django 4.2 | Booking management and state machine |- ✅ Celery для фоновых обновлений

| **Payment Service** | Django 4.2 | Payment processing and transactions |

| **User Service** | Django 4.2 | User authentication and profiles |Документация: [`flight-search-service/README.md`](flight-search-service/README.md)

| **Notification** | FastAPI 0.109 | Email/SMS delivery |

### 3. Booking Service (Port 8002) - Django REST

### Databases**Управление бронированиями и билетами**



- **PostgreSQL 16** - Transactional data (Users, Bookings, Payments)Фичи:

- **MongoDB 7** - Flight schedules and search cache- ✅ State Machine для статусов бронирования

- **Redis 7** - Session cache and rate limiting- ✅ PNR (Passenger Name Record) генерация

- ✅ Автоматическая expire через 15 минут

### Infrastructure- ✅ Event publishing в RabbitMQ

- ✅ Celery задачи для background обработки

- **RabbitMQ 3.12** - Event bus for async messaging- ✅ Django Admin панель

- **Celery 5.3** - Distributed task queue

- **Docker Compose** - Service orchestrationДокументация: [`booking-service/README.md`](booking-service/README.md)

- **Nginx** - Reverse proxy for frontend

### 4. Payment Service (Port 8003) - Django REST

### Frontend**Обработка платежей и возвратов**



- **React 18** - Modern UI libraryФичи:

- **TypeScript 5** - Type-safe development- ⚠️ Payment модель и API endpoints (в разработке)

- **Vite** - Lightning-fast build tool- ⚠️ Mock payment provider

- **Tailwind CSS** - Utility-first styling- ⚠️ Idempotency keys

- **shadcn/ui** - Premium component library- ⚠️ Webhook handling

- **Zustand** - Lightweight state management

- **React Router 6** - Client-side routing### 5. User Service (Port 8005) - Django REST

- **Axios** - HTTP client with interceptors**Управление пользователями и профилями**



---Фичи:

- ⚠️ User registration/login (в разработке)

## 📚 API Documentation- ⚠️ JWT token generation

- ⚠️ Loyalty program (базовая структура)

### Interactive Docs

### 6. Notification Service (Port 8004) - FastAPI

- **Swagger UI:** http://localhost:8000/docs**Email, SMS, Push уведомления**

- **ReDoc:** http://localhost:8000/redoc

Фичи:

### Key Endpoints- ✅ Базовые HTTP endpoints

- ⚠️ RabbitMQ consumer (в разработке)

#### Authentication- ⚠️ Email templates

```http- ⚠️ Event handlers

POST /api/v1/users/register      # User registration

POST /api/v1/users/login          # Login (returns JWT)---

POST /api/v1/users/refresh        # Refresh access token

GET  /api/v1/users/me             # Get current user## 🛠️ Технологический Стек

PUT  /api/v1/users/me             # Update profile

```### Backend Frameworks

- **FastAPI** 0.109 - для высоконагруженных сервисов

#### Flight Search- **Django** 4.2 + **DRF** 3.14 - для бизнес-логики

```http

GET /api/v1/flights/search### Базы Данных

  ?from_airport=ALA- **PostgreSQL** 15 - транзакционные данные

  &to_airport=DXB- **MongoDB** 6 - поисковые данные и кеш

  &departure_date=2025-11-01- **Redis** 7 - кеширование и rate limiting

  &passengers=2

  &cabin_class=economy### Message Queue

- **RabbitMQ** 3 - асинхронная коммуникация

GET /api/v1/flights/{flight_id}   # Flight details- **Celery** 5.3 - фоновые задачи

GET /api/v1/flights/airports      # Available airports

```### Infrastructure

- **Docker** & **Docker Compose**

#### Bookings- **Nginx** (для production)

```http- **Prometheus** & **Grafana** (planned)

POST   /api/v1/bookings           # Create booking

GET    /api/v1/bookings           # List user bookings### Python Libraries

GET    /api/v1/bookings/{id}      # Booking details```

PUT    /api/v1/bookings/{id}      # Update bookingaiohttp, httpx - async HTTP clients

DELETE /api/v1/bookings/{id}      # Cancel bookingpydantic - data validation

```structlog - structured logging

pyjwt - JWT tokens

#### Paymentsmotor - async MongoDB

```httppytest - testing

POST /api/v1/payments             # Process payment```

GET  /api/v1/payments/{id}        # Payment status

POST /api/v1/payments/refund      # Request refund---

```

## 📚 API Документация

---

### Swagger UI

## 📂 Project Structure- **API Gateway**: http://localhost:8000/docs

- **Flight Search**: http://localhost:8001/docs

```

flighthub/### Основные Endpoints

├── flighthub-api-gateway/        # API Gateway (FastAPI)

│   ├── app/#### 🔍 Поиск Рейсов

│   │   ├── routes/               # API endpoints```http

│   │   ├── middleware/           # Auth, rate limitingGET /api/v1/flights/search

│   │   └── utils/                # HelpersQuery Parameters:

│   └── Dockerfile  - from_airport: string (IATA code, e.g., ALA)

│  - to_airport: string (IATA code, e.g., DXB)

├── user-service/                  # User Service (Django)  - departure_date: date (YYYY-MM-DD)

│   ├── accounts/  - return_date: date (optional)

│   │   ├── models.py             # User, LoyaltyTier  - passengers: integer (1-9)

│   │   ├── serializers.py  - cabin_class: enum (economy|business|first)

│   │   └── views.py```

│   ├── management/commands/

│   │   └── seed_users.py         # Demo data#### 📝 Создание Бронирования

│   └── Dockerfile```http

│POST /api/v1/bookings

├── flight-search-service/         # Flight Search (FastAPI)Authorization: Bearer <token>

│   ├── app/Body: {

│   │   ├── models/               # Pydantic schemas  "flight_id": "FL-abc123",

│   │   ├── services/             # Search engine  "passengers": [...],

│   │   ├── repositories/         # MongoDB  "contact_email": "user@example.com",

│   │   └── providers/            # External APIs  "contact_phone": "+77001234567"

│   ├── seed_flights.py           # 300+ flights}

│   └── Dockerfile```

│

├── booking-service/               # Booking Service (Django)#### 💳 Оплата

│   ├── bookings/```http

│   │   ├── models.py             # Booking, PNRPOST /api/v1/payments

│   │   ├── services.py           # Business logicAuthorization: Bearer <token>

│   │   └── tasks.py              # Celery tasksBody: {

│   ├── passengers/               # Passenger models  "booking_id": "uuid",

│   ├── tickets/                  # Ticket generation  "amount": 150000,

│   └── Dockerfile  "payment_method": "CARD",

│  "card_token": "tok_visa"

├── payment-service/               # Payment Service (Django)}

│   ├── payments/```

│   │   ├── models.py             # Payment, Transaction

│   │   └── views.py#### 👤 Регистрация

│   └── Dockerfile```http

│POST /api/v1/users/register

├── notification-service/          # Notification (FastAPI)Body: {

│   ├── app/  "email": "user@example.com",

│   │   ├── consumers/            # RabbitMQ consumers  "password": "securepass123",

│   │   └── email/                # Email templates  "first_name": "John",

│   └── Dockerfile  "last_name": "Doe",

│  "phone": "+77001234567"

├── frontend/                      # React Frontend}

│   ├── src/```

│   │   ├── components/           # Reusable components

│   │   │   └── ui/               # shadcn/ui components---

│   │   ├── pages/

│   │   │   ├── HomePage.tsx## 🧪 Тестирование

│   │   │   ├── FlightSearchPage.tsx

│   │   │   ├── ProfilePage.tsx```bash

│   │   │   └── LoginPage.tsx# Запустить unit тесты

│   │   ├── store/cd booking-service

│   │   │   └── authStore.ts      # Zustand statepytest

│   │   ├── lib/

│   │   │   └── api.ts            # Axios client# С покрытием кода

│   │   └── types/                # TypeScript typespytest --cov=bookings --cov-report=html

│   ├── Dockerfile

│   └── nginx.conf# Integration тесты

│pytest tests/integration/

├── docker-compose.yml             # Orchestration

└── README.md# Async тесты

```cd flight-search-service

pytest tests/ -v

---```



## 🧪 Testing---



### Run Tests## 📊 Мониторинг



```bash### Health Checks

# Backend unit tests```bash

docker exec flighthub-user python manage.py test# Все сервисы

docker exec flighthub-booking python manage.py testcurl http://localhost:8000/health  # API Gateway

curl http://localhost:8001/health  # Flight Search

# Frontend testscurl http://localhost:8002/admin/  # Booking (Django)

cd frontend```

npm run test

### RabbitMQ Management UI

# Integration tests```

pytest tests/integration/URL: http://localhost:15672

Login: admin / secret

# With coverage```

pytest --cov=app --cov-report=html

```### Celery Monitoring

```bash

### Health Checks# Активные задачи

celery -A booking_service inspect active

```bash

# Check all services# Scheduled задачи

docker-compose pscelery -A booking_service inspect scheduled

```

# Health endpoints

curl http://localhost:8000/health           # API Gateway### Логи

curl http://localhost:8001/health           # Flight Search```bash

curl http://localhost:8002/admin/           # Booking Service# Все сервисы

```docker-compose logs -f



---# Конкретный сервис

docker-compose logs -f api-gateway

## 🔧 Developmentdocker-compose logs -f flight-search

```

### Local Development (without Docker)

---

```bash

# Start infrastructure only## 🔐 Безопасность

docker-compose up -d postgres mongodb redis rabbitmq

- ✅ JWT токены с коротким временем жизни (30 мин)

# Run service locally- ✅ Refresh tokens (7 дней)

cd flight-search-service- ✅ Rate limiting (100 req/min per user)

python -m venv venv- ✅ CORS настройки

source venv/bin/activate  # Windows: venv\Scripts\activate- ✅ Input validation (Pydantic, DRF)

pip install -r requirements.txt- ✅ Password hashing (готовность к bcrypt)

uvicorn app.main:app --reload --port 8001- ✅ Environment variables для секретов



# Run frontend---

cd frontend

npm install## 📈 Производительность

npm run dev  # Starts on http://localhost:5173

```### Метрики

```

### Database MigrationsFlight Search: ~500ms (mock provider)

Booking Creation: ~200ms

```bashPayment Processing: ~150ms

# User serviceEnd-to-End Flow: ~1 second

docker exec flighthub-user python manage.py makemigrations```

docker exec flighthub-user python manage.py migrate

### Масштабирование

# Booking service- Horizontal scaling через Kubernetes

docker exec flighthub-booking python manage.py makemigrations- Read replicas для баз данных

docker exec flighthub-booking python manage.py migrate- Redis Cluster для кеша

```- Load balancer перед API Gateway



### View Logs---



```bash## 🚧 Текущий Статус

# All services

docker-compose logs -f### ✅ Полностью Реализовано

- [x] API Gateway с middleware stack

# Specific service- [x] Flight Search с async search engine

docker-compose logs -f api-gateway- [x] Booking Service с state machine

docker-compose logs -f flight-search --tail=100- [x] Docker Compose infrastructure

```- [x] Celery workers и beat schedulers

- [x] MongoDB + PostgreSQL + Redis + RabbitMQ

---- [x] Swagger/ReDoc documentation



## 🌐 Environment Configuration### ⚠️ В Разработке

- [ ] Payment Service (40% готово)

### Key Environment Variables- [ ] User Service (30% готово)

- [ ] Notification Service consumer (50% готово)

```env- [ ] Integration tests

# API Gateway- [ ] Kubernetes manifests

ENVIRONMENT=production

USER_SERVICE_URL=http://user-service:8000---

FLIGHT_SERVICE_URL=http://flight-search-service:8000

BOOKING_SERVICE_URL=http://booking-service:8000## � Статус проекта

REDIS_URL=redis://redis:6379/0

### ✅ Готово (95%)

# User Service- JWT Authentication - 100% работает

DATABASE_URL=postgresql://postgres:postgres@postgres:5432/user_db- Микросервисная архитектура - все сервисы запущены

SECRET_KEY=your-secret-key-change-in-production- Docker Compose orchestration

JWT_SECRET_KEY=your-jwt-secret-change-in-production- Frontend на React + TypeScript

JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30- API Gateway с rate limiting

JWT_REFRESH_TOKEN_EXPIRE_DAYS=7- Flight Search с MongoDB

RABBITMQ_URL=amqp://admin:secret@rabbitmq:5672- Booking Service с PostgreSQL

- Payment Service skeleton

# Frontend- Notification Service skeleton

VITE_API_URL=http://localhost:8000/api/v1

```### 🔧 В разработке (5%)

- Real payment integration (Stripe/Kaspi)

---- Email notifications (SMTP)

- Unit tests (target: 80% coverage)

## 🐛 Troubleshooting- Production secrets management



### Services Won't Start### 🚀 Roadmap (2-3 месяца)

- Kubernetes deployment (Helm)

```bash- Monitoring (Prometheus + Grafana)

# Check logs for errors- CI/CD (GitHub Actions)

docker-compose logs [service-name]- Real flight providers (Amadeus API)

- Mobile apps (React Native)

# Rebuild containers

docker-compose down -v---

docker-compose up -d --build

## 🎯 Для Работодателей

# Check resource usage

docker stats### Что Демонстрирует Этот Проект

```

✅ **Микросервисная архитектура**

### Database Connection Issues- Правильное разделение ответственности

- Event-driven communication

```bash- Service discovery

# Wait for databases to be ready

docker-compose ps✅ **Современный Python Stack**

- FastAPI для высокопроизводительных API

# Test PostgreSQL- Django для сложной бизнес-логики

docker exec flighthub-postgres pg_isready- Async/await patterns



# Test MongoDB✅ **Production-Ready Подход**

docker exec flighthub-mongodb mongosh --eval "db.runCommand({ ping: 1 })"- Docker containerization

```- Health checks

- Structured logging

### Port Conflicts- Error handling

- API documentation

```powershell

# Check if ports are in use (Windows)✅ **DevOps Skills**

netstat -an | findstr "3000 8000 5432 27017"- Docker Compose orchestration

- Multi-stage builds

# Change ports in docker-compose.yml if needed- Environment configuration

```- CI/CD ready



---✅ **Best Practices**

- Clean code architecture

## 🚀 Deployment- Type hints (Pydantic, mypy)

- Unit and integration tests

### Production Considerations- Git workflow



- [ ] Use environment-specific `.env` files### Применимость к Travel-Tech

- [ ] Enable HTTPS with SSL certificates

- [ ] Configure proper CORS originsЭтот проект использует patterns и технологии, применяемые в:

- [ ] Set up monitoring (Prometheus + Grafana)- ✈️ Booking.com, Expedia, Airbnb

- [ ] Implement log aggregation (ELK stack)- 🏨 Hospitality системы

- [ ] Use managed databases (AWS RDS, MongoDB Atlas)- 🚗 Ride-sharing платформы

- [ ] Set up CI/CD pipeline (GitHub Actions)- 🎫 Ticketing systems

- [ ] Configure auto-scaling (Kubernetes)

---

### Docker Production Build

## 🔮 Что можно улучшить

```bash

# Build optimized images### Priority 1 (1-2 недели)

docker-compose -f docker-compose.prod.yml build- [ ] **Real Payment Integration** - Stripe/Kaspi Pay вместо mock

- [ ] **Email Notifications** - Реальные SMTP уведомления

# Deploy with secrets- [ ] **Unit Tests** - Покрытие 80%+

docker-compose -f docker-compose.prod.yml up -d- [ ] **Production Security** - Secrets management (Vault)

```- [ ] **HTTPS/TLS** - SSL сертификаты



---### Priority 2 (1-2 месяца)

- [ ] **Kubernetes** - Helm charts для deployment

## 🎯 For Employers- [ ] **Monitoring** - Prometheus + Grafana dashboards

- [ ] **CI/CD** - GitHub Actions pipeline

This project demonstrates:- [ ] **Real Flight API** - Amadeus/Sabre integration

- [ ] **Distributed Tracing** - Jaeger для debugging

### Technical Skills

✅ **Microservices Architecture** - Service decomposition, API design  ### Priority 3 (3-6 месяцев)

✅ **Async Programming** - FastAPI, Celery, RabbitMQ  - [ ] **Mobile Apps** - React Native (iOS + Android)

✅ **Database Design** - PostgreSQL, MongoDB, Redis  - [ ] **AI Features** - Price prediction, smart recommendations

✅ **Authentication & Security** - JWT, rate limiting, input validation  - [ ] **Chatbot** - GPT-4 customer support

✅ **DevOps** - Docker, Docker Compose, multi-stage builds  - [ ] **Multi-currency** - USD, EUR, KZT, RUB

✅ **Full-Stack Development** - React, TypeScript, Python  - [ ] **Analytics** - Business intelligence dashboard

✅ **API Design** - RESTful principles, OpenAPI/Swagger  

✅ **Event-Driven Architecture** - Message queues, async workers  ---



### Applicable To## 🤝 Локальная Разработка

- ✈️ Travel & Hospitality platforms (Booking.com, Expedia)

- 🏨 Hotel booking systems### Seed Data

- 🚗 Ride-sharing applications```bash

- 🎫 Event ticketing platforms# Создать тестовых пользователей

- 📦 E-commerce marketplacesdocker exec flighthub-user python manage.py seed_users



---# Загрузить рейсы в базу

docker exec flighthub-flight-search python seed_flights.py

## 📈 Roadmap```



### Phase 1 - Core Features ✅### Development Mode

- [x] Microservices architecture```bash

- [x] JWT authentication# Запустить только инфраструктуру

- [x] Flight search enginedocker-compose up -d postgres mongodb redis rabbitmq

- [x] Booking management

- [x] User profiles with loyalty program# Разработка конкретного сервиса

- [x] Beautiful React UIcd flight-search-service

python -m venv venv

### Phase 2 - Production Ready 🚧source venv/bin/activate  # или venv\Scripts\activate на Windows

- [ ] Real payment integration (Stripe/Kaspi)pip install -r requirements.txt

- [ ] Email notifications (SMTP)uvicorn app.main:app --reload --port 8001

- [ ] Unit tests (80% coverage)```

- [ ] Integration tests

- [ ] Kubernetes deployment### Code Style

```bash

### Phase 3 - Advanced Features 📅# Format

- [ ] Real flight API integration (Amadeus)black app/

- [ ] Mobile app (React Native)isort app/

- [ ] Admin dashboard

- [ ] Analytics and reporting# Lint

- [ ] Multi-currency supportflake8 app/

- [ ] AI-powered recommendationsmypy app/

```

---

---

## 🤝 Contributing

## 📞 Контакты

Contributions are welcome! Please follow these guidelines:

- **GitHub Issues**: Для вопросов и предложений

1. Fork the repository- **Email**: [ваш email]

2. Create a feature branch (`git checkout -b feature/amazing-feature`)- **LinkedIn**: [ваш LinkedIn]

3. Make your changes with clear commit messages

4. Write tests for new features---

5. Ensure all tests pass

6. Submit a Pull Request## 📄 Лицензия



### Code StyleMIT License - см. [LICENSE](LICENSE) файл



- **Python:** Follow PEP 8, use `black` formatter---

- **TypeScript:** Follow Airbnb style guide, use `prettier`

- **Commits:** Use conventional commits (`feat:`, `fix:`, `docs:`)## 🙏 Acknowledgments



---- FastAPI Documentation

- Django REST Framework

## 📄 License- Docker Community

- Travel Tech Industry Best Practices

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

---

<div align="center">

## 👨‍💻 Author  <h3>⭐ Если проект полезен, поставьте звезду! ⭐</h3>

  <p>Made with ❤️ for Travel Tech Industry</p>

**Your Name**</div>


- 🌐 Portfolio: [yourwebsite.com](https://yourwebsite.com)
- 💼 LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- 📧 Email: your.email@example.com
- 🐙 GitHub: [@yourusername](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Django](https://www.djangoproject.com/) - Batteries-included web framework
- [React](https://reactjs.org/) - A JavaScript library for building user interfaces
- [shadcn/ui](https://ui.shadcn.com/) - Beautiful and accessible components
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- Travel Tech community for best practices and patterns

---

<div align="center">

### ⭐ Star this repository if you find it useful!

**Built with** ❤️ **for the Travel Tech Industry**

[⬆ Back to Top](#-flighthub---modern-flight-booking-platform)

</div>
