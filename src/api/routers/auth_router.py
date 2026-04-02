from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.user_schemas import AuthUpdatePassword, UserLoging
from src.api.services.auth_service import AuthService
from src.api.utils import security
from src.api.utils.security import security as bearer_security
from src.config import settings
from src.database.database_helper import db_helper
from src.models import User

router = APIRouter(prefix=settings.api.v1.auth, tags=["AUTH"])


@router.post("/")
async def login_user(
    user_in: UserLoging,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = AuthService(session)
    return await service.login_user(user_in=user_in)


@router.get("/me")
async def get_auth_user(
    current_user: User = Depends(security.get_current_user),
):
    return current_user


@router.post("/reset-password")
async def reset_user_password(
    update_password: AuthUpdatePassword,
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = AuthService(session)
    return await service.update_user_password(
        update_password=update_password, current_user=current_user
    )


@router.post("/logout")
async def logout(
    credential: HTTPAuthorizationCredentials = Depends(bearer_security),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = AuthService(session)
    return await service.logout(credential=credential)
