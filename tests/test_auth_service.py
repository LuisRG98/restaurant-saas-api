from app.core.security import verify_password
from app.services.auth_service import AuthService
from app.core.exceptions import ConflictException


def test_register_user(db):
    service = AuthService(db)

    user = service.register_user(
        email="newuser@example.com",
        password="Password123",
    )

    assert user.id is not None
    assert user.email == "newuser@example.com"
    assert user.role == "STAFF"
    assert user.is_active is True

    assert user.password_hash != "Password123"

    assert verify_password(
        "Password123",
        user.password_hash,
    )


def test_register_duplicate_email(db):
    service = AuthService(db)

    service.register_user(
        email="duplicate@example.com",
        password="Password123",
    )

    try:
        service.register_user(
            email="duplicate@example.com",
            password="AnotherPassword123",
        )

        assert False, "Expected ConflictException"

    except ConflictException as exc:
        assert exc.message == (
            "A user with this email already exists"
        )