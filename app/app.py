from fastapi import FastAPI
from app.routers import health
from app.routers import items

app = FastAPI(
    title="My FastAPI Project",
    description="This is a modular FastAPI project with a health check.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(items.router, prefix="/items", tags=["items"])
