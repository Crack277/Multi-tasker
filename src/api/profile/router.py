from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user import security
from src.config import settings
from src.database.db import db_helper

from . import services
from .schemas import ProfileCreate

router = APIRouter(prefix=settings.api.v1.profile, tags=["PROFILE"])


@router.get("/")
async def get_user_with_profile(
    current_user: dict = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await services.get_user_with_profile(
        current_user=current_user, session=session
    )


@router.post("/")
async def create_user_profile(
    profile_in: ProfileCreate,
    current_user: dict = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await services.create_user_profile(
        profile_in=profile_in, current_user=current_user, session=session
    )
