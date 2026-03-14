from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User

from .schemas import UserCreate, UserUpdate
from .security import get_hashed_password, create_access_token


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
        if user_in.hashed_password == user_in.reset_password:
            hash_password = get_hashed_password(user_in.hashed_password)
            user = User(
                email=user_in.email,
                hashed_password=hash_password,
            )
            session.add(user)
            await session.commit()

            access_token = create_access_token(
                data={"subject": user_in.email}
            )

            return {
                "access_token": access_token,
                "type_of_token": "bearer",
            }

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пароли должны совпадать!"
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Этот email уже используется другим пользователем!"
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
