from typing import Annotated, Optional
from argon2 import PasswordHasher

from fastapi import Depends
from wapang.app.users.models import User
from wapang.app.orders.models import Order
from wapang.app.reviews.models import Review
from wapang.app.users.repositories import UserRepository
from wapang.app.users.exceptions import EmailAlreadyExistsException
from wapang.app.users.schemas import OrderResponse, UserChangeRequest


class UserService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends()]) -> None:
        self.user_repository = user_repository

    def create_user(self, email: str, password: str) -> User:
        if self.user_repository.get_user_by_email(email):
            raise EmailAlreadyExistsException()

        hashed_password = PasswordHasher().hash(password)

        return self.user_repository.create_user(email, hashed_password)

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.user_repository.get_user_by_id(user_id)

    def modify_user(self, user: User, change_request: UserChangeRequest) -> User:
        if change_request.email is not None and self.user_repository.get_user_by_email(
            change_request.email
        ):
            raise EmailAlreadyExistsException()

        return self.user_repository.modify_user(
            user, **change_request.model_dump(exclude_unset=True)
        )

    def get_orders(self, user: User) -> list[Order]:
        return list(self.user_repository.get_all_orders_from_user(user))

    def get_reviews(self, user: User) -> list[Review]:
        return list(self.user_repository.get_all_reviews_from_user(user))
