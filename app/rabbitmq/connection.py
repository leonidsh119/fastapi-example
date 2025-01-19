# import aio_pika
# import logging
#
#
# class Connection:
#     def __init__(self, user, password, host, port, vhost):
#         self.url = f"amqp://{user}:{password}@{host}:{port}/{vhost}"
#
#     def connect(self):
#         try:
#             logging.info(f"Connecting to RabbitMQ: {RABBITMQ_URL} ...")
#             connection = await aio_pika.connect_robust(RABBITMQ_URL)
#             logging.info(f"Connected to RabbitMQ: {RABBITMQ_URL}")
#         except aio_pika.exceptions.AMQPConnectionError as e:
#             logging.error(f"Connection failed: {e}. Retrying in 5 seconds...")
#             await asyncio.sleep(5)
