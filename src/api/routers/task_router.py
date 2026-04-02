from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.task_schemas import TaskCreate
from src.api.services.task_service import TaskService
from src.api.utils import security
from src.config import settings
from src.database.database_helper import db_helper
from src.models import User

router = APIRouter(prefix=settings.api.v1.tasks, tags=["TASKS"])


@router.get("/all")
async def get_tasks(
    page: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = TaskService(session)
    return await service.get_tasks(page=page)


@router.get("/{task_id}/")
async def get_task_by_id(
    task_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = TaskService(session)
    return await service.get_task_by_id(task_id=task_id)


@router.get("/{user_id}/completed")
async def get_user_completed_tasks(
    user_id: int,
    page: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = TaskService(session)
    return await service.get_user_completed_tasks(user_id=user_id, page=page)


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


@router.get("/")
async def get_user_tasks_by_priority(
    page: int,
    very_urgent: bool = Query(False),
    urgent: bool = Query(False),
    can_wait: bool = Query(False),
    not_urgent: bool = Query(False),
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = TaskService(session)
    return await service.get_user_tasks_by_priority(
        page=page,
        very_urgent=very_urgent,
        urgent=urgent,
        can_wait=can_wait,
        not_urgent=not_urgent,
        current_user=current_user,
    )
