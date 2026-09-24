from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)
prefix="/api/v1/restaurants/"


def test_get_restaurants(client, staff_token):
    response = client.get(
        prefix,
        headers={
            "Authorization": f"Bearer {staff_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_create_restaurant(client, manager_token):
    restaurant_data = {
        "name": "Test Restaurant",
        "address": "Test Address 123",
        "phone": "70000000",
    }

    response = client.post(
        prefix,
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
        json=restaurant_data,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Restaurant"
    assert data["address"] == "Test Address 123"
    assert data["phone"] == "70000000"
    assert "id" in data


def test_get_restaurant_by_id(client, manager_token):
    restaurant_data = {
        "name": "Restaurant For Get Test",
        "address": "Get Test Address",
        "phone": "71111111",
    }

    create_response = client.post(
        prefix,
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
        json=restaurant_data,
    )

    assert create_response.status_code == 201

    restaurant_id = create_response.json()["id"]

    response = client.get(
        f"{prefix}{restaurant_id}",
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == restaurant_id
    assert data["name"] == "Restaurant For Get Test"
    assert data["address"] == "Get Test Address"
    assert data["phone"] == "71111111"


def test_get_restaurant_not_found(client):
    response = client.get("/api/v1/restaurants/999999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Restaurant with id 999999 not found"


def test_update_restaurant(client, manager_token):
    restaurant_data = {
        "name": "Restaurant Before Update",
        "address": "Original Address",
        "phone": "72222222",
    }

    create_response = client.post(
        prefix,
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
        json=restaurant_data,
    )

    assert create_response.status_code == 201

    restaurant_id = create_response.json()["id"]

    response = client.patch(
        f"{prefix}{restaurant_id}",
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
        json={
            "name": "Restaurant After Update",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == restaurant_id
    assert data["name"] == "Restaurant After Update"
    assert data["address"] == "Original Address"
    assert data["phone"] == "72222222"



def test_delete_restaurant(client, admin_token):
    restaurant_data = {
        "name": "Restaurant To Delete",
        "address": "Delete Address",
        "phone": "75555555",
    }

    create_response = client.post(
        prefix,
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json=restaurant_data,
    )

    assert create_response.status_code == 201

    restaurant_id = create_response.json()["id"]

    response = client.delete(
        f"{prefix}{restaurant_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 204

    get_response = client.get(
        f"{prefix}{restaurant_id}"
    )

    assert get_response.status_code == 404


def test_delete_restaurant_not_found(client, admin_token):
    response = client.delete(
        f"{prefix}9999",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Restaurant with id 9999 not found"


def test_create_restaurant_missing_name(
    client,
    manager_token,
):
    restaurant_data = {
        "address": "Test Address",
        "phone": "70000000",
    }

    response = client.post(
        prefix,
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
        json=restaurant_data,
    )

    assert response.status_code == 422
    data = response.json()

    assert "detail" in data
    assert any(
        error["loc"][-1] == "name"
        for error in data["detail"]
    )


def test_create_restaurant_missing_address(    
    client,
    manager_token,
):
    restaurant_data = {
        "name": "Restaurant Without Address",
        "phone": "70000000",
    }

    response = client.post(
        prefix,
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
        json=restaurant_data,
    )

    assert response.status_code == 422
    data = response.json()

    assert "detail" in data
    assert any(
        error["loc"][-1] == "address"
        for error in data["detail"]
    )


def test_create_restaurant_missing_phone(
    client,
    manager_token,):
    restaurant_data = {
        "name": "Restaurant Without Phone",
        "address": "Test Address",
    }

    response = client.post(
        prefix,
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
        json=restaurant_data,
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert any(
        error["loc"][-1] == "phone"
        for error in data["detail"]
    )


def test_create_duplicate_restaurant(
    client,
    manager_token,
):
    restaurant_data = {
        "name": "Duplicate Restaurant",
        "address": "First Address",
        "phone": "70000000",
    }

    first_response = client.post(
        prefix,
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
        json=restaurant_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        prefix,
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
        json=restaurant_data,
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["detail"] == (
        "A restaurant with this name already exists"
    )


def test_create_duplicate_restaurant(
    client,
    manager_token,
):
    restaurant_data = {
        "name": "Duplicate Restaurant",
        "address": "First Address",
        "phone": "70000000",
    }

    first_response = client.post(
        prefix,
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
        json=restaurant_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        prefix,
        headers={
            "Authorization": f"Bearer {manager_token}",
        },
        json=restaurant_data,
    )

    assert second_response.status_code == 409


def test_get_restaurants_without_token(client):
    response = client.get(prefix)

    assert response.status_code == 401


def test_create_restaurant_staff_forbidden(
    client,
    staff_token,
):
    response = client.post(
        prefix,
        headers={
            "Authorization": f"Bearer {staff_token}",
        },
        json={
            "name": "Unauthorized Restaurant",
            "address": "Address",
            "phone": "70000000",
        },
    )

    assert response.status_code == 403