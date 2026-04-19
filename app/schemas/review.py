from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    user_id: int
    book_id: int
    rating: int = Field(ge=1, le=5)
    review_text: str | None = None


class ReviewUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    review_text: str | None = None


class ReviewRead(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int
    review_text: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

