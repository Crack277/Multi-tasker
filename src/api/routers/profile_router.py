from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.profile_schemas import ProfileUpdate
from src.api.services.profile_service import ProfileService
from src.api.utils import security
from src.config import settings
from src.database.database_helper import db_helper
from src.models import User

router = APIRouter(prefix=settings.api.v1.profile, tags=["PROFILE"])


@router.get("/{user_id}/")
async def get_auth_user_with_profile(
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = ProfileService(session)
    return await service.get_user_with_profile(current_user=current_user)


@router.put("/{user_id}/")
async def update_user_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = ProfileService(session)
    return await service.update_user_with_profile(
        current_user=current_user, profile_update=profile_update
    )
