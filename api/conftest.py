import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def admin():
    """Фикстура, возвращающая пользователя со статусом администратора."""
    user = User.objects.create_user(
        username="admin_user",
        email="admin@example.com",
        password="password123",
        is_staff=True,
        is_superuser=True,
    )
    return user


@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    return APIClient()
