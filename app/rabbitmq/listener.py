import aio_pika
import asyncio
from app.core.settings import settings
import logging

logger = logging.getLogger()

RABBITMQ_URL = f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/{settings.RABBITMQ_VHOST}"

async def on_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        message_payload: str = message.body.decode()
        logger.info(f"Received message: {message_payload}")

async def start_rabbitmq_listener():
    while True:
        try:
            logger.info(f"Connecting to RabbitMQ: {RABBITMQ_URL} ...")
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            logger.info(f"Connected to RabbitMQ: {RABBITMQ_URL}")
            async with connection:
                channel = await connection.channel()
                queue = await channel.declare_queue(settings.RABBITMQ_SUBSCRIBER_QUEUE, durable=True)
                logger.info(f"Waiting for messages in the queue {settings.RABBITMQ_SUBSCRIBER_QUEUE} ...")
                await queue.consume(on_message)
                await asyncio.Future()
        except aio_pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Connection failed: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)





