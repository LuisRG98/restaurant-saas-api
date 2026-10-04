from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ConflictException,
    ForbiddenException,
    NotFoundException,
)
from app.core.security import hash_password
from app.core.roles import UserRole
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
    

    def update_user(
        self,
        user_id: int,
        email: str | None,
        role: UserRole | None,
        is_active: bool | None,
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

        # Tenant isolation
        if user.restaurant_id != current_user.restaurant_id:
            raise NotFoundException(
                f"User with id {user_id} not found"
            )

        # Prevent modifying yourself through this endpoint
        if user.id == current_user.id:
            raise ForbiddenException(
                "You cannot modify your own account through this endpoint"
            )

        # Role permissions
        if current_user.role == UserRole.MANAGER.value:
            if user.role != UserRole.STAFF.value:
                raise ForbiddenException()

            if role is not None and role != UserRole.STAFF:
                raise ForbiddenException()

        elif current_user.role == UserRole.ADMIN.value:
            if user.role == UserRole.ADMIN.value:
                raise ForbiddenException()

            if role == UserRole.ADMIN:
                raise ForbiddenException()

        else:
            raise ForbiddenException()

        if email is not None:
            existing_user = self.repository.get_by_email(email)

            if (
                existing_user is not None
                and existing_user.id != user.id
            ):
                raise ConflictException(
                    "A user with this email already exists"
                )

            user.email = email

        if role is not None:
            user.role = role.value

        if is_active is not None:
            user.is_active = is_active

        try:
            self.db.commit()
            self.db.refresh(user)
            return user

        except IntegrityError:
            self.db.rollback()
            raise ConflictException(
                "A user with this email already exists"
            )