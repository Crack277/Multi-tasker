from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User

from . import security
from .schemas import UserCreate, UserUpdate


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
