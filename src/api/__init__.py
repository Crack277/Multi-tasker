from fastapi import APIRouter

from src.config import settings

from .profile.router import router as profile_router
from .user.auth_router import router as auth_router
from .user.router import router as user_router

router = APIRouter(prefix=settings.api.prefix)
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(profile_router)
