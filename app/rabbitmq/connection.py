import aio_pika
import logging
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, NoneType, AbstractRobustQueue, \
    AbstractExchange


class Connection:
    def __init__(self):
        self.connection: AbstractRobustConnection = NoneType
        self.channel: AbstractRobustChannel = NoneType
        self.connected: bool = False

    def is_connected(self):
        return self.connected

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

    async def declare_queue(self, queue_name: str, is_durable: bool = True) -> AbstractRobustQueue:
        if not self.connected:
            logging.warning(f"Connection not initialized. Call connect() method first.")
            return NoneType
        try:
            logging.info(f"Declaring queue: [{queue_name}] ...")
            return await self.channel.declare_queue(queue_name, durable=is_durable)
        except aio_pika.exceptions.AMQPConnectionError as e:
            logging.error(f"Failed declaring queue [{queue_name}]]: {e}.")

    def get_default_exchange(self) -> AbstractExchange:
        if not self.connected:
            logging.warning(f"Connection not initialized. Call connect() method first.")
            return NoneType
        return self.channel.default_exchange