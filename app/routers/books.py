import httpx

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.book import BookDetailResponse, BookSearchResponse, BookSearchResult
from app.services.openlibrary import fetch_search_results, fetch_work_details
from app.utils.helpers import normalize_openlibrary_key

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/search", response_model=BookSearchResponse)
async def search_books(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
) -> BookSearchResponse:
    try:
        payload = await fetch_search_results(q, limit)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Open Library search request failed",
        ) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to reach Open Library",
        ) from exc

    results = []
    for doc in payload.get("docs", []):
        work_key = doc.get("key")
        title = doc.get("title")
        if not work_key or not title:
            continue

        author_names = doc.get("author_name") or []
        cover_id = doc.get("cover_i")
        cover_url = (
            f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            if cover_id is not None
            else None
        )
        results.append(
            BookSearchResult(
                openlibrary_key=work_key,
                title=title,
                author_name=author_names[0] if author_names else None,
                first_publish_year=doc.get("first_publish_year"),
                cover_url=cover_url,
            )
        )

    return BookSearchResponse(query=q, limit=limit, results=results)


@router.get("/{openlibrary_key:path}", response_model=BookDetailResponse)
async def get_book(openlibrary_key: str) -> BookDetailResponse:
    normalized_key = normalize_openlibrary_key(openlibrary_key)
    try:
        payload = await fetch_work_details(normalized_key)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found in Open Library",
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Open Library detail request failed",
        ) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to reach Open Library",
        ) from exc

    description = payload.get("description")
    if isinstance(description, dict):
        description = description.get("value")
    elif description is not None and not isinstance(description, str):
        description = str(description)

    subjects = payload.get("subjects") or []
    covers = payload.get("covers") or []
    cover_url = (
        f"https://covers.openlibrary.org/b/id/{covers[0]}-L.jpg" if covers else None
    )

    return BookDetailResponse(
        openlibrary_key=payload.get("key", normalized_key),
        title=payload.get("title", "Unknown Title"),
        author_name=None,
        first_publish_year=payload.get("first_publish_date"),
        subject=", ".join(subjects[:5]) if subjects else None,
        cover_url=cover_url,
        description=description,
    )
