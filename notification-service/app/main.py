from fastapi import FastAPI
from datetime import datetime
from contextlib import asynccontextmanager
import asyncio
import os
import logging
from app.consumers.rabbitmq_consumer import start_consumer_background

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Consumer task
consumer_task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events - startup and shutdown"""
    global consumer_task
    
    # Startup
    logger.info("Starting Notification Service...")
    
    # Start RabbitMQ consumer in background
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://admin:secret@rabbitmq:5672')
    consumer_task = asyncio.create_task(start_consumer_background(rabbitmq_url))
    logger.info("RabbitMQ consumer started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Notification Service...")
    if consumer_task:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
    logger.info("Consumer stopped")


app = FastAPI(
    title="Notification Service",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Notification Service",
        "status": "operational",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "consumer": "running" if consumer_task and not consumer_task.done() else "stopped"
    }


@app.post("/send")
async def send_notification(recipient: str, message: str, type: str = "email"):
    """Manual notification sending endpoint (for testing)"""
    from app.services.email_service import EmailService
    
    try:
        email_service = EmailService()
        
        if type == "email":
            email_service.send_email(
                to_email=recipient,
                subject="Test Notification",
                html_body=f"<html><body><p>{message}</p></body></html>"
            )
            return {"status": "sent", "recipient": recipient, "type": type}
        else:
            return {"status": "error", "message": f"Unsupported notification type: {type}"}
    
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        return {"status": "error", "message": str(e)}
