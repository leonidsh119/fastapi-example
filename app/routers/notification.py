from fastapi import APIRouter
from app.models.message import MessageRequest
from app.rabbitmq.publisher import send_message

router = APIRouter()

@router.post("/")
async def publish_message(request: MessageRequest):
    await send_message(request.message)
    return {"status": "Message sent", "message.py": request.message}