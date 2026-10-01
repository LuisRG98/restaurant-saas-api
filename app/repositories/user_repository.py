from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        user_id: int,
    ) -> User | None:

        return self.db.get(User, user_id)

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        statement = (
            select(User)
            .where(User.email == email)
        )

        result = self.db.execute(statement)

        return result.scalar_one_or_none()

    def create(
        self,
        user: User,
    ) -> User:

        self.db.add(user)
        self.db.flush()

        return user
    
    def get_all_by_restaurant(
        self,
        restaurant_id: int,
    ) -> list[User]:

        statement = (
            select(User)
            .where(
                User.restaurant_id == restaurant_id
            )
            .order_by(User.id)
        )

        return list(
            self.db.scalars(statement).all()
        )