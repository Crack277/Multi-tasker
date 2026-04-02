from fastapi import APIRouter

from src.config import settings

from .routers.auth_router import router as auth_router
from .routers.category_router import router as category_router
from .routers.profile_router import router as profile_router
from .routers.project_router import router as project_router
from .routers.task_router import router as task_router
from .routers.user_router import router as user_router

router = APIRouter(prefix=settings.api.prefix)
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(project_router)
router.include_router(category_router)
router.include_router(task_router)
