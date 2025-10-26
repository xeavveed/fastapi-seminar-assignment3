from typing import Annotated, List
from fastapi import APIRouter, Depends, status

from wapang.app.auth.utils import login_with_header
from wapang.app.stores.schemas import ChangeStoreRequest, NewStoreRequest, StoreResponse
from wapang.app.items.schemas import ProductResponse
from wapang.app.users.models import User
from wapang.app.stores.services import StoreService

store_router = APIRouter()


@store_router.post("/", status_code=status.HTTP_201_CREATED)
def new_store(
    new_store_request: NewStoreRequest,
    user: Annotated[User, Depends(login_with_header)],
    store_service: Annotated[StoreService, Depends()],
) -> StoreResponse:
    return StoreResponse.model_validate(
        store_service.create_store(user, **new_store_request.model_dump())
    )


@store_router.patch("/{store_id}", status_code=status.HTTP_200_OK)
def patch_store(
    change_request: ChangeStoreRequest,
    user: Annotated[User, Depends(login_with_header)],
    store_service: Annotated[StoreService, Depends()],
    store_id: str,
) -> StoreResponse:
    store = store_service.get_store_by_id(user, store_id)
    store = store_service.modify_store(store, change_request)
    return StoreResponse.model_validate(store)


@store_router.get("/{store_id}")
def get_store(
    store_service: Annotated[StoreService, Depends()],
    store_id: str,
) -> StoreResponse:
    store = store_service.get_store_by_id(None, store_id)
    return StoreResponse.model_validate(store)


@store_router.get("/{store_id}/items")
def get_store_items(
    store_service: Annotated[StoreService, Depends()],
    store_id: str,
) -> List[ProductResponse]:
    store = store_service.get_store_by_id(None, store_id)
    products = store_service.get_all_products(store)
    return [ProductResponse.model_validate(product) for product in products]
