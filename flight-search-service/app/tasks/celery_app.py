"""
Celery application for background tasks
"""
from celery import Celery
from app.config import settings

# Create Celery app
celery_app = Celery(
    "flight_search",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.update_flights"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    task_soft_time_limit=240,  # 4 minutes
)

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "update-flight-data-every-30-minutes": {
        "task": "app.tasks.update_flights.update_flight_schedules",
        "schedule": 1800.0,  # 30 minutes
    },
    "cleanup-expired-cache-every-hour": {
        "task": "app.tasks.update_flights.cleanup_expired_cache",
        "schedule": 3600.0,  # 1 hour
    },
}
