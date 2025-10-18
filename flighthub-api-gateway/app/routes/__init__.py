"""
Routes package
"""
from app.routes import health, flights, bookings, users, payments

__all__ = [
    "health",
    "flights",
    "bookings",
    "users",
    "payments",
]
