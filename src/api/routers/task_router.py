from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.pagination_schemas import Pagination
from src.api.schemas.task_schemas import TaskCreate, TaskTypes
from src.api.services.task_service import TaskService
from src.api.utils import security
from src.config import settings
from src.database.database_helper import db_helper
from src.models import User

router = APIRouter(prefix=settings.api.v1.tasks, tags=["TASKS"])


@router.post("/all")
async def get_tasks(
    pagination: Pagination,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = TaskService(session)
    return await service.get_tasks(pagination=pagination)


@router.get("/{task_id}/")
async def get_task_by_id(
    task_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = TaskService(session)
    return await service.get_task_by_id(task_id=task_id)


@router.post("/{user_id}/completed")
async def get_user_completed_tasks(
    user_id: int,
    pagination: Pagination,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = TaskService(session)
    return await service.get_user_completed_tasks(user_id=user_id, pagination=pagination)


@router.get("/{user_id}/info")
async def get_user_tasks_info(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = TaskService(session)
    return await service.get_user_tasks_info(user_id=user_id)


@router.post("/{task_id}/")
async def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = TaskService(session)
    return await service.create_task(task_create=task_create, current_user=current_user)


@router.post("/{task_id}/complete")
async def complete_task(
    task_id: int,
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = TaskService(session)
    return await service.complete_task(task_id=task_id, current_user=current_user)


@router.post("/")
async def get_user_tasks_by_priority(
    pagination: Pagination,
    types: List[TaskTypes],
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = TaskService(session)
    return await service.get_user_tasks_by_priority(
        pagination=pagination,
        types=types,
        current_user=current_user,
    )
