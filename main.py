import uvicorn
from app.core.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        app="app.app:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )
