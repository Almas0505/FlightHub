# ✈️ FlightHub

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![Django](https://img.shields.io/badge/Django-4.2-darkgreen.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178c6.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Современная микросервисная платформа для бронирования авиабилетов**

[Особенности](#-особенности) • [Быстрый старт](#-быстрый-старт) • [Архитектура](#-архитектура) • [Технологии](#-технологии)

</div>

---

## 📋 О проекте

**FlightHub** — production-ready система бронирования авиабилетов, демонстрирующая современные подходы к разработке:

- 🏗️ **Микросервисная архитектура** — 6 независимых сервисов
- ⚡ **Event-Driven Design** — асинхронная обработка через RabbitMQ
- 🔐 **JWT аутентификация** — безопасная система токенов
- 🎨 **Современный UI** — React 18 + TypeScript + Tailwind CSS
- 🐳 **Docker Compose** — развертывание одной командой

---

## ✨ Особенности

### Backend
- **6 микросервисов**: API Gateway, User, Flight Search, Booking, Payment, Notification
- **Polyglot Persistence**: PostgreSQL + MongoDB + Redis
- **Асинхронная обработка**: RabbitMQ для событий, Celery для задач
- **Защита API**: Rate limiting, JWT токены, валидация данных
- **Автодокументация**: Swagger UI и ReDoc

### Frontend
- **React 18** с TypeScript для type-safety
- **Tailwind CSS** + shadcn/ui компоненты
- **Zustand** для управления состоянием
- **Responsive дизайн** для всех устройств

### DevOps
- **Docker Compose** оркестрация 14 контейнеров
- **Health checks** для всех сервисов
- **Multi-stage builds** для оптимизации образов
- **Structured logging** с централизованными логами

---

## ⚡ Быстрый старт

### Требования
- Docker Desktop (или Docker Engine + Compose)
- Минимум: 4GB RAM, 10GB дискового пространства
- Рекомендуется: 8GB RAM, 20GB дискового пространства

### Установка (60 секунд)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/yourusername/flighthub.git
cd flighthub

# 2. Запустить все сервисы
docker-compose up -d

# 3. Дождаться инициализации (~30 сек)
docker-compose ps

# 4. Загрузить тестовые данные
docker exec flighthub-user python manage.py seed_users
docker exec flighthub-flight-search python seed_flights.py
```

### Доступ к приложению

- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Тестовый аккаунт

```
Email: demo@flighthub.com
Password: Demo123!
Loyalty Tier: GOLD (15,000 баллов)
```

---

## 🏗️ Архитектура

```
                    ┌──────────────────────────┐
                    │   FRONTEND (React 18)    │
                    │  Vite + Tailwind CSS     │
                    │      Port 3000           │
                    └──────────┬───────────────┘
                               │
                    ┌──────────▼───────────────┐
                    │   API GATEWAY (FastAPI)  │
                    │  Routing • Auth • Rate   │
                    │   Limiting • Port 8000   │
                    └──┬────┬────┬────┬────┬───┘
                       │    │    │    │    │
        ┌──────────────┘    │    │    │    └──────────────┐
        │                   │    │    │                   │
 ┌──────▼──────┐   ┌────────▼────▼────▼────────┐   ┌─────▼──────┐
 │   FLIGHT    │   │      USER SERVICE          │   │  BOOKING   │
 │   SEARCH    │   │   (Django + PostgreSQL)    │   │  SERVICE   │
 │  (FastAPI)  │   │  • Auth • Profiles • Loyalty│   │  (Django)  │
 │  + MongoDB  │   │      Port 8001             │   │  Port 8003 │
 │  Port 8002  │   └────────┬───────────────────┘   └─────┬──────┘
 └─────────────┘            │                             │
                            │      ┌──────────────────────┘
                            │      │
                    ┌───────▼──────▼───────┐
                    │   PAYMENT SERVICE    │
                    │  (Django + Postgres) │
                    │      Port 8004       │
                    └───────┬──────────────┘
                            │
                    ┌───────▼──────────────┐
                    │  NOTIFICATION SERVICE│
                    │     (FastAPI)        │
                    │      Port 8005       │
                    └──────────────────────┘
                            │
                    ┌───────▼──────────────┐
                    │   RABBITMQ MESSAGE   │
                    │       BUS            │
                    │  Event Distribution  │
                    └──────────────────────┘
```

### Event Flow

```
Booking Created → RabbitMQ → [Payment, Notification]
Payment Success → RabbitMQ → [Booking Update, User Points]
```

---

## 🛠️ Технологии

### Backend Services

| Сервис | Технология | БД | Назначение |
|--------|-----------|-----|-----------|
| API Gateway | FastAPI | Redis | Роутинг, аутентификация, rate limiting |
| Flight Search | FastAPI | MongoDB | Поиск рейсов в реальном времени |
| Booking | Django | PostgreSQL | Управление бронированиями |
| Payment | Django | PostgreSQL | Обработка платежей |
| User | Django | PostgreSQL | Пользователи и профили |
| Notification | FastAPI | - | Email/SMS уведомления |

### Frontend Stack
- React 18 + TypeScript
- Tailwind CSS + shadcn/ui
- Zustand (state management)
- React Router
- Axios для API запросов

### Infrastructure
- Docker & Docker Compose
- RabbitMQ (message broker)
- Redis (caching)
- Celery (task queue)
- Nginx (reverse proxy)
- PostgreSQL & MongoDB

---

## 📚 Что демонстрирует проект

### Архитектурные паттерны
- ✅ **Microservices Architecture** — разделение по бизнес-доменам
- ✅ **Event-Driven Design** — асинхронная коммуникация
- ✅ **API Gateway Pattern** — единая точка входа
- ✅ **Database per Service** — изоляция данных

### Backend Skills
- ✅ **FastAPI** — высокопроизводительные async API
- ✅ **Django** — сложная бизнес-логика
- ✅ **PostgreSQL** — реляционные данные
- ✅ **MongoDB** — документоориентированное хранилище
- ✅ **Redis** — кэширование и rate limiting
- ✅ **RabbitMQ** — message queuing

### DevOps & Infrastructure
- ✅ **Docker Compose** — multi-container оркестрация
- ✅ **Health Checks** — мониторинг состояния сервисов
- ✅ **Environment Variables** — конфигурация через .env
- ✅ **Structured Logging** — JSON логи для агрегации

### Frontend Development
- ✅ **React 18** — современные hooks и patterns
- ✅ **TypeScript** — type safety
- ✅ **Tailwind CSS** — utility-first styling
- ✅ **Component Library** — переиспользуемые компоненты

---

## 🎯 Применимость

Проект использует паттерны и технологии, применяемые в:

- ✈️ **Travel Tech**: Booking.com, Expedia, Airbnb
- 🏨 **Hospitality**: системы управления отелями
- 🚗 **Ride-sharing**: Uber, Lyft
- 🎫 **Ticketing**: системы продажи билетов
- 📦 **E-commerce**: маркетплейсы

---

## 🔮 Roadmap

### Phase 1 - MVP ✅
- [x] Микросервисная архитектура
- [x] JWT аутентификация
- [x] Поиск рейсов
- [x] Система бронирования
- [x] Программа лояльности
- [x] React UI

### Phase 2 - Production Ready 🚧
- [ ] Real payment integration (Stripe/Kaspi)
- [ ] Email notifications (SMTP)
- [ ] Unit тесты (80% coverage)
- [ ] Integration тесты
- [ ] Kubernetes deployment

### Phase 3 - Advanced Features 📅
- [ ] Интеграция с реальными API авиакомпаний (Amadeus)
- [ ] Mobile app (React Native)
- [ ] Admin dashboard
- [ ] Analytics и reporting
- [ ] Multi-currency support
- [ ] AI-powered рекомендации

---

## 🤝 Локальная разработка

### Запуск отдельного сервиса

```bash
# Запустить только инфраструктуру
docker-compose up -d postgres mongodb redis rabbitmq

# Разработка конкретного сервиса
cd flight-search-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

### Code Quality

```bash
# Formatting
black app/
isort app/

# Linting
flake8 app/
mypy app/

# Tests
pytest tests/ -v --cov=app
```

---

## 🐛 Troubleshooting

### Контейнеры не запускаются

```bash
# Проверить статус
docker-compose ps

# Посмотреть логи
docker-compose logs -f [service-name]

# Пересобрать образы
docker-compose down
docker-compose up -d --build
```

### Конфликт портов

```powershell
# Windows: проверить занятые порты
netstat -an | findstr "3000 8000 5432 27017"

# Linux/Mac
lsof -i :3000
```

Измените порты в `docker-compose.yml` при необходимости.

---

## 📄 Лицензия

MIT License — см. [LICENSE](LICENSE) файл

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) — Modern Python web framework
- [Django](https://www.djangoproject.com/) — Batteries-included framework
- [React](https://reactjs.org/) — UI library
- [shadcn/ui](https://ui.shadcn.com/) — Component library
- [Tailwind CSS](https://tailwindcss.com/) — CSS framework
- Travel Tech community за best practices

---

<div align="center">

### ⭐ Если проект полезен, поставьте звезду! ⭐

<p>Made with ❤️ for Travel Tech Industry</p>

[⬆ Back to Top](#-flighthub)

</div>
