# FlightHub API Gateway

Единая точка входа для микросервисной системы бронирования авиабилетов FlightHub.

## 🚀 Особенности

- **Unified API**: Единый интерфейс для всех микросервисов
- **JWT Authentication**: Безопасная аутентификация с JWT токенами
- **Rate Limiting**: Защита от DDoS через Redis
- **Caching**: Кеширование популярных запросов
- **Circuit Breaker**: Отказоустойчивость при падении сервисов
- **Request Logging**: Структурированное логирование всех запросов
- **Health Checks**: Kubernetes-совместимые health/liveness/readiness проверки
- **Auto Documentation**: Swagger UI и ReDoc

## 📋 Требования

- Python 3.11+
- Redis 7+
- Docker & Docker Compose (опционально)

## 🛠️ Установка

### Локальная разработка

```bash
# Клонировать репозиторий
git clone <repository-url>
cd flighthub-api-gateway

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Скопировать .env файл
cp .env.example .env

# Отредактировать .env с вашими настройками
nano .env
```

### Docker

```bash
# Собрать и запустить
docker-compose up -d

# Проверить логи
docker-compose logs -f api-gateway

# Остановить
docker-compose down
```

## 🔧 Конфигурация

Основные переменные окружения в `.env`:

```env
# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://localhost:6379

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Microservices URLs
FLIGHT_SEARCH_URL=http://localhost:8001
BOOKING_SERVICE_URL=http://localhost:8002
PAYMENT_SERVICE_URL=http://localhost:8003
USER_SERVICE_URL=http://localhost:8005
```

## 🚦 Запуск

### Development

```bash
# С hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
# С Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📚 API Документация

После запуска доступна документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔑 Аутентификация

API использует JWT токены для аутентификации.

### Регистрация

```bash
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Вход

```bash
curl -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

Ответ:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Использование токена

```bash
curl http://localhost:8000/api/v1/bookings \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🛣️ Основные эндпоинты

### Поиск рейсов

```http
GET /api/v1/flights/search?from_airport=ALA&to_airport=DXB&departure_date=2025-11-01&passengers=1
```

### Создание бронирования

```http
POST /api/v1/bookings
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
  "flight_id": "FL123",
  "passengers": [
    {
      "title": "MR",
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "1990-01-01",
      "passport_number": "N12345678",
      "nationality": "KZ"
    }
  ],
  "contact_email": "user@example.com",
  "contact_phone": "+77001234567"
}
```

### Оплата

```http
POST /api/v1/payments
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
  "booking_id": "BK12345",
  "payment_method": "card",
  "card_token": "tok_visa_4242"
}
```

## 🧪 Тестирование

```bash
# Запустить все тесты
pytest

# С покрытием кода
pytest --cov=app --cov-report=html

# Запустить конкретный тест
pytest tests/test_health.py -v

# Асинхронные тесты
pytest tests/test_cache.py -v
```

## 📊 Мониторинг

### Health Checks

```bash
# Liveness probe (для Kubernetes)
curl http://localhost:8000/health/live

# Readiness probe
curl http://localhost:8000/health/ready

# General health
curl http://localhost:8000/health
```

### Метрики

API Gateway возвращает custom headers:
- `X-Request-ID`: Уникальный ID запроса
- `X-Response-Time`: Время обработки в миллисекундах
- `X-RateLimit-Limit`: Лимит запросов
- `X-RateLimit-Remaining`: Оставшиеся запросы
- `X-RateLimit-Reset`: Время сброса лимита

## 🏗️ Архитектура

```
API Gateway
├── Authentication (JWT)
├── Rate Limiting (Redis)
├── Caching (Redis)
├── Circuit Breaker
└── Service Routing
    ├── Flight Search Service
    ├── Booking Service
    ├── Payment Service
    ├── User Service
    └── Notification Service
```

### Middleware Stack

1. **LoggingMiddleware**: Логирование запросов/ответов
2. **RateLimitMiddleware**: Rate limiting через Redis
3. **AuthMiddleware**: JWT аутентификация

### Service Communication

- **HTTP/REST**: Асинхронные запросы через `aiohttp`
- **Circuit Breaker**: Автоматическое отключение неработающих сервисов
- **Timeouts**: Настраиваемые таймауты для каждого сервиса
- **Retries**: Автоматические повторы при временных ошибках

## 🔒 Безопасность

- JWT токены с коротким временем жизни (30 минут)
- Refresh токены для обновления (7 дней)
- Rate limiting для защиты от DDoS
- CORS настройки
- Валидация всех входных данных
- Защита от SQL injection (через ORM в других сервисах)

## 📈 Performance

- **Кеширование**: Популярные поиски кешируются на 5 минут
- **Асинхронность**: Все I/O операции асинхронные
- **Connection pooling**: Переиспользование соединений
- **Gzip compression**: Автоматическое сжатие ответов
- **Database connection pooling**: В микросервисах

## 🐳 Docker Deployment

### Простой запуск

```bash
docker build -t flighthub-api-gateway .
docker run -p 8000:8000 \
  -e REDIS_URL=redis://redis:6379 \
  -e SECRET_KEY=your-secret-key \
  flighthub-api-gateway
```

### Docker Compose

```bash
docker-compose up -d
```

### Kubernetes

См. `k8s/` директорию для Kubernetes манифестов.

## 🔧 Development

### Code Style

```bash
# Format code
black app/

# Sort imports
isort app/

# Lint
flake8 app/

# Type checking
mypy app/
```

### Pre-commit Hook

```bash
pip install pre-commit
pre-commit install
```

## 📝 Логирование

API использует структурированное логирование (structlog):

```python
logger.info(
    "request_completed",
    request_id=request_id,
    method=request.method,
    path=request.url.path,
    status_code=response.status_code,
    duration_ms=duration
)
```

Логи выводятся в JSON формате для удобной обработки.

## 🤝 Вклад в проект

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

MIT License

## 👥 Авторы

FlightHub Development Team

## 📞 Поддержка

- Email: support@flighthub.com
- Issues: GitHub Issues
- Slack: #flighthub-support
