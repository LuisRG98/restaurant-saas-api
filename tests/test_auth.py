from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_user(client):
    user_data = {
        "email": "register@example.com",
        "password": "Password123",
    }

    response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["email"] == "register@example.com"
    assert data["role"] == "STAFF"
    assert data["is_active"] is True

    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email(client):
    user_data = {
        "email": "duplicate@example.com",
        "password": "Password123",
    }

    first_response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["detail"] == (
        "A user with this email already exists"
    )


def test_register_invalid_email(client):
    user_data = {
        "email": "this-is-not-an-email",
        "password": "Password123",
    }

    response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert response.status_code == 422


def test_login_user(client):

    register_response = client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "Password123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "Password123",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):

    client.post(
        "/auth/register",
        json={
            "email": "wrong-password@example.com",
            "password": "Password123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "wrong-password@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid credentials"


def test_login_nonexistent_user(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "does-not-exist@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid credentials"