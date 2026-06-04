from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.user_repository import UserRepository
from src.api.schemas.task_schemas import TaskStatus
from src.models import Category, Profile, Project, Task, User


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def mock_credentials():
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid_token")


@pytest.fixture
def user_repository(mock_session):
    """Фикстура для репозитория с мок-сессией."""
    return UserRepository(mock_session)


@pytest.fixture
def mock_user():
    """Фикстура для тестового пользователя."""
    user = MagicMock(spec=User)
    user.id = 1
    user.email = "test@example.com"
    user.hashed_password = "hashed_secret123"
    user.confirm_code = "123456"
    return user


@pytest.fixture
def mock_profile():
    """Фикстура для тестового профиля."""
    profile = MagicMock(spec=Profile)
    profile.id = 1
    profile.user_id = 1
    profile.email = "test@example.com"
    profile.first_name = "Test"
    return profile


@pytest.fixture
def mock_project():
    """Фикстура для тестового проекта."""
    project = MagicMock(spec=Project)
    project.id = 1
    project.owner_id = 1
    project.name = "Test Project"
    project.icon = "icon.png"
    return project


@pytest.fixture
def mock_category():
    """Фикстура для тестовой категории."""
    category = MagicMock(spec=Category)
    category.id = 1
    category.user_id = 1
    category.name = "Test Category"
    return category


@pytest.fixture
def mock_task():
    """Фикстура для тестовой задачи."""
    task = MagicMock(spec=Task)
    task.id = 1
    task.assignee_id = 1
    task.author_id = 1
    task.project_id = 1
    task.category_id = 1
    task.status = TaskStatus.IN_PROGRESS
    task.priority = "MEDIUM"
    return task
