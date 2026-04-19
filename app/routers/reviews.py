from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(prefix="/reviews", tags=["reviews"])


def _get_review_or_404(db: Session, review_id: int) -> Review:
    review = db.query(Review).filter(Review.id == review_id).first()
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )
    return review


@router.post("", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)) -> Review:
    user = db.query(User).filter(User.id == payload.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    book = db.query(Book).filter(Book.id == payload.book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    review = Review(
        user_id=payload.user_id,
        book_id=payload.book_id,
        rating=payload.rating,
        review_text=payload.review_text,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get("/{review_id}", response_model=ReviewRead)
def get_review(review_id: int, db: Session = Depends(get_db)) -> Review:
    return _get_review_or_404(db, review_id)


@router.get("/book/{book_id}", response_model=list[ReviewRead])
def list_book_reviews(book_id: int, db: Session = Depends(get_db)) -> list[Review]:
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return (
        db.query(Review)
        .filter(Review.book_id == book_id)
        .order_by(Review.created_at.desc())
        .all()
    )


@router.put("/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int,
    payload: ReviewUpdate,
    db: Session = Depends(get_db),
) -> Review:
    review = _get_review_or_404(db, review_id)
    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    for field, value in updates.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)) -> Response:
    review = _get_review_or_404(db, review_id)
    db.delete(review)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
