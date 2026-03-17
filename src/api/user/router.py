from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database.db import db_helper
from src.models import User

from . import services as users_crud
from .dependencies import user_by_id
from .schemas import UserCreate, UserUpdate

router = APIRouter(prefix=settings.api.v1.users, tags=["USERS"])


@router.get("/")
async def get_users(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await users_crud.get_users(session=session)


@router.get("/{user_id}/")
async def get_user(user: User = Depends(user_by_id)):
    return user


@router.post("/{user_id}/")
async def create_user(
    user_in: UserCreate, session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await users_crud.create_user(user_in=user_in, session=session)


# @router.put("/{user_id}/")
# async def update_user(
#     user_update: UserUpdate,
#     user: User = Depends(user_by_id),
#     session: AsyncSession = Depends(db_helper.session_dependency),
# ):
#     return await users_crud.update_user(
#         user_update=user_update, user=user, session=session
#     )


# @router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(
#     user: User = Depends(user_by_id),
#     session: AsyncSession = Depends(db_helper.session_dependency),
# ):
#     return await users_crud.delete_user(user=user, session=session)
