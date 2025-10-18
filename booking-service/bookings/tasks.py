"""
Booking tasks - Celery
"""
from celery import shared_task
from django.utils import timezone
from .models import Booking, BookingStatus
import logging

logger = logging.getLogger(__name__)


@shared_task
def expire_pending_bookings():
    """
    Expire bookings that passed their expiry time
    Runs every minute
    """
    expired_bookings = Booking.objects.filter(
        status=BookingStatus.PENDING,
        expires_at__lt=timezone.now()
    )
    
    count = expired_bookings.count()
    
    if count > 0:
        expired_bookings.update(status=BookingStatus.EXPIRED)
        logger.info(f"Expired {count} pending bookings")
        
        # Publish events for each expired booking
        for booking in expired_bookings:
            try:
                from .events import publish_booking_expired
                publish_booking_expired(booking)
            except Exception as e:
                logger.error(f"Failed to publish booking.expired event: {str(e)}")
    
    return count


@shared_task
def cleanup_old_bookings():
    """
    Delete old cancelled/expired bookings older than 30 days
    Runs daily
    """
    from datetime import timedelta
    
    threshold = timezone.now() - timedelta(days=30)
    
    old_bookings = Booking.objects.filter(
        status__in=[BookingStatus.CANCELLED, BookingStatus.EXPIRED],
        created_at__lt=threshold
    )
    
    count = old_bookings.count()
    
    if count > 0:
        old_bookings.delete()
        logger.info(f"Cleaned up {count} old bookings")
    
    return count


@shared_task
def send_booking_reminder(booking_id):
    """
    Send reminder 24 hours before flight
    """
    try:
        booking = Booking.objects.get(id=booking_id)
        
        # Check if booking is still valid
        if booking.status not in [BookingStatus.CONFIRMED, BookingStatus.TICKETED]:
            logger.warning(f"Booking {booking.pnr} is {booking.status}, skipping reminder")
            return
        
        # Publish reminder event
        from .events import publish_booking_reminder
        publish_booking_reminder(booking)
        
        logger.info(f"Reminder sent for booking {booking.pnr}")
        
    except Booking.DoesNotExist:
        logger.error(f"Booking {booking_id} not found")
    except Exception as e:
        logger.error(f"Failed to send reminder for booking {booking_id}: {str(e)}")


@shared_task
def process_booking_payment(booking_id, payment_id):
    """
    Process successful payment and update booking status
    """
    try:
        booking = Booking.objects.get(id=booking_id)
        
        if booking.status != BookingStatus.PENDING:
            logger.warning(f"Booking {booking.pnr} is already {booking.status}")
            return
        
        # Confirm booking
        booking.confirm()
        
        # Issue ticket
        from tickets.services import TicketService
        ticket_service = TicketService()
        ticket_service.issue_ticket(booking)
        
        # Update status to ticketed
        booking.status = BookingStatus.TICKETED
        booking.save()
        
        # Publish event
        from .events import publish_booking_ticketed
        publish_booking_ticketed(booking)
        
        logger.info(f"Booking {booking.pnr} processed successfully")
        
    except Booking.DoesNotExist:
        logger.error(f"Booking {booking_id} not found")
    except Exception as e:
        logger.error(f"Failed to process booking {booking_id}: {str(e)}", exc_info=True)
