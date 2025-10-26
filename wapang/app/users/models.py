import uuid
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wapang.database.common import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    nickname: Mapped[str | None] = mapped_column(String(30))
    address: Mapped[str | None] = mapped_column(String(150))
    phone_number: Mapped[str | None] = mapped_column(String(20))
    
    store: Mapped["Store"] = relationship(back_populates="user", uselist=False)  # type: ignore
    orders: Mapped[List["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # type: ignore
    reviews: Mapped[List["Review"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # type: ignore
    cart_products: Mapped[List["CartProduct"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # type: ignore