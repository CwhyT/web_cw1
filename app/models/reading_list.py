from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ReadingList(Base):
    __tablename__ = "reading_lists"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class ReadingListItem(Base):
    __tablename__ = "reading_list_items"
    __table_args__ = (
        UniqueConstraint("reading_list_id", "book_id", name="uq_list_book"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reading_list_id: Mapped[int] = mapped_column(
        ForeignKey("reading_lists.id"), nullable=False
    )
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="to_read", nullable=False)
    added_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

