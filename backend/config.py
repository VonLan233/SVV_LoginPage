"""
SVV-LoginPage Configuration
Settings management using Pydantic BaseSettings with environment variable support
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support

    All settings can be overridden via environment variables or .env file.
    """

    # Database Configuration
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/svv_auth"
    )

    # JWT Configuration
    secret_key: str = os.getenv(
        "SECRET_KEY",
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Application Configuration
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
