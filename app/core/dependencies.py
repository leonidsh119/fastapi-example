from app.rabbitmq.connection import Connection
from app.rabbitmq.publisher import Publisher
from app.rabbitmq.subscriber import Subscriber

rabbitmq_connection = Connection()

publisher = Publisher(rabbitmq_connection)

subscriber = Subscriber(rabbitmq_connection)