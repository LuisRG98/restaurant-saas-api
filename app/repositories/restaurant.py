from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.restaurant import Restaurant


class RestaurantRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, restaurant: Restaurant) -> Restaurant:
        try:
            self.db.add(restaurant)
            self.db.commit()
            self.db.refresh(restaurant)

            return restaurant

        except Exception:
            self.db.rollback()
            raise

    def get_by_id(
        self,
        restaurant_id: int
    ) -> Restaurant | None:

        statement = (
            select(Restaurant)
            .where(Restaurant.id == restaurant_id)
        )

        return self.db.scalar(statement)

    def get_all(self) -> list[Restaurant]:

        statement = (
            select(Restaurant)
            .order_by(Restaurant.id)
        )

        return list(self.db.scalars(statement).all())
        

    def update(self, restaurant: Restaurant) -> Restaurant:
        try:
            self.db.commit()
            self.db.refresh(restaurant)

            return restaurant

        except Exception:
            self.db.rollback()
            raise

    def delete(self, restaurant: Restaurant) -> None:
        try:
            self.db.delete(restaurant)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise