import aio_pika
import logging
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, NoneType


class Publisher:
    def __init__(self):
        self.connection: AbstractRobustConnection = NoneType
        self.channel: AbstractRobustChannel = NoneType
        self.connected: bool = False

    async def connect(self, user: str, password: str, host: str, port: str, vhost: str):
        if self.connected:
            logging.warning(f"Already connected.")
            return
        try:
            connection_url = f"amqp://{user}:{password}@{host}:{port}/{vhost}"
            logging.info(f"Connecting to RabbitMQ: {connection_url} ...")
            self.connection = await aio_pika.connect_robust(connection_url)
            logging.info(f"Connected to RabbitMQ: {connection_url}")
            self.channel = await self.connection.channel()
            self.connected = True
        except aio_pika.exceptions.AMQPConnectionError as e:
            logging.error(f"Connection failed: {e}.")
            self.connected = False

    async def disconnect(self):
        if not self.connected:
            logging.warning(f"Already disconnected.")
            return
        try:
            logging.info(f"Disconnecting from RabbitMQ ...")
            await self.channel.close()  # Close the channel
            await self.connection.close()  # Close the connection
            logging.info(f"Disconnected from RabbitMQ.")
            self.channel = NoneType
            self.connection = NoneType
            self.connected = False
        except aio_pika.exceptions.AMQPConnectionError as e:
            logging.error(f"Failed to disconnect from RabbitMQ: {e}.")

    async def publish(self, message: str, queue_name: str):
        if not self.connected:
            logging.error(f"Can't publish to RabbitMQ - not connected.")
            return
        try:
            logging.info(f"Declaring queue: [{queue_name}] ...")
            await self.channel.declare_queue(queue_name, durable=True)  # Declare queue
            logging.info(f"Sending message: [{message}] ...")
            await self.channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=queue_name
            )
            logging.info(f"Sent message: [{message}].")
        except aio_pika.exceptions.AMQPError as e:
            logging.error(f"Failed to publish message: {e}.")
