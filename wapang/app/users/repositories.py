from typing import Annotated, Sequence
import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from wapang.app.reviews.models import Review
from wapang.app.users.models import User
from wapang.app.orders.models import Order
from wapang.database.connection import get_db_session


class UserRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]) -> None:
        self.session = session

    def create_user(self, email: str, hashed_password: str) -> User:
        user = User(email=email, hashed_password=hashed_password)
        self.session.add(user)

        self.session.flush()

        return user

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.session.scalar(select(User).where(User.id == user_id))

    def get_user_by_email(self, email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email))

    def modify_user(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.session.commit()
        return user

    def get_all_orders_from_user(self, user: User) -> Sequence[Order]:
        return self.session.scalars(select(Order).where(Order.user_id == user.id)).all()

    def get_all_reviews_from_user(self, user: User) -> Sequence[Review]:
        return self.session.scalars(
            select(Review).where(Review.user_id == user.id)
        ).all()
