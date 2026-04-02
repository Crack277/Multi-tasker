from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.user_schemas import UnAuthUpdatePassword, UserCreate
from src.api.services.user_service import UserService
from src.config import settings
from src.database.database_helper import db_helper

router = APIRouter(prefix=settings.api.v1.users, tags=["USERS"])


@router.get("/")
async def get_users(
    page: int, session: AsyncSession = Depends(db_helper.session_dependency)
):
    service = UserService(session)
    return await service.get_users(page=page)


@router.get("/{user_id}/")
async def get_user(
    user_id: int, session: AsyncSession = Depends(db_helper.session_dependency)
):
    service = UserService(session)
    return await service.get_user_by_id(user_id=user_id)


@router.post("/{user_id}/")
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = UserService(session)
    return await service.create_user(user_in=user_in)


@router.post("/confirm-code")
async def send_confirm_code(
    recipient: EmailStr,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = UserService(session)
    return await service.send_confirm_code(recipient=recipient)


@router.post("/recovery-password")
async def recovery_password(
    update_password: UnAuthUpdatePassword,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = UserService(session)
    return await service.recovery_password(update_password=update_password)


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
