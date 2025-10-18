# Flight Search Service

Асинхронный микросервис для поиска авиарейсов с агрегацией данных от нескольких провайдеров (GDS систем).

## 🚀 Особенности

- **Multi-Provider Search**: Агрегация результатов от Amadeus, Sabre и других GDS
- **Async/Await**: Полностью асинхронная архитектура на FastAPI
- **MongoDB**: Хранение расписаний и кеширование результатов
- **Redis**: Дополнительный кеш слой
- **Celery**: Фоновые задачи для обновления расписаний
- **Circuit Breaker**: Отказоустойчивость при падении провайдеров
- **Auto Documentation**: Swagger UI и ReDoc

## 📋 Требования

- Python 3.11+
- MongoDB 6+
- Redis 7+
- RabbitMQ 3+ (для Celery)
- Docker & Docker Compose (опционально)

## 🛠️ Установка

### Docker Compose (Рекомендуется)

```bash
# Клонировать и перейти в директорию
cd flight-search-service

# Скопировать .env
cp .env.example .env

# Запустить все сервисы
docker-compose up -d

# Проверить логи
docker-compose logs -f flight-search

# Seed sample airport data
curl -X POST http://localhost:8001/airports/seed
```

### Локальная установка

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Установить зависимости
pip install -r requirements.txt

# Настроить .env
cp .env.example .env
# Отредактировать .env с вашими настройками

# Запустить MongoDB
docker run -d -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  mongo:6

# Запустить Redis
docker run -d -p 6379:6379 redis:7-alpine

# Запустить RabbitMQ
docker run -d -p 5672:5672 -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=admin \
  -e RABBITMQ_DEFAULT_PASS=secret \
  rabbitmq:3-management-alpine

# Запустить приложение
uvicorn app.main:app --reload --port 8001

# В отдельном терминале запустить Celery Worker
celery -A app.tasks.celery_app worker -l info

# В третьем терминале запустить Celery Beat
celery -A app.tasks.celery_app beat -l info
```

## 🔧 Конфигурация

Основные настройки в `.env`:

```env
# MongoDB
MONGODB_URL=mongodb://admin:secret@localhost:27017
MONGODB_DB_NAME=flight_search

# Redis
REDIS_URL=redis://localhost:6379

# Celery
CELERY_BROKER_URL=amqp://admin:secret@localhost:5672
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# GDS Providers
AMADEUS_API_KEY=your_api_key
AMADEUS_API_SECRET=your_api_secret
USE_MOCK_PROVIDER=True

# Search Settings
MAX_CONCURRENT_SEARCHES=3
SEARCH_TIMEOUT_SECONDS=30
MAX_RESULTS_PER_PROVIDER=50
```

## 📚 API Документация

После запуска доступна по адресам:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## 🛣️ API Endpoints

### Flight Search

#### GET /search
Поиск авиарейсов

```bash
curl "http://localhost:8001/search?\
from_airport=ALA&\
to_airport=DXB&\
departure_date=2025-11-01&\
passengers=1&\
cabin_class=economy"
```

**Параметры:**
- `from_airport` (required): IATA код аэропорта отправления
- `to_airport` (required): IATA код аэропорта прибытия
- `departure_date` (required): Дата вылета (YYYY-MM-DD)
- `return_date` (optional): Дата возврата
- `passengers` (optional): Количество пассажиров (1-9, default: 1)
- `cabin_class` (optional): economy/business/first (default: economy)
- `direct_only` (optional): Только прямые рейсы (default: false)

**Ответ:**
```json
{
  "search_id": "550e8400-...",
  "flights": [...],
  "total": 15,
  "from_cache": false,
  "search_duration_ms": 1234.56,
  "providers_used": ["mock", "amadeus"]
}
```

#### GET /flights/{flight_id}
Детальная информация о рейсе

```bash
curl http://localhost:8001/flights/FL-abc123def456
```

#### GET /popular-routes
Популярные маршруты

```bash
curl http://localhost:8001/popular-routes
```

### Airports

#### GET /airports
Поиск аэропортов

```bash
# По IATA коду
curl "http://localhost:8001/airports?query=ALA"

# По городу
curl "http://localhost:8001/airports?query=Almaty"
```

#### GET /airports/{iata_code}
Информация об аэропорте

```bash
curl http://localhost:8001/airports/ALA
```

#### GET /airports/popular/list
Популярные аэропорты

```bash
curl http://localhost:8001/airports/popular/list
```

#### POST /airports/seed
Загрузить тестовые данные аэропортов

```bash
curl -X POST http://localhost:8001/airports/seed
```

### Health Checks

```bash
# Liveness probe
curl http://localhost:8001/health/live

# Readiness probe
curl http://localhost:8001/health/ready

# General health
curl http://localhost:8001/health
```

## 🏗️ Архитектура

```
Flight Search Service
│
├── FastAPI Application
│   ├── Routes (API Endpoints)
│   ├── Models (Pydantic schemas)
│   └── Services (Business logic)
│
├── Search Engine
│   ├── Provider Management
│   ├── Parallel Search
│   ├── Result Aggregation
│   └── Deduplication
│
├── Providers
│   ├── Mock Provider (testing)
│   ├── Amadeus GDS
│   ├── Sabre GDS
│   └── Base Provider Interface
│
├── Databases
│   ├── MongoDB (flights, airports, cache)
│   └── Redis (fast cache)
│
└── Background Tasks (Celery)
    ├── Update flight schedules
    ├── Cleanup expired cache
    └── Refresh popular routes
```

### Search Flow

```
1. Client Request
    ↓
2. Check MongoDB Cache (5 min TTL)
    ↓
3. If not cached:
   → Search all providers in parallel
   → Aggregate results
   → Deduplicate
   → Sort by price
    ↓
4. Save to cache
    ↓
5. Return results
```

### Provider Integration

```python
class BaseFlightProvider(ABC):
    async def search_flights(self, request) -> List[Flight]:
        """Override in subclass"""
        pass
```

Провайдеры:
- **MockProvider**: Генерирует реалистичные тестовые данные
- **AmadeusProvider**: Интеграция с Amadeus GDS API
- **SabreProvider**: Интеграция с Sabre GDS API (TODO)

## 🧪 Тестирование

```bash
# Запустить тесты
pytest -v

# С покрытием
pytest --cov=app --cov-report=html

# Конкретный тест
pytest tests/test_search.py -v
```

## 📊 Мониторинг

### Celery Tasks

```bash
# Просмотр задач через RabbitMQ Management
open http://localhost:15672
# Login: admin / secret

# Мониторинг Celery
celery -A app.tasks.celery_app inspect active
celery -A app.tasks.celery_app inspect scheduled
```

### MongoDB

```bash
# Подключиться к MongoDB
mongosh mongodb://admin:secret@localhost:27017

# Проверить данные
use flight_search
db.flights.countDocuments()
db.airports.countDocuments()
db.search_cache.countDocuments()
```

## 🔄 Фоновые задачи (Celery)

### Периодические задачи

1. **update_flight_schedules** - Каждые 30 минут
   - Обновление расписаний от провайдеров
   - Инвалидация устаревших данных

2. **cleanup_expired_cache** - Каждый час
   - Удаление устаревшего кеша
   - Освобождение места в MongoDB

3. **refresh_popular_routes** - По требованию
   - Анализ популярных маршрутов
   - Обновление рекомендаций

### Ручной запуск задач

```python
from app.tasks.update_flights import update_flight_schedules

# Асинхронно
result = update_flight_schedules.delay()
print(result.id)

# Синхронно (для тестирования)
result = update_flight_schedules()
```

## 🚀 Production Deployment

### Environment Variables

```env
ENVIRONMENT=production
DEBUG=False
MONGODB_URL=mongodb://user:pass@mongodb-prod:27017
REDIS_URL=redis://redis-prod:6379
AMADEUS_API_KEY=real_production_key
USE_MOCK_PROVIDER=False
```

### Docker

```bash
docker build -t flight-search-service:1.0.0 .
docker run -p 8001:8001 \
  -e MONGODB_URL=$MONGODB_URL \
  -e REDIS_URL=$REDIS_URL \
  flight-search-service:1.0.0
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flight-search
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: flight-search
        image: flight-search-service:1.0.0
        ports:
        - containerPort: 8001
        env:
        - name: MONGODB_URL
          valueFrom:
            secretKeyRef:
              name: mongodb-secret
              key: url
```

## 📈 Performance

- **Search latency**: ~500ms (mock provider)
- **Cache hit rate**: ~70% (5 min TTL)
- **Concurrent searches**: 3 providers в параллель
- **MongoDB operations**: Индексированные запросы
- **Memory usage**: ~200MB base + results

## 🔐 Security

- MongoDB authentication
- Redis password (optional)
- RabbitMQ credentials
- API keys for GDS providers
- Input validation (Pydantic)
- Rate limiting (через API Gateway)

## 🐛 Troubleshooting

### Service not starting

```bash
# Проверить логи
docker-compose logs flight-search

# Проверить зависимости
docker-compose ps
```

### MongoDB connection error

```bash
# Проверить MongoDB
docker exec -it flight-search-mongodb mongosh

# Проверить URL в .env
echo $MONGODB_URL
```

### No search results

```bash
# Проверить провайдеры
curl http://localhost:8001/health

# Проверить логи
docker-compose logs -f flight-search
```

### Celery tasks not running

```bash
# Проверить worker
docker-compose logs celery-worker

# Проверить beat
docker-compose logs celery-beat

# Проверить RabbitMQ
open http://localhost:15672
```

## 🤝 Интеграция с другими сервисами

### API Gateway Integration

API Gateway проксирует запросы к этому сервису:

```
GET /api/v1/flights/search → http://flight-search:8001/search
GET /api/v1/flights/airports → http://flight-search:8001/airports
```

### Booking Service Integration

Booking Service использует flight_id для создания бронирований:

```python
# Get flight details
flight = await get_flight_by_id(flight_id)

# Create booking with flight data
booking = create_booking(user, flight, passengers)
```

## 📝 Добавление нового провайдера

```python
# 1. Создать класс провайдера
class NewProvider(BaseFlightProvider):
    async def search_flights(self, request):
        # Implement search logic
        pass

# 2. Добавить в SearchEngine
def __init__(self):
    self.providers = [
        MockProvider(),
        AmadeusProvider(),
        NewProvider(),  # Add here
    ]
```

## 📄 Лицензия

MIT License

## 👥 Контакты

FlightHub Development Team
