from fastapi import HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.user_repository import UserRepository
from src.api.schemas.user_schemas import (AuthUpdatePassword, PrintAccessToken,
                                          UserLoging)
from src.api.utils import security
from src.config import settings
from src.models import User
from src.redis import redis_client


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def login_user(self, user_in: UserLoging) -> PrintAccessToken:
        user = await self.repository.get_user_by_email(user_email=user_in.email)

        if not user or not security.verify_password(
            user_in.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password!",
            )

        access_token = await security.create_access_token(user)
        return access_token

    async def upload_file(self, file: UploadFile, current_user: User):
        file_url = await self.repository.upload_file(file=file, user_id=current_user.id)

        current_user.profile.photo = file_url
        await self.session.commit()
        return file_url

    async def update_user_password(
        self, current_user: User, update_password: AuthUpdatePassword
    ):
        return await self.repository.update_user_password(
            current_user=current_user, update_password=update_password
        )

    async def logout(self, credential: HTTPAuthorizationCredentials):
        token = credential.credentials
        await redis_client.add_to_blacklist(
            token, settings.access_token.expire_minutes * 60
        )
        return {"message": "Logged out"}
