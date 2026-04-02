from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.user_repository import UserRepository
from src.api.schemas.project_schemas import CreateUserProject, UpdateUserProject
from src.models import Project, User


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def get_user_with_projects(self, current_user: User) -> User:
        return await self.repository.get_user_with_projects(current_user=current_user)

    async def create_project(
        self, project_create: CreateUserProject, current_user: User
    ) -> Project:
        return await self.repository.create_user_project(
            project_create=project_create, current_user=current_user
        )

    async def upload_file(
        self, project_id: int, file: UploadFile, current_user: User
    ) -> str:
        file_url = await self.repository.upload_file(
            file=file, user_id=current_user.id, name=f"icon_{project_id}"
        )

        project = await self.repository.get_project_by_id(project_id=project_id)
        if project.owner_id == current_user.id:
            project.icon = file_url
            await self.session.commit()
            return file_url

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This is not your project!",
        )

    async def update_project(
        self, project_update: UpdateUserProject, current_user: User
    ) -> Project:
        return await self.repository.update_project(
            project_update=project_update, current_user=current_user
        )

    async def delete_project(self, project_id: int, current_user: User) -> dict:
        return await self.repository.delete_project(
            project_id=project_id, current_user=current_user
        )
