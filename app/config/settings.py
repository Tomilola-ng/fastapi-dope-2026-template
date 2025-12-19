"""
Core configuration
"""

import os
from typing import Literal


from dotenv import load_dotenv
from pydantic_settings import BaseSettings


# Load environment variables from .env file
load_dotenv()


class AppSettings(BaseSettings):
    """Settings Class"""

    PROJECT_NAME: str = "Fast_Template"
    DATABASE_URL: str = (
        os.getenv("DATABASE_URL")
    )
    ENVIRONMENT: Literal["local", "staging", "production"] = os.getenv(
        "ENVIRONMENT", "local"
    )
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER", "hello@fast_template.com")
    ZEPTO_API_KEY: str = os.getenv("ZEPTO_API_KEY")

    # R2 Storage Configuration
    R2_ENDPOINT_URL: str = os.getenv("R2_ENDPOINT_URL")
    R2_ACCESS_KEY_ID: str = os.getenv("R2_ACCESS_KEY_ID")
    R2_SECRET_ACCESS_KEY: str = os.getenv("R2_SECRET_ACCESS_KEY")
    R2_BUCKET_NAME: str = os.getenv("R2_BUCKET_NAME")
    R2_PUBLIC_URL: str = os.getenv("R2_PUBLIC_URL")

    # Security Configuration
    API_AUTHORIZATION_TOKEN: str = os.getenv("API_AUTHORIZATION_TOKEN")
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "").split(",")

    TORTOISE_CONFIG: dict = {
        "connections": {"default": DATABASE_URL},
        "apps": {
            "models": {
                "models": [
                    "aerich.models",
                    "app.base.models",
                ],
                "default_connection": "default",
            },
        },
    }


settings = AppSettings()
