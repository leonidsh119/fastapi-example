import aio_pika
import asyncio
from app.core.settings import settings
import logging

logger = logging.getLogger(__name__)

RABBITMQ_URL = f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/{settings.RABBITMQ_VHOST}"

async def on_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        message_payload: str = message.body.decode()
        logger.info(f"Received message: {message_payload}")
        print(f"Received message: {message_payload}")

async def start_rabbitmq_listener():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    logger.info(f"Connected to RabbitMQ: {RABBITMQ_URL}")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(settings.RABBITMQ_SUBSCRIBER_QUEUE, durable=True)
        logger.info(f"Listening on : {settings.RABBITMQ_SUBSCRIBER_QUEUE}")

        logger.info("Waiting for messages in the queue...")
        await queue.consume(on_message)

        # Keep the listener running
        await asyncio.Future()  # This will block forever, waiting for messages.

