"""
URL configuration for booking service
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'booking-service',
        'version': '1.0.0'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('bookings/', include('bookings.urls')),
]
