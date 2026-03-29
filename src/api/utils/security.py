import secrets
import string
import time

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.user_schemas import PrintAccessToken
from src.config import settings
from src.database.database_helper import db_helper
from src.models import User
from src.redis import redis_client

security = HTTPBearer()

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def get_hashed_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hash_password) -> bool:
    return pwd_context.verify(plain_password, hash_password)


def generate_confirm_code() -> str:
    return "".join(secrets.choice(string.digits) for _ in range(6))


async def create_access_token(user: User) -> PrintAccessToken:
    current_time = int(time.time())
    expire_time = current_time + settings.access_token.expire_minutes * 60

    encode_data = {
        "user_id": user.id,
        "email": user.email,
        "exp": expire_time,
        "created_at": current_time,
    }
    token = jwt.encode(
        encode_data, settings.access_token.secret_key, settings.access_token.ALGORITHM
    )
    message = PrintAccessToken(access_token=token)

    return message


async def get_current_user(
    session: AsyncSession = Depends(db_helper.session_dependency),
    credential: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    if credential is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )

    token = credential.credentials

    if await redis_client.is_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
        )

    payload = jwt.decode(
        token,
        settings.access_token.secret_key,
        settings.access_token.ALGORITHM,
        options={"verify_exp": True},
    )

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    stmt = select(User).where(User.id == user_id)
    user = await session.scalar(stmt)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
