# API Gateway Documentation

## Overview

FlightHub API Gateway служит единой точкой входа для всей микросервисной системы. Все клиентские запросы проходят через Gateway, который обеспечивает аутентификацию, rate limiting, кеширование и маршрутизацию к соответствующим микросервисам.

## Architecture

### Request Flow

```
Client Request
    ↓
[CORS Middleware]
    ↓
[Logging Middleware] - Логирование request/response
    ↓
[Rate Limit Middleware] - Проверка лимитов через Redis
    ↓
[Auth Middleware] - JWT валидация
    ↓
[Route Handler]
    ↓
[Cache Check] - Проверка Redis cache
    ↓
[Service Client] - HTTP запрос к микросервису
    ↓
[Circuit Breaker] - Защита от падающих сервисов
    ↓
Response to Client
```

## Middleware Components

### 1. Authentication Middleware

**Назначение**: JWT токен валидация

**Public Endpoints** (без аутентификации):
- `/` - Root
- `/docs` - API documentation
- `/health/*` - Health checks
- `/api/v1/users/register` - Регистрация
- `/api/v1/users/login` - Вход
- `/api/v1/flights/search` - Поиск рейсов

**Protected Endpoints**:
- Все остальные требуют `Authorization: Bearer <token>` header

**Headers**:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Token Payload**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "exp": 1698765432,
  "type": "access"
}
```

### 2. Rate Limiting Middleware

**Назначение**: Защита от DDoS и abuse

**Algorithm**: Sliding Window (Redis sorted sets)

**Limits**:
- Default: 100 requests per 60 seconds
- Per user (authenticated): tracked by user_id
- Per IP (anonymous): tracked by IP address

**Response Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 35
```

**Error Response** (429):
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Try again in 35 seconds."
}
```

### 3. Logging Middleware

**Назначение**: Структурированное логирование

**Log Format** (JSON):
```json
{
  "event": "request_completed",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "method": "GET",
  "path": "/api/v1/flights/search",
  "status_code": 200,
  "duration_ms": 142.5,
  "timestamp": "2025-10-17T10:30:00Z"
}
```

## Service Communication

### Service Client

**Features**:
- Async HTTP requests (aiohttp)
- Circuit Breaker pattern
- Automatic retries
- Timeout handling
- Error propagation

**Circuit Breaker States**:
1. **CLOSED**: Normal operation
2. **OPEN**: Service unavailable, fail fast
3. **HALF_OPEN**: Testing if service recovered

**Configuration**:
```python
CIRCUIT_BREAKER_THRESHOLD = 5  # failures before opening
CIRCUIT_BREAKER_TIMEOUT = 60    # seconds before retry
SERVICE_TIMEOUT = 30            # request timeout
```

### Error Handling

**Service Errors** map to HTTP codes:
- 400-499: Client errors (pass through)
- 500-599: Server errors (circuit breaker)
- Timeout: 504 Gateway Timeout
- Connection failed: 503 Service Unavailable

## Caching Strategy

### Cache Keys Pattern

```
{resource}:{params}:{values}
```

**Examples**:
```
flight_search:from:ALA:to:DXB:date:2025-11-01:passengers:1
popular_routes
```

### Cache TTL

- Flight searches: 5 minutes (300s)
- Popular routes: 1 hour (3600s)
- User profile: 15 minutes (900s)

### Cache Invalidation

```python
# Invalidate pattern
await CacheService.invalidate_pattern("flight_search:*")

# Delete specific key
await CacheService.delete("flight_search:ALA:DXB:...")
```

## API Endpoints

### Health Checks

#### GET /health/live
Liveness probe для Kubernetes

**Response**:
```json
{
  "status": "alive",
  "timestamp": "2025-10-17T10:30:00Z",
  "service": "api-gateway",
  "version": "1.0.0"
}
```

#### GET /health/ready
Readiness probe - проверяет зависимости

**Response** (200 OK):
```json
{
  "status": "ready",
  "timestamp": "2025-10-17T10:30:00Z",
  "checks": {
    "redis": true
  }
}
```

**Response** (503 Service Unavailable):
```json
{
  "status": "not_ready",
  "checks": {
    "redis": false
  }
}
```

### Flight Search

#### GET /api/v1/flights/search

**Query Parameters**:
- `from_airport` (required): IATA code (e.g., ALA)
- `to_airport` (required): IATA code (e.g., DXB)
- `departure_date` (required): YYYY-MM-DD
- `return_date` (optional): YYYY-MM-DD
- `passengers` (optional): 1-9 (default: 1)
- `cabin_class` (optional): economy|business|first

**Response**:
```json
{
  "results": [...],
  "total": 42,
  "from_cache": true,
  "search_id": "550e8400-..."
}
```

### Bookings

#### POST /api/v1/bookings

**Authentication**: Required

**Request Body**:
```json
{
  "flight_id": "FL12345",
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

**Response** (201 Created):
```json
{
  "id": "550e8400-...",
  "pnr": "ABC123",
  "status": "PENDING",
  "expires_at": "2025-10-17T11:00:00Z",
  "total_amount": 50000.00,
  "currency": "KZT"
}
```

#### GET /api/v1/bookings/{booking_id}

**Authentication**: Required

**Response**:
```json
{
  "id": "550e8400-...",
  "pnr": "ABC123",
  "status": "CONFIRMED",
  "flight_details": {...},
  "passengers": [...],
  "total_amount": 50000.00
}
```

### Payments

#### POST /api/v1/payments

**Authentication**: Required

**Request Body**:
```json
{
  "booking_id": "550e8400-...",
  "payment_method": "card",
  "card_token": "tok_visa_4242",
  "save_card": false
}
```

**Response** (201 Created):
```json
{
  "id": "payment-123",
  "booking_id": "550e8400-...",
  "amount": 50000.00,
  "currency": "KZT",
  "status": "completed",
  "created_at": "2025-10-17T10:30:00Z"
}
```

### Users

#### POST /api/v1/users/register

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepass123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+77001234567"
}
```

#### POST /api/v1/users/login

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1Qi...",
  "refresh_token": "eyJ0eXAiOiJKV1Qi...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## Error Responses

### Standard Error Format

```json
{
  "error": "Error Type",
  "message": "Human-readable message",
  "details": {
    "field": "error details"
  }
}
```

### Common Status Codes

- **200 OK**: Success
- **201 Created**: Resource created
- **400 Bad Request**: Validation error
- **401 Unauthorized**: Missing/invalid token
- **403 Forbidden**: No permission
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error
- **503 Service Unavailable**: Service down
- **504 Gateway Timeout**: Service timeout

## Security

### JWT Tokens

**Access Token**:
- Lifetime: 30 minutes
- Used for API requests
- Stored in memory (not localStorage)

**Refresh Token**:
- Lifetime: 7 days
- Used to get new access token
- HTTP-only cookie recommended

### Best Practices

1. Always use HTTPS in production
2. Rotate SECRET_KEY regularly
3. Implement token blacklist for logout
4. Use short-lived access tokens
5. Store refresh tokens securely
6. Validate all user input
7. Use parameterized queries
8. Enable CORS only for trusted origins

## Monitoring

### Metrics

Available via response headers:
- Request ID
- Response time
- Rate limit status

### Logging

All requests logged with:
- Request ID (for tracing)
- Method, path
- Status code
- Duration
- User ID (if authenticated)
- Errors and stack traces

### Alerts

Configure alerts for:
- High error rate (>5%)
- Slow responses (>1s p95)
- Rate limit hits (>100/min)
- Circuit breaker opens
- Service unavailable errors

## Performance Tips

1. **Enable caching** for frequently requested data
2. **Use pagination** for large result sets
3. **Compress responses** (gzip)
4. **Connection pooling** in service clients
5. **Async operations** everywhere
6. **Database indexes** in microservices
7. **CDN** for static assets

## Troubleshooting

### Gateway not starting

Check:
- Redis connection (`REDIS_URL`)
- Port 8000 not in use
- Environment variables loaded
- Dependencies installed

### High response times

Check:
- Redis performance
- Downstream service latency
- Circuit breaker status
- Database queries in services

### Authentication errors

Check:
- Token not expired
- Correct SECRET_KEY
- Token format correct
- Public endpoints configured

### Rate limiting issues

Check:
- Redis connection
- Rate limit configuration
- Client IP detection
- User ID in token
