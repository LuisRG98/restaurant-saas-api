from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, category: Category) -> Category:
        self.db.add(category)
        self.db.flush()
        return category

    def get_by_id(
        self,
        category_id: int,
    ) -> Category | None:
        return self.db.get(Category, category_id)

    def get_all_by_restaurant(
        self,
        restaurant_id: int,
    ) -> list[Category]:

        statement = (
            select(Category)
            .where(Category.restaurant_id == restaurant_id)
            .order_by(Category.id)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update(
        self,
        category: Category,
    ) -> Category:

        self.db.flush()
        return category

    def delete(
        self,
        category: Category,
    ) -> None:

        self.db.delete(category)
        self.db.flush()