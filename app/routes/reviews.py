from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.db import database, models

router = APIRouter()

class ReviewIn(BaseModel):
    user_id: int
    course_id: int
    rating: int  # 1-5
    comment: str

class ReviewOut(ReviewIn):
    id: int
    created_at: datetime

@router.post("/reviews", response_model=ReviewOut)
async def create_review(review: ReviewIn):
    query = models.reviews.insert().values(
        user_id=review.user_id,
        course_id=review.course_id,
        rating=review.rating,
        comment=review.comment,
        created_at=datetime.utcnow()
    )
    review_id = await database.execute(query)
    return {**review.dict(), "id": review_id, "created_at": datetime.utcnow()}

@router.get("/reviews/{course_id}", response_model=List[ReviewOut])
async def get_reviews(course_id: int):
    query = models.reviews.select().where(models.reviews.c.course_id == course_id)
    results = await database.fetch_all(query)
    return results
