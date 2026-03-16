from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.security import security
from src.config import settings
from src.database.db import db_helper
from src.models import User

router = APIRouter(prefix=settings.api.v1.projects, tags=["PROJECT"])


@router.get("/")
async def get_user_projects(
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    pass
