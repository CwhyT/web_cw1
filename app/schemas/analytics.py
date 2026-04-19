from pydantic import BaseModel


class GenreStat(BaseModel):
    name: str
    count: int


class GenreAnalyticsResponse(BaseModel):
    genres: list[GenreStat]


class UserPreferencesResponse(BaseModel):
    user_id: int
    favorite_subjects: list[str]
    favorite_authors: list[str]
    average_rating: float | None = None


class RecommendationItem(BaseModel):
    book_id: int
    openlibrary_key: str
    title: str
    author_name: str | None = None
    subject: str | None = None
    cover_url: str | None = None
    reason: str


class RecommendationResponse(BaseModel):
    user_id: int
    recommendations: list[RecommendationItem]
