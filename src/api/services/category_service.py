from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.user_repository import UserRepository
from src.api.schemas.category_schemas import CategoryCreate
from src.models import Category, User


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def get_categories(self, page: int) -> List[Category]:
        return await self.repository.get_categories(page=page)

    async def create_category(
        self, category_create: CategoryCreate, current_user: User
    ) -> Category:
        return await self.repository.create_category(
            category_create=category_create, current_user=current_user
        )
