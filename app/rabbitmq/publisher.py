import aio_pika
from app.core.settings import settings
import logging

RABBITMQ_URL = f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/{settings.RABBITMQ_VHOST}"

async def send_message(message: str):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(settings.RABBITMQ_PUBLISHER_QUEUE, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=settings.RABBITMQ_PUBLISHER_QUEUE
        )
        logging.info(f"Sent message: {message}")