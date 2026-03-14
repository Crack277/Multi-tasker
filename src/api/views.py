from fastapi import APIRouter

from src.config import settings

from .user import router as user_router

router = APIRouter(prefix=settings.api.prefix)
router.include_router(user_router)
