from fastapi import APIRouter
from app.api.endpoints import normalization

api_router = APIRouter()
api_router.include_router(normalization.router, tags=["Normalization"])