import asyncio
import logging
from logging import config
from fastapi import FastAPI
from app.routers import health
from app.routers import items
from app.routers import notification
from app.rabbitmq.listener import start_rabbitmq_listener
from app.core.settings import settings
from pathlib import Path

config.fileConfig(fname=Path(__file__).resolve().parent.parent / "logging.conf")

app = FastAPI(
    title="My FastAPI Project",
    description="This is a modular FastAPI project with a health check.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(notification.router, prefix="/notification", tags=["notification"])

@app.on_event("startup")
async def startup_event():
    # Start the RabbitMQ listener in the background
    asyncio.create_task(start_rabbitmq_listener())
    logging.info(f"FastAPI application started. Listening on RabbitMQ at {settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}.")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("FastAPI application shutting down...")