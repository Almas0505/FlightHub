"""
Celery configuration for booking service
"""
import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_service.settings')

app = Celery('booking_service')

# Load config from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'expire-pending-bookings-every-minute': {
        'task': 'bookings.tasks.expire_pending_bookings',
        'schedule': 60.0,  # Every minute
    },
    'cleanup-old-bookings-daily': {
        'task': 'bookings.tasks.cleanup_old_bookings',
        'schedule': 86400.0,  # Daily
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
