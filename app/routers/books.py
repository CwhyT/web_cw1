from fastapi import APIRouter, Query

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/search")
def search_books(q: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=50)):
    return {
        "query": q,
        "limit": limit,
        "results": [],
        "message": "Book search placeholder",
    }


@router.get("/{openlibrary_key}")
def get_book(openlibrary_key: str):
    return {
        "openlibrary_key": openlibrary_key,
        "message": "Book detail placeholder",
    }

