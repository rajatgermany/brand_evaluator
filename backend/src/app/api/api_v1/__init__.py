from fastapi import APIRouter

from .endpoints.tweet_analyzer import tweet_analyzer_router

api_v1_router = APIRouter()
api_v1_router.include_router(
    tweet_analyzer_router, prefix="/api_v1", tags=["api_v1"]
)
