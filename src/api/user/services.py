from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.utils.security import get_hashed_password, verify_password
from src.models import User

from ..utils import security
from .dependencies import user_by_id
from .schemas import ResetPassword, UserCreate, UserUpdate


async def get_users(session: AsyncSession) -> List[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(user_id: int, session: AsyncSession) -> User | None:
    return await session.get(User, user_id)


async def create_user(user_in: UserCreate, session: AsyncSession):
    stmt = select(User).where(User.email == user_in.email)
    result = await session.scalar(stmt)
    if result is None:
        if user_in.password == user_in.repeat_password:
            hash_password = security.get_hashed_password(user_in.password)
            user = User(
                email=user_in.email,
                hashed_password=hash_password,
            )
            session.add(user)
            await session.commit()

            token = security.create_access_token(user_in.model_dump())
            return token

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пароли должны совпадать!"
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Этот email уже используется другим пользователем!",
    )


async def update_user(
    user_update: UserUpdate,
    user: User,
    session: AsyncSession,
    partial=True,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(user: User, session: AsyncSession) -> None:
    await session.delete(user)
    await session.commit()


async def reset_user_password(
    reset_password: ResetPassword,
    current_user: dict,
    session: AsyncSession,
):
    user = await user_by_id(user_id=current_user.get("user_id"), session=session)

    if reset_password.new_password != reset_password.repeat_new_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="New passwords must be equals!",
        )
    if not verify_password(reset_password.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password!",
        )

    set_hashed_password = get_hashed_password(reset_password.new_password)
    user.hashed_password = set_hashed_password

    await session.commit()
    await session.refresh(user)
    return {
        "Access": True,
    }
