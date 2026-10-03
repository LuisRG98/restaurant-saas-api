from fastapi.security import HTTPAuthorizationCredentials

from app.core.dependencies import get_current_user
from app.models.user import User

from app.core.security import create_access_token
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_current_user_with_valid_token(
    client,
    db,
):
    response = client.post(
        "/auth/register",
        json={
            "email": "dependency@example.com",
            "password": "Password123",
            "restaurant_name": "Dependency Test Restaurant",
            "restaurant_address": "Dependency Test Address",
            "restaurant_phone": "70000002",
        },
    )

    assert response.status_code == 201

    user_id = response.json()["id"]

    user = db.get(User, user_id)

    assert user is not None

    user.role = "STAFF"

    db.commit()
    db.refresh(user)

    response = client.post(
        "/auth/login",
        json={
            "email": "dependency@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    current_user = get_current_user(
        credentials=credentials,
        db=db,
    )

    assert current_user.id == user.id
    assert current_user.email == "dependency@example.com"
    assert current_user.role == "STAFF"
    assert current_user.is_active is True


def test_get_current_user_without_token(client):

    response = client.get("/api/v1/users/me")

    assert response.status_code == 401


def test_get_current_user_with_invalid_token(client):

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401