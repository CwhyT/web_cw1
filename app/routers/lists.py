from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.models.reading_list import ReadingList, ReadingListItem
from app.models.user import User
from app.schemas.reading_list import (
    ReadingListCreate,
    ReadingListDetailRead,
    ReadingListItemCreate,
    ReadingListItemRead,
    ReadingListItemUpdate,
    ReadingListRead,
    ReadingListUpdate,
)

router = APIRouter(prefix="/lists", tags=["lists"])


def _get_list_or_404(db: Session, list_id: int) -> ReadingList:
    reading_list = db.query(ReadingList).filter(ReadingList.id == list_id).first()
    if reading_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading list not found",
        )
    return reading_list


def _get_item_or_404(db: Session, list_id: int, item_id: int) -> ReadingListItem:
    item = (
        db.query(ReadingListItem)
        .filter(
            ReadingListItem.id == item_id,
            ReadingListItem.reading_list_id == list_id,
        )
        .first()
    )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading list item not found",
        )
    return item


@router.post("", response_model=ReadingListRead, status_code=status.HTTP_201_CREATED)
def create_list(payload: ReadingListCreate, db: Session = Depends(get_db)) -> ReadingList:
    user = db.query(User).filter(User.id == payload.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    reading_list = ReadingList(
        user_id=payload.user_id,
        name=payload.name,
        description=payload.description,
    )
    db.add(reading_list)
    db.commit()
    db.refresh(reading_list)
    return reading_list


@router.get("", response_model=list[ReadingListRead])
def list_lists(
    user_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[ReadingList]:
    query = db.query(ReadingList)
    if user_id is not None:
        query = query.filter(ReadingList.user_id == user_id)
    return query.order_by(ReadingList.created_at.desc()).all()


@router.get("/{list_id}", response_model=ReadingListDetailRead)
def get_list(list_id: int, db: Session = Depends(get_db)) -> ReadingListDetailRead:
    reading_list = _get_list_or_404(db, list_id)
    items = (
        db.query(ReadingListItem)
        .filter(ReadingListItem.reading_list_id == list_id)
        .order_by(ReadingListItem.added_at.desc())
        .all()
    )
    return ReadingListDetailRead(
        id=reading_list.id,
        user_id=reading_list.user_id,
        name=reading_list.name,
        description=reading_list.description,
        created_at=reading_list.created_at,
        updated_at=reading_list.updated_at,
        items=[ReadingListItemRead.model_validate(item) for item in items],
    )


@router.put("/{list_id}", response_model=ReadingListRead)
def update_list(
    list_id: int,
    payload: ReadingListUpdate,
    db: Session = Depends(get_db),
) -> ReadingList:
    reading_list = _get_list_or_404(db, list_id)
    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    for field, value in updates.items():
        setattr(reading_list, field, value)

    db.commit()
    db.refresh(reading_list)
    return reading_list


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(list_id: int, db: Session = Depends(get_db)) -> Response:
    reading_list = _get_list_or_404(db, list_id)

    db.query(ReadingListItem).filter(
        ReadingListItem.reading_list_id == reading_list.id
    ).delete()
    db.delete(reading_list)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{list_id}/items",
    response_model=ReadingListItemRead,
    status_code=status.HTTP_201_CREATED,
)
def add_list_item(
    list_id: int,
    payload: ReadingListItemCreate,
    db: Session = Depends(get_db),
) -> ReadingListItem:
    _get_list_or_404(db, list_id)

    book = db.query(Book).filter(Book.openlibrary_key == payload.openlibrary_key).first()
    if book is None:
        book = Book(
            openlibrary_key=payload.openlibrary_key,
            title=payload.title,
            author_name=payload.author_name,
            first_publish_year=payload.first_publish_year,
            subject=payload.subject,
            cover_url=payload.cover_url,
        )
        db.add(book)
        db.flush()

    existing_item = (
        db.query(ReadingListItem)
        .filter(
            ReadingListItem.reading_list_id == list_id,
            ReadingListItem.book_id == book.id,
        )
        .first()
    )
    if existing_item is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Book already exists in this reading list",
        )

    item = ReadingListItem(
        reading_list_id=list_id,
        book_id=book.id,
        status=payload.status,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put(
    "/{list_id}/items/{item_id}",
    response_model=ReadingListItemRead,
)
def update_list_item(
    list_id: int,
    item_id: int,
    payload: ReadingListItemUpdate,
    db: Session = Depends(get_db),
) -> ReadingListItem:
    item = _get_item_or_404(db, list_id, item_id)
    item.status = payload.status
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{list_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list_item(list_id: int, item_id: int, db: Session = Depends(get_db)) -> Response:
    item = _get_item_or_404(db, list_id, item_id)
    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
