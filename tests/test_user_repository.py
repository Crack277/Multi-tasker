from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException, UploadFile

from src.api.schemas.category_schemas import CategoryCreate
from src.api.schemas.pagination_schemas import Pagination
from src.api.schemas.profile_schemas import ProfileUpdate
from src.api.schemas.project_schemas import (
    CreateUserProject,
    UpdateUserProject,
)
from src.api.schemas.task_schemas import TaskCreate, TaskPriority, TaskStatus
from src.api.schemas.user_schemas import (
    AuthUpdatePassword,
    UnAuthUpdatePassword,
    UserCreate,
    UserUpdate,
)

from src.models import User


@pytest.mark.asyncio
async def test_get_users(user_repository, mock_session, mock_user):
    """Тест получения списка пользователей с пагинацией."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_user]
    mock_session.execute = AsyncMock(return_value=mock_result)

    pagination = Pagination(page=1, page_size=10)
    users = await user_repository.get_users(pagination)

    assert users == [mock_user]
    assert len(users) == 1
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_users_empty(user_repository, mock_session):
    """Тест получения пустого списка пользователей."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute = AsyncMock(return_value=mock_result)

    pagination = Pagination(page=1, page_size=10)
    users = await user_repository.get_users(pagination)

    assert users == []
    assert len(users) == 0


@pytest.mark.asyncio
async def test_get_user_success(user_repository, mock_session, mock_user):
    """Тест успешного получения пользователя по ID."""
    mock_session.get = AsyncMock(return_value=mock_user)

    user = await user_repository.get_user(1)

    assert user == mock_user
    mock_session.get.assert_called_once_with(User, 1)


@pytest.mark.asyncio
async def test_get_user_not_found(user_repository, mock_session):
    """Тест получения несуществующего пользователя."""
    mock_session.get = AsyncMock(return_value=None)

    user = await user_repository.get_user(999)

    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_id_success(user_repository, mock_session, mock_user):
    """Тест успешного получения пользователя с проверкой существования."""
    mock_session.get = AsyncMock(return_value=mock_user)

    user = await user_repository.get_user_by_id(1)

    assert user == mock_user


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_repository, mock_session):
    """Тест ошибки при получении несуществующего пользователя."""
    mock_session.get = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await user_repository.get_user_by_id(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "This user not found!"


@pytest.mark.asyncio
async def test_get_user_by_email_success(user_repository, mock_session, mock_user):
    """Тест успешного получения пользователя по email."""
    mock_session.scalar = AsyncMock(return_value=mock_user)

    user = await user_repository.get_user_by_email("test@example.com")

    assert user == mock_user
    mock_session.scalar.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(user_repository, mock_session):
    """Тест ошибки при получении пользователя по не существующему email."""
    mock_session.scalar = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await user_repository.get_user_by_email("nonexistent@example.com")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "This user with email not found!"


@pytest.mark.asyncio
async def test_get_user_by_email_optional_success(
    user_repository, mock_session, mock_user
):
    """Тест успешного опционального получения пользователя."""
    mock_session.scalar = AsyncMock(return_value=mock_user)

    user = await user_repository.get_user_by_email_optional("test@example.com")

    assert user == mock_user


@pytest.mark.asyncio
async def test_get_user_by_email_optional_none(user_repository, mock_session):
    """Тест опционального получения несуществующего пользователя."""
    mock_session.scalar = AsyncMock(return_value=None)

    user = await user_repository.get_user_by_email_optional("nonexistent@example.com")

    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_confirm_code_success(
    user_repository, mock_session, mock_user
):
    """Тест успешного получения пользователя по коду подтверждения."""
    mock_session.scalar = AsyncMock(return_value=mock_user)

    user = await user_repository.get_user_by_confirm_code("123456")

    assert user == mock_user


@pytest.mark.asyncio
async def test_get_user_by_confirm_code_not_found(user_repository, mock_session):
    """Тест ошибки при неверном коде подтверждения."""
    mock_session.scalar = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await user_repository.get_user_by_confirm_code("000000")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "This user with confirmation code not found!"


@pytest.mark.asyncio
async def test_get_user_with_profile(
    user_repository, mock_session, mock_user, mock_profile
):
    """Тест получения пользователя с профилем."""
    mock_user.profile = mock_profile
    mock_session.scalar = AsyncMock(return_value=mock_user)

    user = await user_repository.get_user_with_profile(mock_user)

    assert user == mock_user
    assert user.profile == mock_profile


@pytest.mark.asyncio
async def test_create_user_profile(user_repository, mock_session, mock_user):
    """Тест создания профиля пользователя."""
    await user_repository.create_user_profile(mock_user)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_success(user_repository, mock_session):
    """Тест успешного создания пользователя."""
    mock_session.scalar = AsyncMock(return_value=None)

    user_create = UserCreate(
        email="new@example.com", password="secret123", repeat_password="secret123"
    )

    with patch(
        "src.api.repositories.user_repository.security.get_hashed_password",
        return_value="hashed_password",
    ):
        user = await user_repository.create_user(user_create)

        assert user is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_duplicate_email(user_repository, mock_session, mock_user):
    """Тест ошибки при создании пользователя с существующим email."""
    mock_session.scalar = AsyncMock(return_value=mock_user)

    user_create = UserCreate(
        email="test@example.com", password="secret123", repeat_password="secret123"
    )

    with pytest.raises(HTTPException) as exc_info:
        await user_repository.create_user(user_create)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "This email is already being used by another user!"


@pytest.mark.asyncio
async def test_create_user_passwords_not_match(user_repository, mock_session):
    """Тест ошибки при несовпадающих паролях."""
    mock_session.scalar = AsyncMock(return_value=None)

    user_create = UserCreate(
        email="new@example.com", password="secret123", repeat_password="different"
    )

    with pytest.raises(HTTPException) as exc_info:
        await user_repository.create_user(user_create)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Passwords must be equals!"


@pytest.mark.asyncio
async def test_update_user(user_repository, mock_session, mock_user):
    """Тест обновления пользователя."""
    user_update = UserUpdate(email="updated@example.com")

    updated_user = await user_repository.update_user(user_update, mock_user)

    assert updated_user == mock_user
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_profile(user_repository, mock_session, mock_profile):
    """Тест обновления профиля."""
    profile_update = ProfileUpdate(
        name="testtest", email="test@gmail.com", photo="test"
    )

    updated_profile = await user_repository.update_user_profile(
        profile_update, mock_profile
    )

    assert updated_profile == mock_profile
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_password_success(user_repository, mock_session, mock_user):
    """Тест успешной смены пароля."""
    update_password = AuthUpdatePassword(
        old_password="old_password",
        new_password="new_password",
        repeat_new_password="new_password",
    )

    with (
        patch(
            "src.api.repositories.user_repository.security.verify_password",
            return_value=True,
        ),
        patch(
            "src.api.repositories.user_repository.security.get_hashed_password",
            return_value="new_hash",
        ),
    ):
        user = await user_repository.update_user_password(mock_user, update_password)

        assert user == mock_user
        mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_password_wrong_old(user_repository, mock_session, mock_user):
    """Тест ошибки при неверном старом пароле."""
    update_password = AuthUpdatePassword(
        old_password="wrong_old",
        new_password="new_password",
        repeat_new_password="new_password",
    )

    with patch(
        "src.api.repositories.user_repository.security.verify_password",
        return_value=False,
    ):
        with pytest.raises(HTTPException) as exc_info:
            await user_repository.update_user_password(mock_user, update_password)

        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Invalid password!"


@pytest.mark.asyncio
async def test_update_user_password_not_match(user_repository, mock_session, mock_user):
    """Тест ошибки при несовпадающих новых паролях."""
    update_password = AuthUpdatePassword(
        old_password="old_password",
        new_password="new_password",
        repeat_new_password="different",
    )

    with pytest.raises(HTTPException) as exc_info:
        await user_repository.update_user_password(mock_user, update_password)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Passwords must be equals!"


@pytest.mark.asyncio
async def test_recovery_user_password_success(user_repository, mock_session, mock_user):
    """Тест успешного восстановления пароля."""
    update_password = UnAuthUpdatePassword(
        confirm_code="123456",
        new_password="new_password",
        repeat_new_password="new_password",
    )

    with patch(
        "src.api.repositories.user_repository.security.get_hashed_password",
        return_value="new_hash",
    ):
        user = await user_repository.recovery_user_password(mock_user, update_password)

        assert user == mock_user
        assert mock_user.confirm_code is None
        mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_recovery_user_password_not_match(
    user_repository, mock_session, mock_user
):
    """Тест ошибки восстановления с несовпадающими паролями."""
    update_password = UnAuthUpdatePassword(
        confirm_code="123456",
        new_password="new_password",
        repeat_new_password="different",
    )

    with pytest.raises(HTTPException) as exc_info:
        await user_repository.recovery_user_password(mock_user, update_password)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Passwords must be equals!"


@pytest.mark.asyncio
async def test_upload_file(user_repository):
    """Тест загрузки файла."""
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.read = AsyncMock(return_value=b"file_content")
    mock_file.filename = "test.jpg"

    mock_file_handle = AsyncMock()
    mock_file_context = AsyncMock()
    mock_file_context.__aenter__ = AsyncMock(return_value=mock_file_handle)
    mock_file_context.__aexit__ = AsyncMock(return_value=None)

    with patch(
        "src.api.repositories.user_repository.aiofiles.open",
        return_value=mock_file_context,
    ):
        file_url = await user_repository.upload_file(mock_file, 1, "avatar")

        assert file_url is not None
        assert "avatar_1.jpg" in file_url
        mock_file_handle.write.assert_called_once_with(b"file_content")


@pytest.mark.asyncio
async def test_get_user_with_projects(
    user_repository, mock_session, mock_user, mock_project
):
    """Тест получения пользователя с проектами."""
    mock_user.project = [mock_project]
    mock_session.scalar = AsyncMock(return_value=mock_user)

    user = await user_repository.get_user_with_projects(mock_user)

    assert user == mock_user
    assert mock_project in user.project


@pytest.mark.asyncio
async def test_get_project_by_id_success(user_repository, mock_session, mock_project):
    """Тест успешного получения проекта."""
    mock_session.scalar = AsyncMock(return_value=mock_project)

    project = await user_repository.get_project_by_id(1)

    assert project == mock_project


@pytest.mark.asyncio
async def test_get_project_by_id_not_found(user_repository, mock_session):
    """Тест ошибки при получении несуществующего проекта."""
    mock_session.scalar = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await user_repository.get_project_by_id(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Project not found!"


@pytest.mark.asyncio
async def test_create_user_project(user_repository, mock_session, mock_user):
    """Тест создания проекта."""
    project_create = CreateUserProject(name="New Project", icon="icon.png")

    project = await user_repository.create_user_project(project_create, mock_user)

    assert project is not None
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_user)


@pytest.mark.asyncio
async def test_update_project_success(
    user_repository, mock_session, mock_user, mock_project
):
    """Тест успешного обновления проекта."""
    mock_session.scalar = AsyncMock(return_value=mock_project)

    project_update = UpdateUserProject(id=1, name="testtest", icon="testtest")

    updated_project = await user_repository.update_project(mock_user, project_update)

    assert updated_project == mock_project
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_project)


@pytest.mark.asyncio
async def test_update_project_not_found(user_repository, mock_session, mock_user):
    """Тест ошибки обновления несуществующего проекта."""
    mock_session.scalar = AsyncMock(return_value=None)

    project_update = UpdateUserProject(id=999, name="testtest", icon="testtest")

    with pytest.raises(HTTPException) as exc_info:
        await user_repository.update_project(mock_user, project_update)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "This project not found!"


@pytest.mark.asyncio
async def test_delete_project_success(
    user_repository, mock_session, mock_user, mock_project
):
    """Тест успешного удаления проекта."""
    with patch.object(user_repository, "get_project_by_id", return_value=mock_project):
        result = await user_repository.delete_project(1, mock_user)

        assert result == {"Success": True}
        mock_session.delete.assert_called_once_with(mock_project)
        mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_project_not_owner(
    user_repository, mock_session, mock_user, mock_project
):
    """Тест ошибки удаления чужого проекта."""
    mock_project.owner_id = 2  # Другой владелец

    with patch.object(user_repository, "get_project_by_id", return_value=mock_project):
        with pytest.raises(HTTPException) as exc_info:
            await user_repository.delete_project(1, mock_user)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "This project not found!"


@pytest.mark.asyncio
async def test_get_user_with_categories(
    user_repository, mock_session, mock_user, mock_category
):
    """Тест получения пользователя с категориями."""
    mock_user.category = [mock_category]
    mock_session.scalar = AsyncMock(return_value=mock_user)

    user = await user_repository.get_user_with_categories(mock_user)

    assert user == mock_user
    assert mock_category in user.category


@pytest.mark.asyncio
async def test_get_categories(user_repository, mock_session, mock_category):
    """Тест получения списка категорий."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_category]
    mock_session.execute = AsyncMock(return_value=mock_result)

    pagination = Pagination(page=1, page_size=10)
    categories = await user_repository.get_categories(pagination)

    assert categories == [mock_category]
    assert len(categories) == 1


@pytest.mark.asyncio
async def test_get_category_by_id_success(user_repository, mock_session, mock_category):
    """Тест успешного получения категории."""
    mock_session.scalar = AsyncMock(return_value=mock_category)

    category = await user_repository.get_category_by_id(1)

    assert category == mock_category


@pytest.mark.asyncio
async def test_get_category_by_id_not_found(user_repository, mock_session):
    """Тест ошибки при получении несуществующей категории."""
    mock_session.scalar = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await user_repository.get_category_by_id(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "This category not found!"


@pytest.mark.asyncio
async def test_create_category(user_repository, mock_session, mock_user):
    """Тест создания категории."""
    category_create = CategoryCreate(name="testtest", marker="#123456")

    category = await user_repository.create_category(category_create, mock_user)

    assert category is not None
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_tasks(user_repository, mock_session, mock_task):
    """Тест получения списка задач."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_task]
    mock_session.execute = AsyncMock(return_value=mock_result)

    pagination = Pagination(page=1, page_size=10)
    tasks = await user_repository.get_tasks(pagination)

    assert tasks == [mock_task]
    assert len(tasks) == 1


@pytest.mark.asyncio
async def test_get_task_by_id_success(user_repository, mock_session, mock_task):
    """Тест успешного получения задачи."""
    mock_session.scalar = AsyncMock(return_value=mock_task)

    task = await user_repository.get_task_by_id(1)

    assert task == mock_task


@pytest.mark.asyncio
async def test_get_task_by_id_not_found(user_repository, mock_session):
    """Тест ошибки при получении несуществующей задачи."""
    mock_session.scalar = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await user_repository.get_task_by_id(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "This task not found!"


@pytest.mark.asyncio
async def test_get_user_tasks(user_repository, mock_session, mock_task):
    """Тест получения задач пользователя."""
    mock_session.scalars = AsyncMock(return_value=[mock_task])

    pagination = Pagination(page=1, page_size=10)
    tasks = await user_repository.get_user_tasks(1, pagination)

    assert tasks == [mock_task]


@pytest.mark.asyncio
async def test_get_user_tasks_info(user_repository, mock_session, mock_task):
    """Тест получения информации о задачах пользователя."""
    mock_task.status = TaskStatus.COMPLETED
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_task]
    mock_session.execute = AsyncMock(return_value=mock_result)

    tasks_info = await user_repository.get_user_tasks_info(1)

    assert tasks_info is not None
    assert tasks_info.all_tasks == 1
    assert tasks_info.completed_tasks == 1


@pytest.mark.asyncio
async def test_create_task(user_repository, mock_session, mock_user, mock_task):
    """Тест создания задачи."""
    task_create = MagicMock(spec=TaskCreate)
    task_create.title = "New Task"
    task_create.assignee_id = 1
    task_create.project_id = 1
    task_create.category_id = 1
    task_create.model_dump.return_value = {
        "title": "New Task",
        "assignee_id": 1,
        "project_id": 1,
        "category_id": 1,
    }

    with (
        patch.object(user_repository, "get_user_by_id", return_value=mock_user),
        patch.object(user_repository, "get_project_by_id", return_value=MagicMock()),
        patch.object(user_repository, "get_category_by_id", return_value=MagicMock()),
    ):
        task = await user_repository.create_task(task_create, mock_user)

        assert task is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_complete_task(user_repository, mock_session, mock_task):
    """Тест завершения задачи."""
    with patch.object(user_repository, "get_task_by_id", return_value=mock_task):
        completed_task = await user_repository.complete_task(1)

        assert completed_task.status == TaskStatus.COMPLETED
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(mock_task)


@pytest.mark.asyncio
async def test_get_user_priority_tasks(user_repository, mock_session, mock_task):
    """Тест получения задач по приоритету."""
    mock_session.scalars = AsyncMock(return_value=[mock_task])

    pagination = Pagination(page=1, page_size=10)
    tasks = await user_repository.get_user_priority_tasks(
        1, pagination, [TaskPriority.VERY_URGENT]
    )

    assert tasks == [mock_task]
