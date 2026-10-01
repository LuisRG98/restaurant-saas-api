from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.services.auth_service import AuthService
from app.services.onboarding_service import OnboardingService


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
    service = OnboardingService(db)

    return service.register_restaurant_admin(
        email=user_data.email,
        password=user_data.password,
        restaurant_name=user_data.restaurant_name,
        restaurant_address=user_data.restaurant_address,
        restaurant_phone=user_data.restaurant_phone,
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