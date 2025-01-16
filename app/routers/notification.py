from fastapi import APIRouter
from app.models.message import MessageRequest
from app.rabbitmq.publisher import Publisher
from app.core.settings import settings

router = APIRouter()

RABBITMQ_URL = f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/{settings.RABBITMQ_VHOST}"

@router.post("/")
async def publish_message(request: MessageRequest):
    publisher = Publisher(RABBITMQ_URL, settings.RABBITMQ_PUBLISHER_QUEUE)
    await publisher.publish(request.message)
    return {
        "status": "Message sent",
        "message": request.message
    }