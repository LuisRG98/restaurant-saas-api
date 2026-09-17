from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ConflictException

from app.models.restaurant import Restaurant
from app.repositories.restaurant import RestaurantRepository
from app.core.exceptions import NotFoundException
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantService:

    def __init__(self, db: Session):
        self.repository = RestaurantRepository(db)

    def create(
        self,
        data: RestaurantCreate
    ) -> Restaurant:

        restaurant = Restaurant(
            name=data.name,
            address=data.address,
            phone=data.phone,
        )

        try:
            return self.repository.create(restaurant)

        except IntegrityError:
            raise ConflictException(
                "A restaurant with this name already exists"
            )

    def get_restaurant(
        self,
        restaurant_id: int,
    ) -> Restaurant:

        restaurant = self.repository.get_by_id(restaurant_id)

        if restaurant is None:
            raise NotFoundException(
                f"Restaurant with id {restaurant_id} not found"
            )

        return restaurant

    def get_all(self) -> list[Restaurant]:

        return self.repository.get_all()
    
    def update_restaurant(
        self,
        restaurant_id: int,
        restaurant_data: RestaurantUpdate,
    ) -> Restaurant:

        restaurant = self.repository.get_by_id(restaurant_id)

        if restaurant is None:
            raise NotFoundException(
                f"Restaurant with id {restaurant_id} not found"
            )

        update_data = restaurant_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(restaurant, field, value)

        return self.repository.update(restaurant)
    

    def delete_restaurant(
        self,
        restaurant_id: int,
    ) -> None:

        restaurant = self.repository.get_by_id(restaurant_id)

        if restaurant is None:
            raise NotFoundException(
                f"Restaurant with id {restaurant_id} not found"
            )

        self.repository.delete(restaurant)