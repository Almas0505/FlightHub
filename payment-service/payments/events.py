"""
Payment events - RabbitMQ publishing
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


def publish_payment_completed(payment):
    """Publish payment.completed event"""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Declare exchange
        channel.exchange_declare(
            exchange='payments',
            exchange_type='topic',
            durable=True
        )
        
        # Prepare message
        message = {
            'payment_id': str(payment.id),
            'booking_id': str(payment.booking_id),
            'user_id': str(payment.user_id),
            'amount': float(payment.amount),
            'currency': payment.currency,
            'status': payment.status,
            'transaction_id': payment.transaction_id,
            'payment_method': payment.payment_method,
        }
        
        # Publish
        channel.basic_publish(
            exchange='payments',
            routing_key='payment.completed',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent
                content_type='application/json'
            )
        )
        
        connection.close()
        logger.info(f"Published payment.completed for {payment.id}")
        
    except Exception as e:
        logger.error(f"Failed to publish payment.completed: {str(e)}")


def publish_payment_failed(payment):
    """Publish payment.failed event"""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        channel.exchange_declare(
            exchange='payments',
            exchange_type='topic',
            durable=True
        )
        
        message = {
            'payment_id': str(payment.id),
            'booking_id': str(payment.booking_id),
            'user_id': str(payment.user_id),
            'error_code': payment.error_code,
            'error_message': payment.error_message,
        }
        
        channel.basic_publish(
            exchange='payments',
            routing_key='payment.failed',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        
        connection.close()
        logger.info(f"Published payment.failed for {payment.id}")
        
    except Exception as e:
        logger.error(f"Failed to publish payment.failed: {str(e)}")


def publish_payment_refunded(payment):
    """Publish payment.refunded event"""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        channel.exchange_declare(
            exchange='payments',
            exchange_type='topic',
            durable=True
        )
        
        message = {
            'payment_id': str(payment.id),
            'booking_id': str(payment.booking_id),
            'user_id': str(payment.user_id),
            'refund_amount': float(payment.refund_amount),
            'refund_reason': payment.refund_reason,
        }
        
        channel.basic_publish(
            exchange='payments',
            routing_key='payment.refunded',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        
        connection.close()
        logger.info(f"Published payment.refunded for {payment.id}")
        
    except Exception as e:
        logger.error(f"Failed to publish payment.refunded: {str(e)}")
