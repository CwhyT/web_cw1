from pydantic import BaseModel


class BookSearchResult(BaseModel):
    openlibrary_key: str
    title: str
    author_name: str | None = None
    first_publish_year: int | None = None


class BookRead(BaseModel):
    id: int
    openlibrary_key: str
    title: str
    author_name: str | None = None
    first_publish_year: int | None = None
    subject: str | None = None
    cover_url: str | None = None

    model_config = {"from_attributes": True}

