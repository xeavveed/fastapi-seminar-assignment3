from typing import Annotated, Sequence
import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from wapang.database.connection import get_db_session
from wapang.app.reviews.models import Review


class ReviewRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]) -> None:
        self.session = session

    def add_review(self, review: Review) -> Review:
        self.session.add(review)
        self.session.flush()
        return review
    
    def get_review_by_id(self, review_id: str) -> Review | None:
        reviewLoc = select(Review).where(Review.id == review_id)
        return self.session.scalar(reviewLoc)
    
    def get_reviews_for_product(self, product_id: str) -> list[Review]:
        reviewsLoc = select(Review).where(Review.product_id == product_id)
        return self.session.scalars(reviewsLoc).all()

    def get_user_review_for_product(self, user_id: str, product_id: str) -> Review | None:
        reviewLoc = select(Review).where(
            Review.user_id == user_id,
            Review.product_id == product_id,
        )
        return self.session.scalar(reviewLoc)

    def modify_review(self, review: Review, **kwargs) -> Review:
        for key, value in kwargs.items():
            setattr(review, key, value)
        self.session.flush()
        return review
    
    def delete_review(self, review: Review) -> None:
        self.session.delete(review)
        self.session.flush()