from typing import Callable

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:

    if credentials is None:
        raise UnauthorizedException()

    try:
        payload = decode_access_token(credentials.credentials)
    except Exception:
        raise UnauthorizedException()

    user_id = payload.get("sub")

    if user_id is None:
        raise UnauthorizedException()

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise UnauthorizedException()

    repository = UserRepository(db)
    user = repository.get_by_id(user_id)

    if user is None:
        raise UnauthorizedException()

    if not user.is_active:
        raise UnauthorizedException()

    return user


def require_role(
    *allowed_roles: str,
) -> Callable:

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        print(
            f"\nDEBUG ROLE -> "
            f"user_id={current_user.id}, "
            f"email={current_user.email}, "
            f"role={current_user.role!r}, "
            f"allowed={allowed_roles!r}\n"
        )

        if current_user.role not in allowed_roles:
            raise ForbiddenException()

        return current_user

    return role_checker