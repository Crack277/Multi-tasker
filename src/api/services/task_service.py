from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.user_repository import UserRepository
from src.api.schemas.task_schemas import TaskCreate
from src.models import User


class TaskService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def create_task(self, task_create: TaskCreate, current_user: User):
        return await self.repository.create_task(
            task_create=task_create, current_user=current_user
        )
