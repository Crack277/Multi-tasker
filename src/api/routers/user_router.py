from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.pagination_schemas import Pagination
from src.api.schemas.user_schemas import UnAuthUpdatePassword, UserCreate
from src.api.services.user_service import UserService
from src.config import settings
from src.database.database_helper import db_helper

router = APIRouter(prefix=settings.api.v1.users, tags=["USERS"])


@router.post("/")
async def get_users(
    pagination: Pagination,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    service = UserService(session)
    return await service.get_users(pagination=pagination)


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

