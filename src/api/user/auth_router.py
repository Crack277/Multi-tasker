from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.schemas import UserLoging
from src.config import settings
from src.database.db import db_helper
from src.models import User

from . import security

router = APIRouter(prefix=settings.api.v1.auth, tags=["AUTH"])


@router.post("/")
async def login_user(
    user_in: UserLoging,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    stmt = select(User).where(User.email == user_in.email)
    user = await session.scalar(stmt)

    if not user or not security.verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    access_token = security.create_access_token(user_in.model_dump())

    return {
        "access_token": access_token,
        "type_of_token": "bearer",
        "user": user,
    }


@router.get("/me")
async def get_auth_user(current_user: User = Depends(security.get_current_user)):
    return current_user
