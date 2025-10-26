from typing import Annotated, List, Optional

from fastapi import Depends
from wapang.app.items.models import Product
from wapang.app.stores.exceptions import (
    NoStoreOwnedException,
    NotYourStoreException,
    StoreAlreadyExistsException,
    StoreInfoConflictException,
    StoreNotFoundException,
)
from wapang.app.stores.schemas import ChangeStoreRequest
from wapang.app.users.models import User
from wapang.app.stores.models import Store
from wapang.app.stores.repositories import StoreRepository


class StoreService:
    def __init__(self, store_repository: Annotated[StoreRepository, Depends()]) -> None:
        self.store_repository = store_repository

    def create_store(
        self,
        user: User,
        store_name: str,
        address: str,
        email: str,
        phone_number: str,
        delivery_fee: int,
    ) -> Store:
        self._check_duplicates(store_name, email, phone_number, user.id)
        return self.store_repository.create_store(
            user.id, store_name, address, email, phone_number, delivery_fee
        )

    def get_store_by_id(self, user: Optional[User], store_id: str) -> Store:
        store_from_id = self.store_repository.get_store_by_id(store_id)
        if store_from_id is None:
            raise StoreNotFoundException()

        if user is None:
            return store_from_id

        store = self.store_repository.get_store_by_user(user.id)
        if store is None:
            raise NoStoreOwnedException()

        if store.id != store_id:
            raise NotYourStoreException()

        return store

    def modify_store(self, store: Store, change_request: ChangeStoreRequest) -> Store:
        self._check_duplicates(
            change_request.store_name,
            change_request.email,
            change_request.phone_number,
            None,
        )
        return self.store_repository.modify_store(
            store, **change_request.model_dump(exclude_unset=True)
        )

    def get_all_products(self, store: Store) -> List[Product]:
        return store.products

    def _check_duplicates(
        self,
        store_name: Optional[str],
        email: Optional[str],
        phone_number: Optional[str],
        user_id: Optional[str],
    ):

        if store_name and self.store_repository.get_store_by_name(store_name):
            raise StoreInfoConflictException()
        if email and self.store_repository.get_store_by_email(email):
            raise StoreInfoConflictException()
        if phone_number and self.store_repository.get_store_by_phone(phone_number):
            raise StoreInfoConflictException()
        if user_id and self.store_repository.get_store_by_user(user_id):
            raise StoreAlreadyExistsException()

