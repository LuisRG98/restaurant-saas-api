from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException
from app.core.security import hash_password
from app.core.roles import UserRole
from app.models.restaurant import Restaurant
from app.models.user import User
from app.repositories.restaurant import RestaurantRepository
from app.repositories.user_repository import UserRepository


class OnboardingService:

    def __init__(self, db: Session):
        self.db = db

        self.restaurant_repository = (
            RestaurantRepository(db)
        )

        self.user_repository = (
            UserRepository(db)
        )

    def register_restaurant_admin(
        self,
        email: str,
        password: str,
        restaurant_name: str,
        restaurant_address: str,
        restaurant_phone: str,
    ) -> User:

        existing_user = (
            self.user_repository.get_by_email(email)
        )

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
            # 1. Create restaurant
            restaurant = (
                self.restaurant_repository.create(
                    restaurant
                )
            )

            # flush() generates restaurant.id
            # without committing the transaction.

            # 2. Create ADMIN user
            user = User(
                email=email,
                password_hash=hash_password(password),
                role=UserRole.ADMIN.value,
                restaurant_id=restaurant.id,
                is_active=True,
            )

            user = self.user_repository.create(user)

            # 3. Everything succeeded
            self.db.commit()

            # 4. Refresh objects from database
            self.db.refresh(user)

            return user

        except IntegrityError:
            self.db.rollback()

            raise ConflictException(
                "Unable to create the restaurant and user"
            )

        except Exception:
            self.db.rollback()
            raise