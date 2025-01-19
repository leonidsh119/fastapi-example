import aio_pika
import logging
from app.rabbitmq.connection import Connection


class Publisher:
    def __init__(self, connection: Connection):
        self.connection: Connection = connection

    async def publish(self, message: str, queue_name: str):
        if not self.connection.is_connected():
            logging.error(f"Can't publish to RabbitMQ - not connected.")
            return
        try:
            logging.info(f"Sending message: [{message}] to queue [{queue_name}] ...")
            await self.connection.get_channel().declare_queue(queue_name, durable=True)
            await self.connection.get_channel().default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=queue_name
            )
            logging.info(f"Sent message: [{message}].")
        except aio_pika.exceptions.AMQPError as e:
            logging.error(f"Failed to publish message: {e}.")
