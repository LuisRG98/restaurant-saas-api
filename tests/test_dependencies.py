from app.core.security import create_access_token
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_current_user_with_valid_token(client):

    register_response = client.post(
        "/auth/register",
        json={
            "email": "current@example.com",
            "password": "Password123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "current@example.com",
            "password": "Password123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "current@example.com"
    assert data["role"] == "STAFF"
    assert data["is_active"] is True


def test_get_current_user_without_token(client):

    response = client.get("/users/me")

    assert response.status_code == 401


def test_get_current_user_with_invalid_token(client):

    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401