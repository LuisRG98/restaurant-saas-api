from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN", "MANAGER")
    ),
):
    service = UserService(db)
    return service.get_users(current_user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN", "MANAGER")
    ),
):
    service = UserService(db)

    return service.get_user(
        user_id=user_id,
        current_user=current_user,
    )


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN", "MANAGER")
    ),
):
    service = UserService(db)

    return service.create_user(
        email=user_data.email,
        password=user_data.password,
        role=user_data.role,
        current_user=current_user,
    )

