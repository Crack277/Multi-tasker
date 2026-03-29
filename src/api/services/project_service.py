from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.user_repository import UserRepository
from src.api.schemas.project_schemas import (CreateUserProject,
                                             UpdateUserProject)
from src.models import User


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def get_user_with_projects(self, current_user: User):
        return await self.repository.get_user_with_projects(current_user=current_user)

    async def create_project(
        self, project_create: CreateUserProject, current_user: User
    ):
        return await self.repository.create_user_project(
            project_create=project_create, current_user=current_user
        )

    async def update_project(
        self, project_update: UpdateUserProject, current_user: User
    ):
        return await self.repository.update_project(
            project_update=project_update, current_user=current_user
        )

    async def delete_project(
        self, project_id: int, current_user: User
    ):
        return await self.repository.delete_project(
            project_id=project_id, current_user=current_user
        )
