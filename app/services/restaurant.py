from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.repositories.restaurant import RestaurantRepository
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

        return self.repository.create(restaurant)

    def get_by_id(
        self,
        restaurant_id: int
    ) -> Restaurant:

        restaurant = self.repository.get_by_id(
            restaurant_id
        )

        if restaurant is None:
            raise RestaurantNotFoundError(
                f"Restaurant {restaurant_id} was not found"
            )

        return restaurant

    def get_all(self) -> list[Restaurant]:

        return self.repository.get_all()