"""
Fast Template FastAPI
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise


from app.config.settings import AppSettings
from app.config.routes import api_router
from app.config.database import init_db


settings = AppSettings()

app = FastAPI(title="Fast Template FastAPI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    config=settings.TORTOISE_CONFIG,
    generate_schemas=settings.ENVIRONMENT == "local",
    add_exception_handlers=True,
)

app.include_router(api_router, prefix="/api/v1")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre process on application start"""
    await init_db()
    yield
