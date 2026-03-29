from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.user_repository import UserRepository
from src.api.schemas.user_schemas import UnAuthUpdatePassword, UserCreate
from src.api.utils import security
from src.api.utils.smtp.email_body import email_body
from src.api.utils.smtp.task import send_email


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def get_users(self):
        return await self.repository.get_users()

    async def get_user_by_id(self, user_id: int):
        return await self.repository.get_user_by_id(user_id=user_id)

    async def create_user(self, user_in: UserCreate):
        user = await self.repository.create_user(user_in=user_in)
        await self.repository.create_user_profile(current_user=user)
        await self.session.refresh(user)
        return await security.create_access_token(user)

    async def send_confirm_code(self, recipient: EmailStr):
        confirm_code = security.generate_confirm_code()

        user = await self.repository.get_user_by_email(user_email=recipient)
        user.confirm_code = confirm_code
        await self.session.commit()

        # add celery?
        await send_email(
            recipient=recipient,
            body=email_body(confirm_code),
        )

        return {"Success": True}

    async def recovery_password(self, update_password: UnAuthUpdatePassword):
        current_user = await self.repository.get_user_by_confirm_code(
            confirm_code=update_password.confirm_code,
        )
        return await self.repository.recovery_user_password(
            current_user=current_user,
            update_password=update_password,
        )
