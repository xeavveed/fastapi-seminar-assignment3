from typing import Annotated, Sequence
import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from wapang.app.users.models import User
from wapang.app.stores.models import Store
from wapang.database.connection import get_db_session


class StoreRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]) -> None:
        self.session = session

    def create_store(
        self,
        user_id: str,
        store_name: str,
        address: str,
        email: str,
        phone_number: str,
        delivery_fee: int,
    ) -> Store:
        store = Store(
            user_id=user_id,
            store_name=store_name,
            address=address,
            email=email,
            phone_number=phone_number,
            delivery_fee=delivery_fee,
        )
        self.session.add(store)
        self.session.flush()
        return store

    def modify_store(self, store: Store, **kwargs) -> Store:
        for key, value in kwargs.items():
            setattr(store, key, value)
        self.session.commit()
        return store

    def get_store_by_id(self, id: str) -> Store | None:
        return self.session.scalar(select(Store).where(Store.id == id))

    def get_store_by_name(self, name: str) -> Store | None:
        return self.session.scalar(select(Store).where(Store.store_name == name))

    def get_store_by_email(self, email: str) -> Store | None:
        return self.session.scalar(select(Store).where(Store.email == email))

    def get_store_by_phone(self, phone_number: str) -> Store | None:
        return self.session.scalar(
            select(Store).where(Store.phone_number == phone_number)
        )

    def get_store_by_user(self, user_id: str) -> Store | None:
        return self.session.scalar(select(Store).where(Store.user_id == user_id))


#
# class UserRepository:
#     def __init__(self, session: Annotated[Session, Depends(get_db_session)]) -> None:
#         self.session = session
#
#     def create_user(self, email: str, hashed_password: str) -> User:
#         user = User(email=email, hashed_password=hashed_password)
#         self.session.add(user)
#
#         self.session.flush()
#
#         return user
#
#     def get_user_by_id(self, user_id: str) -> User | None:
#         return self.session.scalar(select(User).where(User.id == user_id))
#
#     def get_user_by_email(self, email: str) -> User | None:
#         return self.session.scalar(select(User).where(User.email == email))
#
#     def modify_user(self, user: User, **kwargs) -> User:
#         for key, value in kwargs.items():
#             setattr(user, key, value)
#         self.session.commit()
#         return user
#
#     def get_all_orders_from_user(self, user: User) -> Sequence[Order]:
#         return self.session.scalars(select(Order).where(Order.user_id == user.id)).all()
