from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ConflictException,
    NotFoundException,
)
from app.models.category import Category
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


class CategoryService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = CategoryRepository(db)

    def create(
        self,
        data: CategoryCreate,
        current_user: User,
    ) -> Category:

        if current_user.restaurant_id is None:
            raise NotFoundException(
                "Restaurant not found"
            )

        category = Category(
            name=data.name,
            restaurant_id=current_user.restaurant_id,
        )

        try:
            category = self.repository.create(category)

            self.db.commit()
            self.db.refresh(category)

            return category

        except IntegrityError:
            self.db.rollback()

            raise ConflictException(
                "Unable to create category"
            )

    def get_all(
        self,
        current_user: User,
    ) -> list[Category]:

        if current_user.restaurant_id is None:
            return []

        return self.repository.get_all_by_restaurant(
            current_user.restaurant_id
        )

    def get_by_id(
        self,
        category_id: int,
        current_user: User,
    ) -> Category:

        category = self.repository.get_by_id(
            category_id
        )

        if category is None:
            raise NotFoundException(
                f"Category with id {category_id} not found"
            )

        if (
            category.restaurant_id
            != current_user.restaurant_id
        ):
            raise NotFoundException(
                f"Category with id {category_id} not found"
            )

        return category

    def update(
        self,
        category_id: int,
        data: CategoryUpdate,
        current_user: User,
    ) -> Category:

        category = self.get_by_id(
            category_id,
            current_user,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(category, field, value)

        try:
            category = self.repository.update(
                category
            )

            self.db.commit()
            self.db.refresh(category)

            return category

        except IntegrityError:
            self.db.rollback()

            raise ConflictException(
                "Unable to update category"
            )

    def delete(
        self,
        category_id: int,
        current_user: User,
    ) -> None:

        category = self.get_by_id(
            category_id,
            current_user,
        )

        try:
            self.repository.delete(category)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise