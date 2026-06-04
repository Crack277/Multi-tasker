from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException, status

from src.api.schemas.user_schemas import PrintAccessToken
from src.api.utils import security


def test_get_hashed_password():
    """Тест хеширования пароля."""
    password = "secret123"
    hash = security.get_hashed_password(password)

    assert password != hash


def test_verify_password():
    """Тест проверки правильного пароля."""
    password = "secret123"
    hash = security.get_hashed_password(password)

    assert security.verify_password(password, hash)


def test_wrong_verify_password():
    """Тест проверки неправильного пароля."""
    password = "secret123"
    hash = security.get_hashed_password(password)

    assert security.verify_password("wrong", hash) is False


def test_generate_confirm_code():
    """Тест генерации кода подтверждения."""
    first_code = security.generate_confirm_code()
    second_code = security.generate_confirm_code()

    assert first_code != second_code
    assert first_code.isdigit()
    assert len(first_code) == 6


@pytest.mark.asyncio
async def test_create_access_token(mock_user):
    """Тест создания токена доступа."""
    token = await security.create_access_token(mock_user)

    assert isinstance(token, PrintAccessToken)
    assert isinstance(token.access_token, str)
    assert isinstance(token.type, str)
    assert token.type == "Bearer"


@pytest.mark.asyncio
async def test_get_current_user(mock_session, mock_credentials, mock_user):
    """Тест получения текущего пользователя по токену."""
    mock_session.scalar = AsyncMock(return_value=mock_user)

    with (
        patch("src.api.utils.security.redis_client.is_blacklisted", return_value=False),
        patch("src.api.utils.security.jwt.decode", return_value={"user_id": 1}),
    ):

        result = await security.get_current_user(
            session=mock_session, credential=mock_credentials
        )

        assert result == mock_user
        mock_session.scalar.assert_called_once()


@pytest.mark.asyncio
async def test_get_current_user_no_credential(mock_session):
    """Тест ошибки при отсутствии токена авторизации."""
    with pytest.raises(HTTPException) as exc_info:
        await security.get_current_user(
            session=mock_session,
            credential=None,
        )

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Not authenticated"


@pytest.mark.asyncio
async def test_get_current_user_blacklisted_token(mock_session, mock_credentials):
    """Тест ошибки при отозванном токене."""
    with patch("src.api.utils.security.redis_client.is_blacklisted", return_value=True):
        with pytest.raises(HTTPException) as exc_info:
            await security.get_current_user(
                session=mock_session, credential=mock_credentials
            )

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Token has been revoked"