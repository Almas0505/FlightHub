"""
Payment service URLs
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payments.views import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
