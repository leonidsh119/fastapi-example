from fastapi import APIRouter
from app.services import health
from app.models.health import Healthcheck

router = APIRouter()

@router.get("/", response_model=Healthcheck)
async def health_check():
    healthcheck = health.get_health_status()
    if healthcheck.status == "Healthy":
        return healthcheck
    else:
        return healthcheck, 503
