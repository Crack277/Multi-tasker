from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database.db import db_helper
from src.models import User

security = HTTPBearer()

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def get_hashed_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hash_password) -> bool:
    return pwd_context.verify(plain_password, hash_password)


def create_access_token(data: dict) -> dict:
    encode_data = {
        "email": data.get("email"),
    }
    expire = datetime.now() + timedelta(minutes=settings.access_token.expire_time)
    encode_data.update({"exp": expire, "type": "access"})
    token = jwt.encode(
        encode_data, settings.access_token.secret_key, settings.access_token.ALGORITHM
    )
    return {
        "access_token": token,
        "type": "bearer",
    }


async def get_current_user(
    session: AsyncSession = Depends(db_helper.session_dependency),
    credential: HTTPAuthorizationCredentials = Depends(security),
):

    if credential is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )

    token = credential.credentials

    payload = jwt.decode(
        token, settings.access_token.secret_key, settings.access_token.ALGORITHM
    )

    email = payload.get("email")
    stmt = select(User).where(User.email == email)
    user = await session.scalar(stmt)
    payload.update({"user_id": user.id})

    return payload


# def create_refresh_token(data: dict) -> str:
#
#     refresh_token = secrets.token_urlsafe(32)
#
#     # Сохранение токена в Redis с временем жизни
#     redis_client.setex(
#         name=f"refresh_token:{refresh_token}",
#         time=settings.access_token.refresh_expire_time * 86_400,  # в секундах
#         value=json.dumps({
#             "user_email": data["email"],
#             "created_at": datetime.now().isoformat(),
#         })
#     )
#
#     return refresh_token
#
#
# def create_token_pair(data: dict) -> dict:
#
#     access_token = create_access_token(data)
#     refresh_token = create_refresh_token(data)
#
#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#     }
#
#
# def verify_access_token(access_token: str):
#
#     exc = HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Incorrect access token!",
#     )
#
#     try:
#         payload = jwt.decode(
#             jwt=access_token,
#             key=settings.access_token.secret_key,
#             algorithms=[settings.access_token.ALGORITHM],
#         )
#
#         if payload.get("type") != "access":
#             raise exc
#
#         return payload
#
#     except JWToken:
#         raise exc
#
#
# def verify_refresh_token(refresh_token: str):
#
#     data = redis_client.get(f"refresh_token:{refresh_token}")
#
#     if data is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Incorrect refresh token!"
#         )
#
#     return data
