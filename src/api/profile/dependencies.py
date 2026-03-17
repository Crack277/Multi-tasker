from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.utils import security
from src.database.db import db_helper
from src.models import Profile


async def get_user_profile(
    session: AsyncSession = Depends(db_helper.session_dependency),
    current_user: dict = Depends(security.get_current_user),
) -> Profile:
    stmt = select(Profile).where(Profile.email == current_user.get("email"))
    profile = await session.scalar(stmt)

    if profile is not None:
        return profile

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="This profile not found!",
    )
