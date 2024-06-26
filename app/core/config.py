from typing import Any, Dict, Optional, ClassVar
from pydantic import EmailStr, field_validator, BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_URI: Optional[str] = None

    @field_validator("POSTGRES_URI", mode='before')
    def validate_postgres_conn(cls, values: Dict[str, Any], field: str) -> Any:
        password = "password"
        return "postgresql+asyncpg://"+os.getenv("POSTGRES_USER")+":"+os.getenv("POSTGRES_PASSWORD")+ "@" + os.getenv("POSTGRES_HOST")+"/" + os.getenv("POSTGRES_DB")


settings = Settings()
