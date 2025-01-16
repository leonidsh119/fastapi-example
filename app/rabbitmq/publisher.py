import aio_pika
import logging


class Publisher:
    def __init__(self, connection_url: str, queue_name: str):
        self.connection_url = connection_url
        self.queue_name = queue_name


    async def publish(self, message: str):
        connection = await aio_pika.connect_robust(self.connection_url)
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(self.queue_name, durable=True)
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=self.queue_name
            )
            logging.info(f"Sent message: {message}")


