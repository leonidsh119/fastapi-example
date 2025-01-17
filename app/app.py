import asyncio
import logging
from logging import config
from fastapi import FastAPI
from pathlib import Path
from contextlib import asynccontextmanager

from app.routers import health
from app.routers import items
from app.routers import notification
from app.core.settings import settings
from app.core.dependencies import rabbitmq_connection, publisher, subscriber

config.fileConfig(fname=Path(__file__).resolve().parent.parent / "logging.conf")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event - runs when the app starts
    asyncio.create_task(initialize_rabbitmq_connection())
    logging.info(f"FastAPI application started. Listening on RabbitMQ at {settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}.")

    # Yield control to FastAPI to continue running the app
    yield

    # Shutdown event - runs when the app shuts down
    logging.info("FastAPI application is shutting down...")
    asyncio.create_task(rabbitmq_connection.disconnect())

async def initialize_rabbitmq_connection():
    await rabbitmq_connection.connect(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD, settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, settings.RABBITMQ_VHOST)
    asyncio.create_task(subscriber.subscribe(settings.RABBITMQ_SUBSCRIBER_QUEUE))

app = FastAPI(
    title="My FastAPI Project",
    description="This is a modular FastAPI project with a health check.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(notification.router, prefix="/notification", tags=["notification"])