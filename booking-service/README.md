# Booking Service

Django REST Framework service for managing flight bookings.

## Quick Start
```bash
docker-compose up -d
python manage.py migrate
python manage.py runserver 8002
```

## Features
- Create/Cancel bookings
- PNR generation
- Auto-expiry (15 min)
- Celery tasks
- Event publishing

## API Endpoints
- POST /bookings/ - Create booking
- GET /bookings/ - List bookings
- GET /bookings/{id}/ - Get booking
- POST /bookings/{id}/cancel/ - Cancel
- GET /bookings/{id}/ticket/ - Get ticket
