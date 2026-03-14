from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.config import settings

security = HTTPBasic()


def get_hashed_password(password: str) -> bytes:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def create_access_token(data: dict) -> str:
    encode_data = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.access_token.expire_time)
    encode_data.update({"exp": expire})
    token = jwt.encode(encode_data, settings.access_token.secret_key, settings.access_token.ALGORITHM)
    return token

