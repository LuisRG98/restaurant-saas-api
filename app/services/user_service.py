from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ConflictException,
    ForbiddenException,
    NotFoundException,
)
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def get_users(
        self,
        current_user: User,
    ) -> list[User]:

        if current_user.restaurant_id is None:
            return []

        return self.repository.get_all_by_restaurant(
            current_user.restaurant_id
        )

    def create_user(
        self,
        email: str,
        password: str,
        role: str,
        current_user: User,
    ) -> User:

        allowed_roles = {"STAFF", "MANAGER"}

        if role not in allowed_roles:
            raise ForbiddenException(
                "You cannot create this role"
            )

        if role == "MANAGER" and current_user.role != "ADMIN":
            raise ForbiddenException()

        if current_user.restaurant_id is None:
            raise ForbiddenException()

        existing_user = (
            self.repository.get_by_email(email)
        )

        if existing_user is not None:
            raise ConflictException(
                "A user with this email already exists"
            )

        user = User(
            email=email,
            password_hash=hash_password(password),
            role=role,
            restaurant_id=current_user.restaurant_id,
            is_active=True,
        )

        try:
            user = self.repository.create(user)

            self.db.commit()
            self.db.refresh(user)

            return user

        except IntegrityError:
            self.db.rollback()

            raise ConflictException(
                "A user with this email already exists"
            )
        
    def get_user(
        self,
        user_id: int,
        current_user: User,
    ) -> User:

        if current_user.restaurant_id is None:
            raise NotFoundException(
                f"User with id {user_id} not found"
            )

        user = self.repository.get_by_id(user_id)

        if user is None:
            raise NotFoundException(
                f"User with id {user_id} not found"
            )

        if user.restaurant_id != current_user.restaurant_id:
            raise NotFoundException(
                f"User with id {user_id} not found"
            )

        return user