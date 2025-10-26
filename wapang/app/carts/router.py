from fastapi import APIRouter, Depends, status
from typing import Annotated

from wapang.app.auth.utils import login_with_header
from wapang.app.users.models import User
from wapang.app.carts.schemas import *
from wapang.app.carts.services import CartService
from wapang.app.orders.schemas import OrderResponse

cart_router = APIRouter()

@cart_router.patch("/", status_code=status.HTTP_200_OK)
def patch_carts(
    request: CartProductRequest, 
    user: Annotated[User, Depends(login_with_header)], 
    cart_service: Annotated[CartService, Depends()]
) -> CartResponse:
    
    stores_data, total_price = cart_service.update_cart(request, user)
    
    return CartResponse(
        details=list(stores_data.values()), 
        total_price=total_price
    )

@cart_router.get("/", status_code=status.HTTP_200_OK)
def get_carts(
    user: Annotated[User, Depends(login_with_header)], 
    cart_service: Annotated[CartService, Depends()]
) -> CartResponse:
    
    stores_data, total_price = cart_service.get_cart(user)
    
    return CartResponse(
        details=list(stores_data.values()), 
        total_price=total_price
    )

@cart_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_carts(
    user: Annotated[User, Depends(login_with_header)], 
    cart_service: Annotated[CartService, Depends()]
):
    cart_service.clear_cart(user)
    return
            
@cart_router.post("/checkout", status_code=status.HTTP_201_CREATED)
def checkout_from_cart(
    user: Annotated[User, Depends(login_with_header)],
    cart_service: Annotated[CartService, Depends()]
) -> OrderResponse:
    
    order, stores_data = cart_service.checkout(user)
    
    return OrderResponse(
        id=order.id,
        details=list(stores_data.values()),
        total_price=order.total_price,
        status=order.status
    )

        
        
