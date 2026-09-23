from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "MyPassword123"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(
        password,
        hashed_password,
    )


def test_wrong_password_fails():
    password = "MyPassword123"

    hashed_password = hash_password(password)

    assert not verify_password(
        "WrongPassword",
        hashed_password,
    )


def test_create_and_decode_access_token():

    token = create_access_token(
        user_id=10,
        role="STAFF",
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "10"
    assert payload["role"] == "STAFF"
    assert "exp" in payload