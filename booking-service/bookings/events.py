"""
Booking events - RabbitMQ publishing
"""
import pika
import json
import logging
import os

logger = logging.getLogger(__name__)


def get_rabbitmq_connection():
    """Get RabbitMQ connection"""
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://admin:secret@localhost:5672')
    params = pika.URLParameters(rabbitmq_url)
    return pika.BlockingConnection(params)


def publish_booking_created(booking):
    """Publish booking.created event"""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Declare exchange
        channel.exchange_declare(
            exchange='bookings',
            exchange_type='topic',
            durable=True
        )
        
        # Prepare message
        message = {
            'booking_id': str(booking.id),
            'pnr': booking.pnr,
            'user_id': str(booking.user_id),
            'contact_email': booking.contact_email,
            'contact_phone': booking.contact_phone,
            'flight_number': booking.flight_number,
            'departure_airport': booking.departure_airport,
            'arrival_airport': booking.arrival_airport,
            'departure_time': booking.departure_time.isoformat(),
            'status': booking.status,
            'total_amount': float(booking.total_amount),
        }
        
        # Publish
        channel.basic_publish(
            exchange='bookings',
            routing_key='booking.created',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent
                content_type='application/json'
            )
        )
        
        connection.close()
        logger.info(f"Published booking.created for {booking.pnr}")
        
    except Exception as e:
        logger.error(f"Failed to publish booking.created: {str(e)}")


def publish_booking_cancelled(booking):
    """Publish booking.cancelled event"""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        channel.exchange_declare(
            exchange='bookings',
            exchange_type='topic',
            durable=True
        )
        
        message = {
            'booking_id': str(booking.id),
            'pnr': booking.pnr,
            'user_id': str(booking.user_id),
            'contact_email': booking.contact_email,
            'status': booking.status,
        }
        
        channel.basic_publish(
            exchange='bookings',
            routing_key='booking.cancelled',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        
        connection.close()
        logger.info(f"Published booking.cancelled for {booking.pnr}")
        
    except Exception as e:
        logger.error(f"Failed to publish booking.cancelled: {str(e)}")


def publish_booking_expired(booking):
    """Publish booking.expired event"""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        channel.exchange_declare(
            exchange='bookings',
            exchange_type='topic',
            durable=True
        )
        
        message = {
            'booking_id': str(booking.id),
            'pnr': booking.pnr,
            'user_id': str(booking.user_id),
            'contact_email': booking.contact_email,
        }
        
        channel.basic_publish(
            exchange='bookings',
            routing_key='booking.expired',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        
        connection.close()
        logger.info(f"Published booking.expired for {booking.pnr}")
        
    except Exception as e:
        logger.error(f"Failed to publish booking.expired: {str(e)}")


def publish_booking_ticketed(booking):
    """Publish booking.ticketed event"""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        channel.exchange_declare(
            exchange='bookings',
            exchange_type='topic',
            durable=True
        )
        
        message = {
            'booking_id': str(booking.id),
            'pnr': booking.pnr,
            'user_id': str(booking.user_id),
            'contact_email': booking.contact_email,
            'flight_number': booking.flight_number,
        }
        
        channel.basic_publish(
            exchange='bookings',
            routing_key='booking.ticketed',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        
        connection.close()
        logger.info(f"Published booking.ticketed for {booking.pnr}")
        
    except Exception as e:
        logger.error(f"Failed to publish booking.ticketed: {str(e)}")


def publish_booking_reminder(booking):
    """Publish booking.reminder event"""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        channel.exchange_declare(
            exchange='bookings',
            exchange_type='topic',
            durable=True
        )
        
        message = {
            'booking_id': str(booking.id),
            'pnr': booking.pnr,
            'user_id': str(booking.user_id),
            'contact_email': booking.contact_email,
            'contact_phone': booking.contact_phone,
            'flight_number': booking.flight_number,
            'departure_time': booking.departure_time.isoformat(),
        }
        
        channel.basic_publish(
            exchange='bookings',
            routing_key='booking.reminder',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        
        connection.close()
        logger.info(f"Published booking.reminder for {booking.pnr}")
        
    except Exception as e:
        logger.error(f"Failed to publish booking.reminder: {str(e)}")
