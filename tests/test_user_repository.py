from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository


def test_create_user(db):
    repository = UserRepository(db)

    user = User(
        email="test@example.com",
        password_hash=hash_password("Password123"),
        role="STAFF",
        is_active=True,
    )

    created_user = repository.create(user)

    assert created_user.id is not None
    assert created_user.email == "test@example.com"
    assert created_user.password_hash != "Password123"


def test_get_user_by_email(db):
    repository = UserRepository(db)

    user = User(
        email="search@example.com",
        password_hash=hash_password("Password123"),
        role="STAFF",
        is_active=True,
    )

    repository.create(user)

    found_user = repository.get_by_email(
        "search@example.com"
    )

    assert found_user is not None
    assert found_user.email == "search@example.com"


def test_get_user_by_email_not_found(db):
    repository = UserRepository(db)

    found_user = repository.get_by_email(
        "doesnotexist@example.com"
    )

    assert found_user is None