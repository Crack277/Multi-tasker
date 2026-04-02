from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.user_repository import UserRepository
from src.api.schemas.task_schemas import TaskCreate, UserTasksInfo
from src.models import User
from src.models.task import Task, TaskPriority, TaskStatus


class TaskService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def get_tasks(self, page: int) -> List[Task]:
        return await self.repository.get_tasks(page=page)

    async def get_task_by_id(self, task_id: int) -> Task:
        return await self.repository.get_task_by_id(task_id=task_id)

    async def get_user_completed_tasks(self, user_id: int, page: int) -> List[Task]:
        user = await self.repository.get_user_by_id(user_id=user_id)
        tasks = await self.repository.get_user_tasks(user_id=user.id, page=page)

        completed_tasks = [
            task for task in tasks if task.status == TaskStatus.COMPLETED
        ]
        return completed_tasks

    async def get_user_tasks_by_priority(
        self,
        page: int,
        very_urgent: bool,
        urgent: bool,
        can_wait: bool,
        not_urgent: bool,
        current_user: User,
    ) -> List[Task]:
        selected_count = sum([very_urgent, urgent, can_wait, not_urgent])
        tasks = []

        if selected_count == 1:
            if very_urgent:
                tasks = await self.repository.get_user_priority_tasks(
                    user_id=current_user.id,
                    priority=TaskPriority.VERY_URGENT,
                    page=page,
                )
            if urgent:
                tasks = await self.repository.get_user_priority_tasks(
                    user_id=current_user.id,
                    priority=TaskPriority.URGENT,
                    page=page,
                )
            if can_wait:
                tasks = await self.repository.get_user_priority_tasks(
                    user_id=current_user.id,
                    priority=TaskPriority.CAN_WAIT,
                    page=page,
                )
            if not_urgent:
                tasks = await self.repository.get_user_priority_tasks(
                    user_id=current_user.id,
                    priority=TaskPriority.NOT_URGENT,
                    page=page,
                )

            return tasks

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There should be one priority!",
        )

    async def get_user_tasks_info(self, user_id: int) -> UserTasksInfo:
        user = await self.repository.get_user_by_id(user_id=user_id)
        return await self.repository.get_user_tasks_info(user_id=user.id)

    async def create_task(self, task_create: TaskCreate, current_user: User) -> Task:
        return await self.repository.create_task(
            task_create=task_create, current_user=current_user
        )

    async def complete_task(self, task_id: int, current_user: User) -> Task:
        task = await self.repository.get_task_by_id(task_id=task_id)

        if task.assignee_id == current_user.id or task.author_id == current_user.id:
            return await self.repository.complete_task(task_id=task_id)

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This is not your task!",
        )
