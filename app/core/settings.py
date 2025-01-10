from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

class Settings(BaseSettings):
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()