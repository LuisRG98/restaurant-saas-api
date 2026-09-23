from app.models.restaurant import Restaurant
from app.models.user import User


def register_user(client, email: str):
    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "Password123",
        },
    )

    assert response.status_code == 201

    return response.json()


def set_user_role(db, user_id: int, role: str):
    user = db.get(User, user_id)

    assert user is not None

    user.role = role
    db.commit()
    db.refresh(user)


def login_user(client, email: str):
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def auth_headers(token: str):
    return {
        "Authorization": f"Bearer {token}",
    }


def create_restaurant(db):
    restaurant = Restaurant(
        name="Test Restaurant",
        address="Test Address",
        phone="123456789",
    )

    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    return restaurant


def test_staff_can_get_restaurants(
    client,
    db,
):
    user = register_user(
        client,
        "staff-get@example.com",
    )

    token = login_user(
        client,
        "staff-get@example.com",
    )

    response = client.get(
        "/restaurants/",
        headers=auth_headers(token),
    )

    assert response.status_code == 200


def test_staff_cannot_create_restaurant(
    client,
    db,
):
    user = register_user(
        client,
        "staff-create@example.com",
    )

    token = login_user(
        client,
        "staff-create@example.com",
    )

    response = client.post(
        "/restaurants/",
        headers=auth_headers(token),
        json={
            "name": "Staff Restaurant",
            "address": "Staff Address",
            "phone": "111111111",
        },
    )

    assert response.status_code == 403


def test_staff_cannot_update_restaurant(
    client,
    db,
):
    user = register_user(
        client,
        "staff-update@example.com",
    )

    restaurant = create_restaurant(db)

    token = login_user(
        client,
        "staff-update@example.com",
    )

    response = client.patch(
        f"/restaurants/{restaurant.id}",
        headers=auth_headers(token),
        json={
            "name": "Updated by Staff",
        },
    )

    assert response.status_code == 403


def test_staff_cannot_delete_restaurant(
    client,
    db,
):
    user = register_user(
        client,
        "staff-delete@example.com",
    )

    restaurant = create_restaurant(db)

    token = login_user(
        client,
        "staff-delete@example.com",
    )

    response = client.delete(
        f"/restaurants/{restaurant.id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 403


def test_manager_can_create_restaurant(
    client,
    db,
):
    user = register_user(
        client,
        "manager-create@example.com",
    )

    set_user_role(
        db,
        user["id"],
        "MANAGER",
    )

    token = login_user(
        client,
        "manager-create@example.com",
    )

    response = client.post(
        "/restaurants/",
        headers=auth_headers(token),
        json={
            "name": "Manager Restaurant",
            "address": "Manager Address",
            "phone": "222222222",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Manager Restaurant"


def test_manager_can_update_restaurant(
    client,
    db,
):
    user = register_user(
        client,
        "manager-update@example.com",
    )

    set_user_role(
        db,
        user["id"],
        "MANAGER",
    )

    restaurant = create_restaurant(db)

    token = login_user(
        client,
        "manager-update@example.com",
    )

    response = client.patch(
        f"/restaurants/{restaurant.id}",
        headers=auth_headers(token),
        json={
            "name": "Updated by Manager",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated by Manager"


def test_manager_cannot_delete_restaurant(
    client,
    db,
):
    user = register_user(
        client,
        "manager-delete@example.com",
    )

    set_user_role(
        db,
        user["id"],
        "MANAGER",
    )

    restaurant = create_restaurant(db)

    token = login_user(
        client,
        "manager-delete@example.com",
    )

    response = client.delete(
        f"/restaurants/{restaurant.id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 403


def test_admin_can_create_restaurant(
    client,
    db,
):
    user = register_user(
        client,
        "admin-create@example.com",
    )

    set_user_role(
        db,
        user["id"],
        "ADMIN",
    )

    token = login_user(
        client,
        "admin-create@example.com",
    )

    response = client.post(
        "/restaurants/",
        headers=auth_headers(token),
        json={
            "name": "Admin Restaurant",
            "address": "Admin Address",
            "phone": "333333333",
        },
    )

    assert response.status_code == 201


def test_admin_can_update_restaurant(
    client,
    db,
):
    user = register_user(
        client,
        "admin-update@example.com",
    )

    set_user_role(
        db,
        user["id"],
        "ADMIN",
    )

    restaurant = create_restaurant(db)

    token = login_user(
        client,
        "admin-update@example.com",
    )

    response = client.patch(
        f"/restaurants/{restaurant.id}",
        headers=auth_headers(token),
        json={
            "name": "Updated by Admin",
        },
    )

    assert response.status_code == 200


def test_admin_can_delete_restaurant(
    client,
    db,
):
    user = register_user(
        client,
        "admin-delete@example.com",
    )

    set_user_role(
        db,
        user["id"],
        "ADMIN",
    )

    restaurant = create_restaurant(db)

    token = login_user(
        client,
        "admin-delete@example.com",
    )

    response = client.delete(
        f"/restaurants/{restaurant.id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 204