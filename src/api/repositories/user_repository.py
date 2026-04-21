from datetime import datetime, timezone
from typing import List

import aiofiles
from fastapi import HTTPException, UploadFile, status
from pydantic import EmailStr
from sqlalchemy import and_, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api.schemas.category_schemas import CategoryCreate
from src.api.schemas.pagination_schemas import Pagination
from src.api.schemas.profile_schemas import ProfileUpdate
from src.api.schemas.project_schemas import CreateUserProject, UpdateUserProject
from src.api.schemas.task_schemas import TaskCreate, UserTasksInfo, TaskTypes
from src.api.schemas.user_schemas import (
    AuthUpdatePassword,
    UnAuthUpdatePassword,
    UserCreate,
    UserUpdate,
)
from src.api.utils import security
from src.models import Category, Profile, Project, Task, User
from src.api.schemas.task_schemas import TaskStatus, TaskPriority


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self, pagination: Pagination) -> List[User]:
        offset = (pagination.page - 1) * pagination.page_size
        stmt = select(User).order_by(User.id).limit(pagination.page_size).offset(offset)
        result: Result = await self.session.execute(stmt)
        users = result.scalars().all()
        return list(users)

    async def get_user(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.get_user(user_id=user_id)

        if user is not None:
            return user

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This user not found!"
        )

    async def get_user_by_email(self, user_email: EmailStr) -> User:
        stmt = select(User).where(User.email == user_email)
        user = await self.session.scalar(stmt)
        if user is not None:
            return user

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user with email not found!",
        )

    async def get_user_by_email_optional(self, user_email: EmailStr) -> User | None:
        stmt = select(User).where(User.email == user_email)
        return await self.session.scalar(stmt)

    async def get_user_by_confirm_code(self, confirm_code: str) -> User:
        stmt = select(User).where(User.confirm_code == confirm_code)
        user = await self.session.scalar(stmt)
        if user is not None:
            return user

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user with confirmation code not found!",
        )

    async def get_user_with_profile(self, current_user: User) -> User:
        stmt = (
            select(User)
            .options(joinedload(User.profile))
            .where(User.email == current_user.email)
        )
        user = await self.session.scalar(stmt)
        return user

    async def create_user_profile(self, current_user: User) -> Profile:
        profile = Profile(
            user_id=current_user.id,
            email=current_user.email,
        )
        self.session.add(profile)
        await self.session.commit()
        return profile

    async def create_user(self, user_in: UserCreate) -> User:
        stmt = select(User).where(User.email == user_in.email)
        user = await self.session.scalar(stmt)
        if user is None:
            if user_in.password == user_in.repeat_password:
                hash_password = security.get_hashed_password(user_in.password)
                user = User(
                    email=user_in.email,
                    hashed_password=hash_password,
                )
                self.session.add(user)
                await self.session.commit()

                return user

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords must be equals!",
            )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email is already being used by another user!",
        )

    async def update_user(
        self,
        user_in: UserUpdate,
        user: User,
        partial: bool = True,
    ) -> User:
        for name, value in user_in.model_dump(exclude_unset=partial).items():
            setattr(user, name, value)
        await self.session.commit()
        return user

    async def update_user_profile(
        self,
        profile_update: ProfileUpdate,
        profile: Profile,
        partial: bool = True,
    ) -> Profile:
        for name, value in profile_update.model_dump(exclude_unset=partial).items():
            setattr(profile, name, value)
        await self.session.commit()
        return profile

    async def update_user_password(
        self, current_user: User, update_password: AuthUpdatePassword
    ) -> User:
        if update_password.new_password == update_password.repeat_new_password:
            if security.verify_password(
                update_password.old_password, current_user.hashed_password
            ):
                hashed_password = security.get_hashed_password(
                    update_password.new_password
                )

                current_user.hashed_password = hashed_password
                await self.session.commit()
                return current_user

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid password!",
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords must be equals!",
        )

    async def recovery_user_password(
        self, current_user: User, update_password: UnAuthUpdatePassword
    ) -> User:
        if update_password.new_password == update_password.repeat_new_password:
            hashed_password = security.get_hashed_password(update_password.new_password)
            current_user.hashed_password = hashed_password
            current_user.confirm_code = None
            await self.session.commit()
            return current_user

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords must be equals!",
        )

    async def upload_file(self, file: UploadFile, user_id: int, name: str) -> str:
        from src.api.utils.static.photo import BASE_DIR

        contents = await file.read()
        file_type = file.filename.split(".")[-1]
        file_url = f"{BASE_DIR}/{name}_{user_id}.{file_type}"
        async with aiofiles.open(file_url, "wb") as f:
            await f.write(contents)

        return file_url

    async def get_user_with_projects(self, current_user: User) -> User:
        stmt = (
            select(User)
            .options(selectinload(User.project))
            .where(User.id == current_user.id)
        )
        user = await self.session.scalar(stmt)
        return user

    async def get_project_by_id(self, project_id: int) -> Project:
        stmt = select(Project).where(Project.id == project_id)
        project = await self.session.scalar(stmt)
        if project is not None:
            return project

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found!",
        )

    async def create_user_project(
        self, project_create: CreateUserProject, current_user: User
    ) -> Project:

        project = Project(
            owner_id=current_user.id,
            name=project_create.name,
            icon=project_create.icon,
        )
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(current_user)
        return project

    async def update_project(
        self,
        current_user: User,
        project_update: UpdateUserProject,
        partial: bool = True,
    ) -> Project:
        stmt = select(Project).where(
            and_(
                Project.id == project_update.id,
                Project.owner_id == current_user.id,
            )
        )
        project = await self.session.scalar(stmt)
        if project is not None:
            for name, value in project_update.model_dump(exclude_unset=partial).items():
                if name != "id":
                    setattr(project, name, value)

            await self.session.commit()
            await self.session.refresh(project)

            return project

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This project not found!",
        )

    async def delete_project(
        self,
        project_id: int,
        current_user: User,
    ):
        project = await self.get_project_by_id(project_id=project_id)

        if project.owner_id == current_user.id:
            await self.session.delete(project)
            await self.session.commit()

            return {"Success": True}

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This project not found!",
        )

    async def get_user_with_categories(self, current_user: User) -> User:
        stmt = (
            select(User)
            .options(selectinload(User.category))
            .where(User.id == current_user.id)
        )
        user = await self.session.scalar(stmt)
        return user

    async def get_categories(
        self, pagination: Pagination,
    ) -> List[Category]:
        offset = (pagination.page - 1) * pagination.page_size
        stmt = select(Category).order_by(Category.id).limit(pagination.page_size).offset(offset)
        result = await self.session.execute(stmt)
        categories = result.scalars().all()

        return list(categories)

    async def get_category_by_id(self, category_id: int) -> Category:
        stmt = select(Category).where(Category.id == category_id)
        category = await self.session.scalar(stmt)

        if category is not None:
            return category

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This category not found!",
        )

    async def create_category(
        self, category_create: CategoryCreate, current_user: User
    ) -> Category:

        category = Category(
            **{
                **category_create.model_dump(),
                "user_id": current_user.id,
            }
        )

        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)

        return category

    async def get_tasks(self, pagination: Pagination) -> List[Task]:
        offset = (pagination.page - 1) * pagination.page_size
        stmt = select(Task).order_by(Task.id).limit(pagination.page_size).offset(offset)
        result = await self.session.execute(stmt)
        tasks = result.scalars().all()

        return list(tasks)

    async def get_task_by_id(self, task_id: int) -> Task:
        stmt = select(Task).where(Task.id == task_id)
        task = await self.session.scalar(stmt)

        if task is not None:
            return task

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This task not found!",
        )

    async def get_user_tasks(
        self, user_id: int, pagination: Pagination
    ) -> List[Task]:

        offset = (pagination.page - 1) * pagination.page_size
        stmt = (
            select(Task)
            .where(Task.assignee_id == user_id)
            .limit(pagination.page_size)
            .offset(offset)
        )
        tasks = await self.session.scalars(stmt)
        return list(tasks)

    async def get_user_priority_tasks(
        self,
        user_id: int,
        pagination: Pagination,
        types: List[TaskTypes],
    ) -> List[Task]:
        offset = (pagination.page - 1) * pagination.page_size
        stmt = (
            select(Task)
            .where(Task.assignee_id == user_id)
            .where(
                Task.priority.in_(
                    types,
                )
            )
            .limit(pagination.page_size)
            .offset(offset)
        )
        tasks = await self.session.scalars(stmt)
        return list(tasks)


        # offset = (pagination.page - 1) * pagination.page_size
        # stmt = (
        #     select(Task)
        #     .where(Task.assignee_id == user_id)
        #     .where(Task.priority == priority)
        #     .limit(pagination.page_size)
        #     .offset(offset)
        # )
        # tasks = await self.session.scalars(stmt)
        # return list(tasks)

    async def get_user_tasks_info(self, user_id: int) -> UserTasksInfo:
        stmt = select(Task).where(Task.assignee_id == user_id)
        result = await self.session.execute(stmt)
        tasks = result.scalars().all()

        all_tasks = len(tasks)
        completed_tasks = sum(
            1 for task in tasks if task.status == TaskStatus.COMPLETED
        )

        user_tasks = UserTasksInfo(
            all_tasks=all_tasks,
            completed_tasks=completed_tasks,
        )

        return user_tasks

    async def create_task(self, task_create: TaskCreate, current_user: User) -> Task:
        assignee_id = await self.get_user_by_id(task_create.assignee_id)
        project_id = await self.get_project_by_id(project_id=task_create.project_id)
        category_id = await self.get_category_by_id(category_id=task_create.category_id)

        if assignee_id and project_id and category_id:

            task = Task(
                **{
                    **task_create.model_dump(),
                    "author_id": current_user.id,
                    "created_at": datetime.now(timezone.utc)
                    .replace(tzinfo=None)
                    .replace(microsecond=0),
                    "updated_at": datetime.now(timezone.utc)
                    .replace(tzinfo=None)
                    .replace(microsecond=0),
                }
            )

            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)

            return task

    async def complete_task(self, task_id: int) -> Task:
        task = await self.get_task_by_id(task_id=task_id)

        task.status = TaskStatus.COMPLETED
        await self.session.commit()
        await self.session.refresh(task)

        return task
