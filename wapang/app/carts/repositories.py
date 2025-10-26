from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session, joinedload

from wapang.app.stores.models import Store
from wapang.app.carts.models import CartProduct
from wapang.app.items.models import Product
from wapang.database.connection import get_db_session


class CartRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]) -> None:
        self.session = session
        
    def get_cart_product(self, user_id: str, product_id: str) -> CartProduct | None:
        cartLoc = select(CartProduct).where(CartProduct.user_id == user_id, CartProduct.product_id == product_id)
        return self.session.scalar(cartLoc)

    def get_all_cart_products_with_details(self, user_id: str) -> Sequence[CartProduct]:
        cartLoc = (
            select(CartProduct)
            .join(Product)
            .join(Store)
            .options(
                joinedload(CartProduct.product)
                .joinedload(Product.store)
            )
            .where(CartProduct.user_id == user_id)
        )
        return self.session.scalars(cartLoc).all()

    def add(self, cart_product: CartProduct) -> None:
        self.session.add(cart_product)

    def delete(self, cart_product: CartProduct) -> None:
        self.session.delete(cart_product)
        
    def delete_all_cart_products(self, user_id: str) -> None:
        cartLoc = delete(CartProduct).where(CartProduct.user_id == user_id)
        self.session.execute(cartLoc)