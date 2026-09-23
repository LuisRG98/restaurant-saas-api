from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ConflictException,
    UnauthorizedException,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def register_user(
        self,
        email: str,
        password: str,
    ) -> User:

        existing_user = self.repository.get_by_email(email)

        if existing_user is not None:
            raise ConflictException(
                "A user with this email already exists"
            )

        password_hash = hash_password(password)

        user = User(
            email=email,
            password_hash=password_hash,
            role="STAFF",
            is_active=True,
        )

        try:
            return self.repository.create(user)

        except IntegrityError:
            raise ConflictException(
                "A user with this email already exists"
            )
    

    def login_user(
        self,
        email: str,
        password: str,
    ) -> str:  

        user = self.repository.get_by_email(email)

        if user is None:
            raise UnauthorizedException()

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise UnauthorizedException()

        if not user.is_active:
            raise UnauthorizedException()

        return create_access_token(
            user_id=user.id,
            role=user.role,
        )