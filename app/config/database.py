"""Database configuration"""

from tortoise import Tortoise

from app.config.settings import settings


async def init_db():
    """
    Initialize the database connection using Tortoise ORM.

    This function configures the Tortoise ORM with the settings
    provided in the application's configuration. It initializes
    the database connection and sets up the necessary models.

    Returns:
        None
    """
    await Tortoise.init(
        config=settings.TORTOISE_CONFIG,
    )

TORTOISE_ORM = settings.TORTOISE_CONFIG
