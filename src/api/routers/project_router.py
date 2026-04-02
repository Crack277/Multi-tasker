from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.project_schemas import CreateUserProject, UpdateUserProject
from src.api.services.project_service import ProjectService
from src.api.utils import security
from src.config import settings
from src.database.database_helper import db_helper
from src.models import User

router = APIRouter(prefix=settings.api.v1.projects, tags=["PROJECTS"])


@router.get("/all")
async def get_user_with_projects(
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = ProjectService(session)
    return await service.get_user_with_projects(current_user=current_user)


@router.post("/{project_id}/")
async def create_project(
    project_create: CreateUserProject,
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = ProjectService(session)
    return await service.create_project(
        project_create=project_create, current_user=current_user
    )


@router.post("/upload-file")
async def upload_file(
    project_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = ProjectService(session)
    return await service.upload_file(
        project_id=project_id, file=file, current_user=current_user
    )


@router.put("/{project_id}/")
async def update_project(
    project_update: UpdateUserProject,
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = ProjectService(session)
    return await service.update_project(
        project_update=project_update, current_user=current_user
    )


@router.delete("/{project_id}/")
async def delete_project(
    project_id: int,
    current_user: User = Depends(security.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    service = ProjectService(session)
    return await service.delete_project(
        project_id=project_id, current_user=current_user
    )
