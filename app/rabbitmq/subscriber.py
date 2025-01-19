import asyncio
import aio_pika
import logging
from aio_pika.abc import AbstractIncomingMessage
from app.rabbitmq.connection import Connection


class Subscriber:
    def __init__(self, connection: Connection):
        self.connection: Connection = connection

    async def subscribe(self, queue_name: str):
        if not self.connection.is_connected():
            logging.error(f"Can't subscribe on RabbitMQ - not connected.")
            return
        try:
            logging.info(f"Subscribing for messages in queue [{queue_name}] ...")
            queue = await self.connection.get_channel().declare_queue(queue_name, durable=True)
            await queue.consume(self.on_message)
            await asyncio.Future()
        except aio_pika.exceptions.AMQPError as e:
            logging.error(f"Failed to subscribe on queue [{queue_name}]: {e}.")

    @staticmethod
    async def on_message(message: AbstractIncomingMessage):
        async with message.process():
            message_payload: str = message.body.decode()
            logging.info(f"Received message: [{message_payload}] from queue [{message.routing_key}]")