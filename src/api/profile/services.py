from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.profile.schemas import ProfileCreate, ProfileUpdate
from src.models import Profile, User


async def get_user_with_profile(current_user: dict, session: AsyncSession):
    stmt = (
        select(User)
        .options(joinedload(User.profile))
        .where(User.email == current_user.get("email"))
    )
    user = await session.scalar(stmt)
    return user


async def create_user_profile(
    profile_in: ProfileCreate, current_user: dict, session: AsyncSession
):
    stmt = select(Profile).where(Profile.user_id == current_user.get("user_id"))
    stmt_profile = await session.execute(stmt)
    result = stmt_profile.scalar_one_or_none()

    if result is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The profile already register!",
        )

    profile = Profile(
        user_id=current_user.get("user_id"),
        name=profile_in.name,
        email=profile_in.email,
        photo=profile_in.photo,
    )
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


async def update_user_profile(
    profile_update: ProfileUpdate,
    session: AsyncSession,
    profile: Profile,
    partial: bool = True,
):
    for name, value in profile_update.model_dump(exclude_unset=partial).items():
        setattr(profile, name, value)
    await session.commit()
    await session.refresh(profile)
    return profile
