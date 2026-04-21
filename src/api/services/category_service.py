from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.user_repository import UserRepository
from src.api.schemas.category_schemas import CategoryCreate
from src.api.schemas.pagination_schemas import Pagination
from src.models import Category, User


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def get_categories(self, pagination: Pagination) -> List[Category]:
        return await self.repository.get_categories(pagination=pagination)

    async def create_category(
        self, category_create: CategoryCreate, current_user: User
    ) -> Category:
        return await self.repository.create_category(
            category_create=category_create, current_user=current_user
        )
