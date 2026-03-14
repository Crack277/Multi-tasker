from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.crud import get_user
from src.database.db import db_helper
from src.models import User


async def user_by_id(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:

    result = await get_user(user_id=user_id, session=session)
    if result is not None:
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="This user not found!"
    )
