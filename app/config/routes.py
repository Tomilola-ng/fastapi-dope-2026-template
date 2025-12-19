"""Main Routes"""

from fastapi import APIRouter

from app.base import routes as base_routes


api_router = APIRouter()

api_router.include_router(base_routes.router)


@api_router.get("/health")
def health():
    """Health check endpoint"""
    return {"message": "Healthy"}
