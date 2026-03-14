import json
import secrets
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from redis.auth.token import JWToken
from src.config import settings
from src.redis import redis_client

security = HTTPBasic()


def get_hashed_password(password: str) -> bytes:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def create_access_token(data: dict) -> str:
    encode_data = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.access_token.expire_time)
    encode_data.update({"exp": expire, "type": "access"})
    token = jwt.encode(encode_data, settings.access_token.secret_key, settings.access_token.ALGORITHM)
    return token


def create_refresh_token(data: dict) -> str:

    refresh_token = secrets.token_urlsafe(32)

    # Сохранение токена в Redis с временем жизни
    redis_client.setex(
        name=f"refresh_token:{refresh_token}",
        time=settings.access_token.refresh_expire_time * 86_400,  # в секундах
        value={
            "user_email": data["email"],
            "created_at": datetime.now(),
        }
    )

    return refresh_token


def create_token_pair(data: dict) -> dict:

    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def verify_access_token(access_token: str):

    exc = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Incorrect access token!",
    )

    try:
        payload = jwt.decode(
            jwt=access_token,
            key=settings.access_token.secret_key,
            algorithms=[settings.access_token.ALGORITHM],
        )

        if payload.get("type") != "access":
            raise exc

        return payload

    except JWToken:
        raise exc


def verify_refresh_token(refresh_token: str):

    data = redis_client.get(f"refresh_token:{refresh_token}")

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect refresh token!"
        )

    return data