from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.user_repository import UserRepository
from src.api.schemas.profile_schemas import ProfileUpdate
from src.api.schemas.user_schemas import UserUpdate
from src.models import Profile, User


class ProfileService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def get_user_with_profile(self, current_user: User) -> User:
        return await self.repository.get_user_with_profile(current_user=current_user)

    async def update_user_with_profile(
        self, current_user: User, profile_update: ProfileUpdate
    ) -> Profile:
        user = await self.repository.get_user_with_profile(current_user=current_user)

        existing_user = await self.repository.get_user_by_email_optional(
            profile_update.email
        )
        if existing_user and existing_user.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use!",
            )

        user_in = UserUpdate(email=profile_update.email)
        await self.repository.update_user(user_in=user_in, user=user)

        updated_profile = await self.repository.update_user_profile(
            profile_update=profile_update,
            profile=user.profile,
        )

        return updated_profile

    async def upload_file(self, file: UploadFile, current_user: User) -> str:
        file_url = await self.repository.upload_file(
            file=file, user_id=current_user.id, name="avatar"
        )
        user = await self.repository.get_user_with_profile(current_user=current_user)
        user.profile.photo = file_url
        await self.session.commit()
        return file_url
