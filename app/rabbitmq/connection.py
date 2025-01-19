import aio_pika
import logging
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, NoneType


class Connection:
    def __init__(self):
        self.connection: AbstractRobustConnection = NoneType
        self.channel: AbstractRobustChannel = NoneType
        self.connected: bool = False

    def is_connected(self):
        return self.connected

    def get_channel(self) -> AbstractRobustChannel:
        return self.channel

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
            await self.channel.close()
            await self.connection.close()
            logging.info(f"Disconnected from RabbitMQ.")
            self.channel = NoneType
            self.connection = NoneType
            self.connected = False
        except aio_pika.exceptions.AMQPConnectionError as e:
            logging.error(f"Failed to disconnect from RabbitMQ: {e}.")
