from unittest.mock import patch

from app.models.restaurant import Restaurant
from app.models.user import User


def register_payload(
    email: str = "owner@example.com",
    restaurant_name: str = "Test Restaurant",
):
    return {
        "email": email,
        "password": "Password123",
        "restaurant_name": restaurant_name,
        "restaurant_address": "Test Address",
        "restaurant_phone": "70000000",
    }


def test_register_creates_restaurant_and_admin(
    client,
    db,
):
    response = client.post(
        "/auth/register",
        json=register_payload(),
    )

    assert response.status_code == 201

    data = response.json()

    user = db.get(User, data["id"])

    assert user is not None
    assert user.email == "owner@example.com"
    assert user.role == "ADMIN"
    assert user.restaurant_id is not None

    restaurant = db.get(
        Restaurant,
        user.restaurant_id,
    )

    assert restaurant is not None
    assert restaurant.name == "Test Restaurant"
    assert restaurant.address == "Test Address"
    assert restaurant.phone == "70000000"


def test_register_duplicate_email_returns_409(
    client,
):
    first_response = client.post(
        "/auth/register",
        json=register_payload(
            email="duplicate@example.com",
            restaurant_name="Restaurant One",
        ),
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json=register_payload(
            email="duplicate@example.com",
            restaurant_name="Restaurant Two",
        ),
    )

    assert second_response.status_code == 409


def test_register_duplicate_restaurant_name_returns_409(
    client,
):
    first_response = client.post(
        "/auth/register",
        json=register_payload(
            email="owner1@example.com",
            restaurant_name="Same Restaurant",
        ),
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json=register_payload(
            email="owner2@example.com",
            restaurant_name="Same Restaurant",
        ),
    )

    assert second_response.status_code == 409