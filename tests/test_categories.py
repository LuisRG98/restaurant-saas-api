from app.models.category import Category
from app.models.user import User


def create_category(
    client,
    token,
    name="Burgers",
):
    return client.post(
        "/api/v1/categories/",
        json={
            "name": name,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

def test_admin_can_create_category(
    client,
    admin_token,
):
    response = create_category(
        client,
        admin_token,
        "Burgers",
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Burgers"
    assert data["restaurant_id"] is not None
    assert data["id"] is not None


def test_manager_can_create_category(
    client,
    manager_token,
):
    response = create_category(
        client,
        manager_token,
        "Drinks",
    )

    assert response.status_code == 201


def test_staff_cannot_create_category(
    client,
    staff_token,
):
    response = create_category(
        client,
        staff_token,
        "Desserts",
    )

    assert response.status_code == 403


def test_create_category_missing_name(
    client,
    admin_token,
):
    response = client.post(
        "/api/v1/categories/",
        json={},
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 422


def test_create_category_invalid_name_type(
    client,
    admin_token,
):
    response = client.post(
        "/api/v1/categories/",
        json={
            "name": 123,
        },
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 422


def test_get_categories_without_token(
    client,
):
    response = client.get(
        "/api/v1/categories/"
    )

    assert response.status_code == 401


def test_get_categories_with_invalid_token(
    client,
):
    response = client.get(
        "/api/v1/categories/",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401


def test_staff_can_get_categories(
    client,
    staff_token,
):
    response = client.get(
        "/api/v1/categories/",
        headers={
            "Authorization": f"Bearer {staff_token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_admin_can_get_categories(
    client,
    admin_token,
):
    response = client.get(
        "/api/v1/categories/",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200


def test_get_category(
    client,
    admin_token,
):
    create_response = create_category(
        client,
        admin_token,
        "Burgers",
    )

    category_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/categories/{category_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == category_id
    assert data["name"] == "Burgers"


def test_get_category_not_found(
    client,
    admin_token,
):
    response = client.get(
        "/api/v1/categories/999999",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 404


def test_user_cannot_get_category_from_other_restaurant(
    client,
    admin_token,
    manager_token,
):
    create_response = create_category(
        client,
        admin_token,
        "Private Category",
    )

    category_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/categories/{category_id}",
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
    )

    assert response.status_code == 404


def test_admin_can_update_category(
    client,
    admin_token,
):
    create_response = create_category(
        client,
        admin_token,
        "Burgers",
    )

    category_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/categories/{category_id}",
        json={
            "name": "Premium Burgers",
        },
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == category_id
    assert data["name"] == "Premium Burgers"


def test_manager_can_update_category(
    client,
    manager_token,
):
    create_response = create_category(
        client,
        manager_token,
        "Drinks",
    )

    category_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/categories/{category_id}",
        json={
            "name": "Cold Drinks",
        },
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
    )

    assert response.status_code == 200


def test_staff_cannot_update_category(
    client,
    staff_token,
):
    response = client.patch(
        "/api/v1/categories/999999",
        json={
            "name": "Hacked",
        },
        headers={
            "Authorization": f"Bearer {staff_token}",
        },
    )

    assert response.status_code == 403


def test_admin_can_delete_category(
    client,
    admin_token,
):
    create_response = create_category(
        client,
        admin_token,
        "Temporary",
    )

    category_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/categories/{category_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 204


def test_manager_can_delete_category(
    client,
    manager_token,
):
    create_response = create_category(
        client,
        manager_token,
        "Temporary",
    )

    category_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/categories/{category_id}",
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
    )

    assert response.status_code == 204


def test_staff_cannot_delete_category(
    client,
    staff_token,
):
    response = client.delete(
        "/api/v1/categories/999999",
        headers={
            "Authorization": f"Bearer {staff_token}",
        },
    )

    assert response.status_code == 403


def test_delete_category_not_found(
    client,
    admin_token,
):
    response = client.delete(
        "/api/v1/categories/999999",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 404


def test_user_cannot_update_category_from_other_restaurant(
    client,
    admin_token,
    manager_token,
):
    create_response = create_category(
        client,
        admin_token,
        "Private Category",
    )

    category_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/categories/{category_id}",
        json={
            "name": "Should Not Work",
        },
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
    )

    assert response.status_code == 404


def test_user_cannot_delete_category_from_other_restaurant(
    client,
    admin_token,
    manager_token,
):
    create_response = create_category(
        client,
        admin_token,
        "Private Category",
    )

    category_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/categories/{category_id}",
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
    )

    assert response.status_code == 404