"""Database configuration"""

from tortoise import Tortoise

from app.config.settings import settings


async def init_db():
    await Tortoise.init(
        config=settings.TORTOISE_CONFIG,
    )
