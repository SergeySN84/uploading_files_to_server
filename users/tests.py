import pytest
import random
import string
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.fixture
def admin_user():
    """Фикстура: администратор с правами суперпользователя."""
    return User.objects.create_superuser(
        username="admin_test", email="admin@test.com", password="adminpass123"
    )


@pytest.fixture
def api_client():
    """Фикстура: клиент для API-запросов."""
    return APIClient()


@pytest.mark.django_db
def test_user_flow(admin_user, api_client):
    """
    Тестовый сценарий с использованием SimpleJWT.
    """
    api_client.force_authenticate(user=admin_user)

    # Генерация 3 пользователей
    users_data = []
    for i in range(3):
        username = (
            f"testuser_{i}_{''.join(random.choices(string.ascii_lowercase, k=6))}"
        )
        email = f"{username}@example.com"
        password = "SecurePass123!"

        response = api_client.post(
            "/api/users/",
            {"username": username, "email": email, "password": password},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        users_data.append(
            {"id": response.data["id"], "username": username, "password": password}
        )

    # Проверка количества в БД
    assert User.objects.filter(username__startswith="testuser_").count() == 3

    # Проверка авторизации через JWT
    for user in users_data:
        login_resp = api_client.post(
            "/api/token/",
            {"username": user["username"], "password": user["password"]},
            format="json",
        )

        assert login_resp.status_code == status.HTTP_200_OK
        assert "access" in login_resp.data
        assert "refresh" in login_resp.data

    # Удаление
    for user in users_data:
        delete_resp = api_client.delete(f"/api/users/{user['id']}/")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

    assert User.objects.filter(username__startswith="testuser_").count() == 0
