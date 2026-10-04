from pydantic import BaseModel, EmailStr
from app.core.roles import UserRole


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    restaurant_name: str
    restaurant_address: str
    restaurant_phone: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: UserRole | None = None
    is_active: bool | None = None