from fastapi import FastAPI
from app.routers import health
from app.routers import items

import asyncio
from app.rabbitmq.listener import start_rabbitmq_listener
from app.core.settings import settings

app = FastAPI(
    title="My FastAPI Project",
    description="This is a modular FastAPI project with a health check.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(items.router, prefix="/items", tags=["items"])

@app.on_event("startup")
async def startup_event():
    # Start the RabbitMQ listener in the background
    asyncio.create_task(start_rabbitmq_listener())
    print(f"FastAPI application started. Listening on RabbitMQ at {settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}.")

@app.on_event("shutdown")
async def shutdown_event():
    print("FastAPI application shutting down...")