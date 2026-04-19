from collections import Counter

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.models.reading_list import ReadingList, ReadingListItem
from app.models.review import Review
from app.models.user import User
from app.schemas.analytics import (
    GenreAnalyticsResponse,
    GenreStat,
    RecommendationResponse,
    UserPreferencesResponse,
)
from app.services.recommendation import build_basic_recommendations

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _split_subjects(subject_text: str | None) -> list[str]:
    if not subject_text:
        return []
    return [subject.strip() for subject in subject_text.split(",") if subject.strip()]


@router.get("/genres", response_model=GenreAnalyticsResponse)
def genre_analytics(db: Session = Depends(get_db)) -> GenreAnalyticsResponse:
    counter: Counter[str] = Counter()
    for (subject_text,) in db.query(Book.subject).filter(Book.subject.is_not(None)).all():
        for subject in _split_subjects(subject_text):
            counter[subject] += 1

    genres = [
        GenreStat(name=name, count=count)
        for name, count in counter.most_common(10)
    ]
    return GenreAnalyticsResponse(genres=genres)


@router.get("/user/{user_id}/preferences", response_model=UserPreferencesResponse)
def user_preferences(user_id: int, db: Session = Depends(get_db)) -> UserPreferencesResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    subject_counter: Counter[str] = Counter()
    author_counter: Counter[str] = Counter()

    review_rows = (
        db.query(Review, Book)
        .join(Book, Review.book_id == Book.id)
        .filter(Review.user_id == user_id)
        .all()
    )
    for review, book in review_rows:
        weight = max(review.rating, 1)
        for subject in _split_subjects(book.subject):
            subject_counter[subject] += weight
        if book.author_name:
            author_counter[book.author_name] += weight

    list_rows = (
        db.query(Book)
        .join(ReadingListItem, ReadingListItem.book_id == Book.id)
        .join(ReadingList, ReadingList.id == ReadingListItem.reading_list_id)
        .filter(ReadingList.user_id == user_id)
        .all()
    )
    for book in list_rows:
        for subject in _split_subjects(book.subject):
            subject_counter[subject] += 1
        if book.author_name:
            author_counter[book.author_name] += 1

    ratings = [review.rating for review, _ in review_rows]
    average_rating = round(sum(ratings) / len(ratings), 2) if ratings else None

    return UserPreferencesResponse(
        user_id=user_id,
        favorite_subjects=[name for name, _ in subject_counter.most_common(3)],
        favorite_authors=[name for name, _ in author_counter.most_common(3)],
        average_rating=average_rating,
    )


@router.get("/recommendations/user/{user_id}", response_model=RecommendationResponse)
def recommendations(user_id: int, db: Session = Depends(get_db)) -> RecommendationResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    recommendations = build_basic_recommendations(db, user_id)
    return RecommendationResponse(user_id=user_id, recommendations=recommendations)
