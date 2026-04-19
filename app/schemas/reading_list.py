from datetime import datetime

from pydantic import BaseModel


class ReadingListCreate(BaseModel):
    user_id: int
    name: str
    description: str | None = None


class ReadingListUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ReadingListRead(BaseModel):
    id: int
    user_id: int
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ReadingListItemCreate(BaseModel):
    openlibrary_key: str
    title: str
    author_name: str | None = None
    first_publish_year: int | None = None
    subject: str | None = None
    cover_url: str | None = None
    status: str = "to_read"


class ReadingListItemUpdate(BaseModel):
    status: str

