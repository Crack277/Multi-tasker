from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.category_schemas import CategoryCreate
from src.api.services.category_service import CategoryService
from src.api.utils import security
from src.config import settings
from src.database.database_helper import db_helper
from src.models import User

router = APIRouter(prefix=settings.api.v1.categories, tags=["CATEGORIES"])


@router.get("/all")
async def get_categories(
    page: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = CategoryService(session)
    return await service.get_categories(page=page)


@router.post("/{category_id}/")
async def create_category(
    category_create: CategoryCreate,
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = CategoryService(session)
    return await service.create_category(
        category_create=category_create, current_user=current_user
    )
