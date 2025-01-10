from fastapi import APIRouter
from app.services import health

router = APIRouter()

@router.get("/")
async def health_check():
    status = health.get_health_status()
    if status["status"] == "healthy":
        return status
    else:
        return status, 503
