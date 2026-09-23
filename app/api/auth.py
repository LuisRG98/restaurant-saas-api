from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import (
    UserLogin,
    UserRegister,
    UserResponse,
    TokenResponse,
)
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.register_user(
        email=user_data.email,
        password=user_data.password,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    access_token = service.login_user(
        email=user_data.email,
        password=user_data.password,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )