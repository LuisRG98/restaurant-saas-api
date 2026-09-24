from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException
from app.core.security import hash_password
from app.models.restaurant import Restaurant
from app.models.user import User
from app.repositories.restaurant import RestaurantRepository
from app.repositories.user_repository import UserRepository


class OnboardingService:

    def __init__(self, db: Session):
        self.db = db
        self.restaurant_repository = RestaurantRepository(db)
        self.user_repository = UserRepository(db)

    def register_restaurant_admin(
        self,
        email: str,
        password: str,
        restaurant_name: str,
        restaurant_address: str,
        restaurant_phone: str,
    ) -> User:

        existing_user = self.user_repository.get_by_email(email)

        if existing_user is not None:
            raise ConflictException(
                "A user with this email already exists"
            )

        restaurant = Restaurant(
            name=restaurant_name,
            address=restaurant_address,
            phone=restaurant_phone,
        )

        try:
            restaurant = self.restaurant_repository.create(
                restaurant
            )

            user = User(
                email=email,
                password_hash=hash_password(password),
                role="ADMIN",
                restaurant_id=restaurant.id,
                is_active=True,
            )

            return self.user_repository.create(user)

        except Exception:
            self.db.rollback()
            raise