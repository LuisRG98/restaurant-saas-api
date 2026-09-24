import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.models.user import User


TEST_DATABASE_URL = (
    "postgresql+psycopg://"
    "restaurant_user:"
    "restaurant_password@"
    "127.0.0.1:15432/"
    "restaurant_test_db"
)


test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def staff_token(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "staff@test.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": "staff@test.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def manager_user(client, db):
    response = client.post(
        "/auth/register",
        json={
            "email": "manager@test.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 201

    user_id = response.json()["id"]

    user = db.get(User, user_id)

    assert user is not None

    user.role = "MANAGER"

    db.commit()
    db.refresh(user)

    response = client.post(
        "/auth/login",
        json={
            "email": "manager@test.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return user, token


@pytest.fixture
def admin_user(client, db):
    response = client.post(
        "/auth/register",
        json={
            "email": "admin@test.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 201

    user_id = response.json()["id"]

    user = db.get(User, user_id)

    assert user is not None

    user.role = "ADMIN"

    db.commit()
    db.refresh(user)

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return user, token


@pytest.fixture
def manager_token(manager_user):
    _, token = manager_user

    return token


@pytest.fixture
def admin_token(admin_user):
    _, token = admin_user

    return token


@pytest.fixture
def assign_restaurant_to_user(db):
    def _assign(
        user_id: int,
        restaurant_id: int,
    ):
        user = db.get(User, user_id)

        assert user is not None

        user.restaurant_id = restaurant_id

        db.commit()
        db.refresh(user)

    return _assign