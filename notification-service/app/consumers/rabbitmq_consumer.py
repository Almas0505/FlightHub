"""
RabbitMQ Consumer for notifications
"""
import pika
import json
import logging
import asyncio
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    """RabbitMQ consumer for notification events"""
    
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.email_service = EmailService()
        self.connection = None
        self.channel = None
        
    def connect(self):
        """Connect to RabbitMQ"""
        try:
            params = pika.URLParameters(self.rabbitmq_url)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            
            # Declare exchanges
            self.channel.exchange_declare(
                exchange='bookings',
                exchange_type='topic',
                durable=True
            )
            
            self.channel.exchange_declare(
                exchange='payments',
                exchange_type='topic',
                durable=True
            )
            
            # Declare queue
            self.channel.queue_declare(
                queue='notifications',
                durable=True
            )
            
            # Bind queue to routing keys
            self.channel.queue_bind(
                exchange='bookings',
                queue='notifications',
                routing_key='booking.created'
            )
            
            self.channel.queue_bind(
                exchange='bookings',
                queue='notifications',
                routing_key='booking.ticketed'
            )
            
            self.channel.queue_bind(
                exchange='bookings',
                queue='notifications',
                routing_key='booking.cancelled'
            )
            
            self.channel.queue_bind(
                exchange='bookings',
                queue='notifications',
                routing_key='booking.reminder'
            )
            
            self.channel.queue_bind(
                exchange='payments',
                queue='notifications',
                routing_key='payment.completed'
            )
            
            self.channel.queue_bind(
                exchange='payments',
                queue='notifications',
                routing_key='payment.failed'
            )
            
            logger.info("Connected to RabbitMQ")
            
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
            raise
    
    def callback(self, ch, method, properties, body):
        """Handle incoming messages"""
        try:
            # Parse message
            message = json.loads(body)
            routing_key = method.routing_key
            
            logger.info(f"Received {routing_key}: {message}")
            
            # Handle different event types
            if routing_key == 'booking.created':
                self.email_service.send_booking_confirmation(message)
                
            elif routing_key == 'booking.ticketed':
                self.email_service.send_ticket(message)
                
            elif routing_key == 'booking.cancelled':
                self.email_service.send_booking_cancellation(message)
                
            elif routing_key == 'booking.reminder':
                self.email_service.send_flight_reminder(message)
                
            elif routing_key == 'payment.completed':
                self.email_service.send_payment_confirmation(message)
                
            elif routing_key == 'payment.failed':
                self.email_service.send_payment_failure(message)
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            # Reject and requeue
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def start_consuming(self):
        """Start consuming messages"""
        try:
            self.connect()
            
            # Set QoS
            self.channel.basic_qos(prefetch_count=1)
            
            # Start consuming
            self.channel.basic_consume(
                queue='notifications',
                on_message_callback=self.callback
            )
            
            logger.info("Starting to consume messages...")
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
            self.stop()
        except Exception as e:
            logger.error(f"Consumer error: {str(e)}", exc_info=True)
            self.stop()
    
    def stop(self):
        """Stop consuming and close connection"""
        try:
            if self.channel and self.channel.is_open:
                self.channel.stop_consuming()
                self.channel.close()
            
            if self.connection and self.connection.is_open:
                self.connection.close()
            
            logger.info("Consumer stopped")
            
        except Exception as e:
            logger.error(f"Error stopping consumer: {str(e)}")


async def start_consumer_background(rabbitmq_url: str):
    """Start consumer in background"""
    consumer = RabbitMQConsumer(rabbitmq_url)
    
    # Run in executor to avoid blocking
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, consumer.start_consuming)
