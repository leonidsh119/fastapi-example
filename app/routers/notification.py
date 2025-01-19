from fastapi import APIRouter
from app.models.message import MessageRequest
from app.core.dependencies import publisher
from app.core.settings import settings

router = APIRouter()

@router.post("/")
async def publish_message(request: MessageRequest):
    await publisher.publish(request.message, settings.RABBITMQ_PUBLISHER_QUEUE)
    return {
        "status": "Message sent",
        "message": request.message
    }