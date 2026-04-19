from collections import Counter

from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.reading_list import ReadingList, ReadingListItem
from app.models.review import Review


def _split_subjects(subject_text: str | None) -> list[str]:
    if not subject_text:
        return []
    return [subject.strip() for subject in subject_text.split(",") if subject.strip()]


def build_basic_recommendations(db: Session, user_id: int) -> list[dict[str, str | int | None]]:
    user_list_ids = [
        row[0]
        for row in db.query(ReadingList.id).filter(ReadingList.user_id == user_id).all()
    ]
    seen_book_ids = {
        row[0]
        for row in db.query(ReadingListItem.book_id)
        .filter(ReadingListItem.reading_list_id.in_(user_list_ids))
        .all()
    }
    reviewed_book_ids = {
        row[0] for row in db.query(Review.book_id).filter(Review.user_id == user_id).all()
    }
    seen_book_ids.update(reviewed_book_ids)

    preferred_subjects: Counter[str] = Counter()
    preferred_authors: Counter[str] = Counter()

    positive_reviews = (
        db.query(Review, Book)
        .join(Book, Review.book_id == Book.id)
        .filter(Review.user_id == user_id, Review.rating >= 4)
        .all()
    )
    for _, book in positive_reviews:
        for subject in _split_subjects(book.subject):
            preferred_subjects[subject] += 2
        if book.author_name:
            preferred_authors[book.author_name] += 2

    list_books = (
        db.query(Book)
        .join(ReadingListItem, ReadingListItem.book_id == Book.id)
        .join(ReadingList, ReadingList.id == ReadingListItem.reading_list_id)
        .filter(ReadingList.user_id == user_id)
        .all()
    )
    for book in list_books:
        for subject in _split_subjects(book.subject):
            preferred_subjects[subject] += 1
        if book.author_name:
            preferred_authors[book.author_name] += 1

    candidates = db.query(Book).filter(~Book.id.in_(seen_book_ids) if seen_book_ids else True).all()

    scored_candidates: list[tuple[int, Book, str]] = []
    for book in candidates:
        score = 0
        reasons: list[str] = []

        matching_subjects = [
            subject for subject in _split_subjects(book.subject) if subject in preferred_subjects
        ]
        if matching_subjects:
            subject_score = sum(preferred_subjects[subject] for subject in matching_subjects)
            score += subject_score
            reasons.append(f"matches your preferred subjects: {', '.join(matching_subjects[:2])}")

        if book.author_name and book.author_name in preferred_authors:
            score += preferred_authors[book.author_name]
            reasons.append(f"includes an author you rate highly: {book.author_name}")

        if score > 0:
            scored_candidates.append((score, book, "; ".join(reasons)))

    scored_candidates.sort(key=lambda item: (-item[0], item[1].title.lower()))

    return [
        {
            "book_id": book.id,
            "openlibrary_key": book.openlibrary_key,
            "title": book.title,
            "author_name": book.author_name,
            "subject": book.subject,
            "cover_url": book.cover_url,
            "reason": reason or "Similar to your saved books and reviews",
        }
        for _, book, reason in scored_candidates[:5]
    ]
