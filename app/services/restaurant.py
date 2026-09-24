from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ConflictException,
    NotFoundException,
)
from app.models.restaurant import Restaurant
from app.models.user import User
from app.repositories.restaurant import RestaurantRepository
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantUpdate,
)


class RestaurantService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = RestaurantRepository(db)

    def create(
        self,
        data: RestaurantCreate,
    ) -> Restaurant:

        restaurant = Restaurant(
            name=data.name,
            address=data.address,
            phone=data.phone,
        )

        try:
            restaurant = self.repository.create(restaurant)

            self.db.commit()
            self.db.refresh(restaurant)

            return restaurant

        except IntegrityError:
            self.db.rollback()

            raise ConflictException(
                "A restaurant with this name already exists"
            )

    def get_restaurant(
        self,
        restaurant_id: int,
        current_user: User,
    ) -> Restaurant:

        if current_user.restaurant_id != restaurant_id:
            raise NotFoundException(
                f"Restaurant with id {restaurant_id} not found"
            )

        restaurant = self.repository.get_by_id(
            restaurant_id
        )

        if restaurant is None:
            raise NotFoundException(
                f"Restaurant with id {restaurant_id} not found"
            )

        return restaurant

    def get_all(
        self,
        current_user: User,
    ) -> list[Restaurant]:

        if current_user.restaurant_id is None:
            return []

        restaurant = self.repository.get_by_id(
            current_user.restaurant_id
        )

        if restaurant is None:
            return []

        return [restaurant]

    def update_restaurant(
        self,
        restaurant_id: int,
        restaurant_data: RestaurantUpdate,
        current_user: User,
    ) -> Restaurant:

        if current_user.restaurant_id != restaurant_id:
            raise NotFoundException(
                f"Restaurant with id {restaurant_id} not found"
            )

        restaurant = self.repository.get_by_id(
            restaurant_id
        )

        if restaurant is None:
            raise NotFoundException(
                f"Restaurant with id {restaurant_id} not found"
            )

        update_data = restaurant_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(restaurant, field, value)

        try:
            restaurant = self.repository.update(
                restaurant
            )

            self.db.commit()
            self.db.refresh(restaurant)

            return restaurant

        except IntegrityError:
            self.db.rollback()

            raise ConflictException(
                "A restaurant with this name already exists"
            )

    def delete_restaurant(
        self,
        restaurant_id: int,
        current_user: User,
    ) -> None:

        if current_user.restaurant_id != restaurant_id:
            raise NotFoundException(
                f"Restaurant with id {restaurant_id} not found"
            )

        restaurant = self.repository.get_by_id(
            restaurant_id
        )

        if restaurant is None:
            raise NotFoundException(
                f"Restaurant with id {restaurant_id} not found"
            )

        try:
            self.repository.delete(restaurant)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise