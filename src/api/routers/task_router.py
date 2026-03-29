from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.task_schemas import TaskCreate
from src.api.services.task_service import TaskService
from src.api.utils import security
from src.config import settings
from src.database.database_helper import db_helper
from src.models import User

router = APIRouter(prefix=settings.api.v1.tasks, tags=["TASKS"])


@router.post("/create/{task_id}")
async def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = TaskService(session)
    return await service.create_task(task_create=task_create, current_user=current_user)
